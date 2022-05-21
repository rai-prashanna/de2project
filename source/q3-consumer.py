import json
import pulsar
import operator
import sys
import json
import re

keywords = ['test', 'spec']
regex_expression = '(\s|^|\W|\d)' + "|".join(map(re.escape, keywords)) + '(\s|$|\W|\d)'

def has_unit_test(list = list):
    for unit in list:
        #search for pattern in its name
        if re.search(regex_expression, unit['name'], re.IGNORECASE):
            return 1
        #If being directory -> search inside
        if unit['type'] == "tree":
            sub_dir = unit['object']['entries']
            for sub_unit in sub_dir:
                if re.search(regex_expression, sub_unit['name'], re.IGNORECASE):
                    return 1
    return 0
        


if __name__ == '__main__':
    #Validate program arguments
    args = sys.argv[1:]
    if len(args) != 1:
        print("Program requires 1 input arg: number of top repos")
        sys.exit(1)
    n_repos = args[0]
    #Pulsar setup
    client = pulsar.Client('pulsar://localhost:6650')
    consumer = client.subscribe('DE2-Q34', subscription_name='DE2-Q3-sub')
    #language list
    language_count = {}
    while True:
        msg = consumer.receive()
        try:
            content = msg.data().decode('utf-8')
            if content == 'end-here': #receive end signal
                #Sort language list in descending order of appearing times
                sorted_list = sorted(language_count.items(),key=operator.itemgetter(1),reverse=True)
                print("Analysis result: Top %s most programming languages that follow unit-test developement approach are" %n_repos)
                print(sorted_list[0:int(n_repos)])
                language = {}
            else:
                repo = json.loads(content)
                repo_language = repo['primaryLanguage']['name']
                file_list = repo['object']['entries']
                #Check folder/file matching patterns
                if has_unit_test(file_list):
                    if repo_language in language_count.keys():
                        language_count[repo_language] += 1
                    else:
                        language_count[repo_language] = 1
                
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    # Destroy pulsar client
    client.close()