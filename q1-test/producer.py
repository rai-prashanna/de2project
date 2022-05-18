import pulsar
import sys
from urllib.parse import urlencode
import requests
from datetime import datetime, timedelta
import time

def url_build(base_url, query, params):
    query_str = ''
    for key in query:
        query_str += str(key) + ':' + query[key]
        query_str += '+'
    return base_url + query_str + '&' + urlencode(params)

if __name__ == '__main__':
    #Validate program arguments
    args = sys.argv[1:]
    if len(args) != 2:
        print("Program requires 2 input args: github-username and token!")
        sys.exit(1)

    #Pulsar setup
    client = pulsar.Client('pulsar://localhost:6650')
    producer = client.create_producer('DE2-Q1')
    
    #Github authentication
    username = args[0]
    token = args[1]

    #Github API base URL
    base_url = 'https://api.github.com/search/repositories?q='

    #Construct query
    query = {}
    query['pushed'] = '2021-01-01' #repositories pushed at date
    query['sort'] = 'stars-desc' #sort by number of stars in descending order
    params = {}
    params['per_page'] = 100 #number of results per page

    start_date = datetime(2021,1,1)
    period = 3; #search for 5 days from start_date

    #iterate over days in period
    for i in range(0, period):
        date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        query['pushed'] = date #set query pushed date
        #iterate over pages of result (10 pages * 100 = 1000 results)
        for j in range(1,11):
            params['page'] = j #return result in page #
            #Query URL
            url = url_build(base_url, query, params)
            #Send request and retrieve data
            response = requests.get(url, auth = requests.auth.HTTPBasicAuth(username, token))
            repos = response.json()['items']
            # Send a message to topic
            for repo in repos:
                #skip repos without language
                if repo['language']:
                    producer.send(str(repo['language']).encode('utf-8'))
            # Sleep 2s after a request due to limitation of 30 requests/min
            time.sleep(2)

    #Send ending signal to consumer
    producer.send('end-here'.encode('utf-8'))
    #Destroy pulsar client
    client.close()