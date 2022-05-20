import pulsar
import operator
import sys

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
        print("Program requires 1 input args: number of repositories to retrieve!")
        sys.exit(1)
    n_repos = int(args[0])
    #Pulsar setup
    client = pulsar.Client('pulsar://localhost:6650')
    consumer = client.subscribe('DE2-Q2', subscription_name='DE-Q2-sub')
    
    #List of repos and their corresponding number of commits
    repo_list = []
    repo_commits = []

    while True:
        msg = consumer.receive()
        try:
            content = msg.data().decode('utf-8').split(';;;')
            if content[0] == 'end-here': #receive end signal
                #Sort language list in descending order of appearing times
                print("Analysis result: Top %d most commited repositories are" %n_repos)
                print(dict(zip(repo_list, repo_commits)))
                repo_list = []
                repo_commits = []
            else:
                repo_name = content[0]
                n_commits = int(content[1])
                #Insert to list basing on n_repos value
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

            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    # Destroy pulsar client
    client.close()
