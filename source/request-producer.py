import pulsar
import sys
import requests
from datetime import datetime, timedelta
import time

PULSAR_IP = '192.168.2.139'

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
          defaultBranchRef {
            name
            target {
              ... on Commit {
                history {
                  totalCount
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
          defaultBranchRef {
            name
            target {
              ... on Commit {
                history {
                  totalCount
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
    variables['numRepos'] = 40 #Number of repos in a response
    #getting the first page
    try:
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
    except:
      print("ERROR sending request!!!!!")

if __name__ == '__main__':
    #Validate program arguments
    args = sys.argv[1:]
    if len(args) != 4:
        print("Program requires 4 input args: github-username , token, start_date(Y-m-d) and end_date (Y-m-d)!")
        sys.exit(1)

    #Pulsar setup
    client = pulsar.Client('pulsar://' + PULSAR_IP + ':6650')
    producer = client.create_producer('DE2-repo')
    agg_producer = client.create_producer('DE2-agg')
    producer_name = producer.producer_name()
    agg_producer.send('start'.encode('utf-8'), properties={'producer': producer_name})
    
    #Github authentication
    username = args[0]
    token = args[1]

    start_date = datetime.strptime(args[2], '%Y-%m-%d')
    end_date = datetime.strptime(args[3], '%Y-%m-%d')
    period = (end_date - start_date).days + 1

    request_count = 0
    error_count = 0
    retry_count = 0

    #iterate over days in period
    for i in range(0, int(period)):
        retry_count = 0 #reset retry count
        date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        continue_flag = True
        while(continue_flag):
          response = send_request(date=date, username=username, token=token)
          request_count += 1
          #If successful response
          if response != None and response['data']['search']['repositoryCount'] != 0:
            retry_count = 0 #reset retry count
            repos = response['data']['search']['edges'] #list of repositories
            page_info = response['data']['search']['pageInfo'] #page info (to find if more results exist)
            #Iterate over repository list
            for repo in repos:
                msg = str(repo['node']).replace("'", '"')
                producer.send(msg.encode('utf-8'), properties={'producer': producer_name})
            
            #Check if more results exists
            if page_info['hasNextPage'] == True:
                next_page_cursor = page_info['endCursor']
                continue_flag = True #indicate to continue requesting next page
                #Request results till last page
                while(continue_flag):
                    traverse_response = send_request(date=date, after = next_page_cursor, username=username, token=token)
                    request_count += 1
                    if traverse_response != None:
                        retry_count = 0
                        repos = traverse_response['data']['search']['edges'] #list of repositories
                        page_info = traverse_response['data']['search']['pageInfo'] #page info (to find if more results exist)
                        #Iterate over repository list
                        for repo in repos:
                            msg = str(repo['node']).replace("'", '"')
                            producer.send(msg.encode('utf-8'), properties={'producer': producer_name})
                        #Continue if still have more results
                        if page_info['hasNextPage'] == True:
                            next_page_cursor = page_info['endCursor']
                        else: #otherwise quit
                            continue_flag = False
                    else:
                        error_count += 1
                        retry_count += 1
                        #if number of retrying request > 3 then move to the next date
                        if retry_count > 3:
                          continue_flag = False
                    time.sleep(0.3)
          else:
            retry_count += 1
            error_count += 1
            #if number of retrying request > 3 then move to the next date
            if retry_count > 3:
              continue_flag = False
        print("Finish request(s) for date: %s" %date)

    print("Job Finished with %d total number of request, with %d error response" %(request_count, error_count))
    time.sleep(3)
    #Send ending signal
    for i in range(5):
        producer.send('finish'.encode('utf-8'), properties={'producer': producer_name})
    #Destroy pulsar client
    producer.close()
    client.close()