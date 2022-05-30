import pulsar, _pulsar
import operator
import sys
import json
import socket


#Find corresponding positon for a number in a descending sorted list
def find_position(repo_commits:list, n_commits:int):
    # Check if list is empty
    if not repo_commits:
        return 0
    new_pos = 0
    for value in repo_commits:
        if value >= n_commits:
            new_pos += 1
        else:
            return new_pos
    return new_pos

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        print("Program requires 1 input args: number of top repositories to retrieve!")
        sys.exit(1)
    n_top_repos = int(args[0])
    #Pulsar setup
    client = pulsar.Client('pulsar://pulsarbroker:6650')
    consumer = client.subscribe('DE2-commit', subscription_name='DE-Q1', consumer_type=_pulsar.ConsumerType.Shared)
    agg_producer = client.create_producer('DE2-agg')
    
    #List of repos and their corresponding number of commits
    repo_list = []
    repo_commits = []
    #Aggregation message
    agg_msg = {}
    agg_msg['type'] = 'Q2'

    msg_count = 0
    frequency = 100 #frequency of printing top list/send update

    while True:
        msg = consumer.receive()
        msg_count += 1
        try:
            content = msg.data().decode('utf-8').replace("'", '"')
            repo = json.loads(content)
            repo_name = repo['name']
            #Check if repo already exists in list
            if(repo_name in repo_list):
                break
            n_commits = 0
            #count total of commits from all branches
            for branch in list(repo['commit_count']):
                n_commits += branch['target']['history']['totalCount']
            #Find position for new repo in the list
            repo_pos = find_position(repo_commits, n_commits)
            #If not in top highest commits, do nothing
            if repo_pos <= n_top_repos:
                repo_list.insert(repo_pos, repo_name)
                repo_commits.insert(repo_pos, n_commits)
                #if list longer than n_top_repos, remove the last element from list
                if len(repo_list) > n_top_repos:
                    repo_list.pop()
                    repo_commits.pop()
                #Periodically print out list of languages and project counts
            if msg_count % frequency == 0:
                print("Current list of top %d repository with most commits from %d message:" %(n_top_repos, msg_count))
                print(dict(zip(repo_list, repo_commits)))
                #Craft message to the aggregation server
                agg_msg['worker'] = socket.gethostname() #for agg server tell apart different replicas of a consumer
                agg_msg['result'] = dict(zip(repo_list, repo_commits))
                #Send aggregation message
                agg_producer.send(str(agg_msg).encode('utf-8'))
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    # Destroy pulsar client
    client.close()