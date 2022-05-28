import pulsar, _pulsar
import operator
import sys
import json

#Find corresponding positon for a number in a descending sorted list
def find_position(repo_commits:list, n_commits:int):
    # Check if list is empty
    if not repo_commits:
        return 0
    new_pos = 0
    for value in repo_commits:
        if value > n_commits:
            new_pos += 1
        else:
            return new_pos
    return new_pos

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        print("Program requires 1 input args: number of top repositories to retrieve!")
        sys.exit(1)
    n_repos = int(args[0])
    #Pulsar setup
    client = pulsar.Client('pulsar://localhost:6650')
    consumer = client.subscribe('DE2-commit', subscription_name='DE-Q1', consumer_type=_pulsar.ConsumerType.Shared)
    
    #List of repos and their corresponding number of commits
    repo_list = []
    repo_commits = []
    count = 0
    frequency = 100 #frequency of printing top list/send update

    while True:
        msg = consumer.receive()
        try:
            content = msg.data().decode('utf-8')
            repo = json.loads(content)
            repo_name = repo['name']
            n_commits = 0
            #count total of commits from all branches
            for branch in list(repo['commit_count']):
                n_commits += branch['target']['history']['totalCount']
            #Find position for new repo in the list
            repo_pos = find_position(repo_commits, n_commits)
            #If not in top highest commits, do nothing
            if repo_pos >= n_repos:
                pass
            #Otherwise, add to list
            else:
                repo_list.insert(repo_pos, repo_name)
                repo_commits.insert(repo_pos, n_commits)
                #if list longer than n_repos, remove the last element from list
                if len(repo_list) > n_repos:
                    repo_list.pop()
                    repo_commits.pop()
                #Periodically print out list of languages and project counts
            if count == frequency:
                print("Current list of top %d repository with most commits:" %n_repos)
                print(dict(zip(repo_list, repo_commits)))
                count = 0
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    # Destroy pulsar client
    client.close()