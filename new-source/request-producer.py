import pulsar
import sys
import requests
from datetime import datetime, timedelta
import time

first_query = """
query ($queryString: String!, $numRepos: Int!) {
  search(query: $queryString, type: REPOSITORY, first: $numRepos) {
    pageInfo {
      hasNextPage
      endCursor
    }
    repositoryCount
    edges {
      node {
        ... on Repository {
          primaryLanguage {
            name
          }
          nameWithOwner
          refs(first: 100, refPrefix: "refs/heads/") {
            nodes {
              name
              target {
                ... on Commit {
                  history {
                    totalCount
                  }
                }
              }
            }
          }
          object(expression: "HEAD:") {
            ... on Tree {
              entries {
                name
                type
                object {
                  ... on Tree {
                    entries {
                      name
                      type
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

secondary_query = """
query ($queryString: String!, $previousCursor: String!, $numRepos: Int!) {
  search(query: $queryString, type: REPOSITORY, first: $numRepos, after: $previousCursor ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    repositoryCount
    edges {
      node {
        ... on Repository {
          primaryLanguage {
            name
          }
          nameWithOwner
          refs(first: 100, refPrefix: "refs/heads/") {
            nodes {
              name
              target {
                ... on Commit {
                  history {
                    totalCount
                  }
                }
              }
            }
          }
          object(expression: "HEAD:") {
            ... on Tree {
              entries {
                name
                type
                object {
                  ... on Tree {
                    entries {
                      name
                      type
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

def send_request(date=None, after=None, username=None, token=None):
    auth = requests.auth.HTTPBasicAuth(username, token)
    variables ={}
    variables['queryString'] = "created:"+ date +" sort:stars-desc"
    variables['numRepos'] = 25 #Number of repos in a response
    #getting the first page
    if after == None:
        response = requests.post('https://api.github.com/graphql', json={'query': first_query, 'variables': variables}, auth = auth)
    #traverse to next page
    else:
        variables['previousCursor'] = after
        response = requests.post('https://api.github.com/graphql', json={'query': secondary_query, 'variables': variables}, auth = auth)

    #Check response
    if response.status_code == 200:
        return response.json()
    else:
        print("Error searching repository for created date: %s with following message: %s" %(date, response.json()))
        return None

if __name__ == '__main__':
    #Validate program arguments
    args = sys.argv[1:]
    if len(args) != 2:
        print("Program requires 2 input args: github-username and token!")
        sys.exit(1)

    #Pulsar setup
    client = pulsar.Client('pulsar://localhost:6650')
    producer = client.create_producer('DE2-repo')
    
    #Github authentication
    username = args[0]
    token = args[1]

    start_date = datetime(2021,1,1)
    period = 5; #search for 'period' days from start_date

    #iterate over days in period
    for i in range(0, period):
        date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        response = send_request(date=date, username=username, token=token)
        if response != None and response['data']['search']['repositoryCount'] != 0:
            repos = response['data']['search']['edges'] #list of repositories
            page_info = response['data']['search']['pageInfo'] #page info (to find if more results exist)
            #Iterate over repository list
            for repo in repos:
                msg = str(repo['node']).replace("'", '"')
                producer.send(msg.encode('utf-8'))
            
            #Check if more results exists
            if page_info['hasNextPage'] == True:
                next_page_cursor = page_info['endCursor']
                continue_flag = True #indicate to continue requesting next page
                #Request results till last page
                while(continue_flag):
                    traverse_response = send_request(date=date, after = next_page_cursor, username=username, token=token)
                    if traverse_response != None:
                        repos = traverse_response['data']['search']['edges'] #list of repositories
                        page_info = traverse_response['data']['search']['pageInfo'] #page info (to find if more results exist)
                        #Iterate over repository list
                        for repo in repos:
                            msg = str(repo['node']).replace("'", '"')
                            producer.send(msg.encode('utf-8'))
                        #Continue if still have more results
                        if page_info['hasNextPage'] == True:
                            next_page_cursor = page_info['endCursor']
                        else: #otherwise quit
                            continue_flag = False
                    else:
                        continue_flag = False
                    time.sleep(0.7)
        print("Finish request(s) for date: %s" %date)

    #Send ending signal to consumer
    # producer.send('end-here'.encode('utf-8'))
    #Destroy pulsar client
    client.close()