import networkx as nx
import requests
import json
from github import Github
import timeit
START = timeit.default_timer()

ACCESS_TOKEN = ''

# Starting point of Network
START_USERNAME = 'shopware'
START_REPONAME = 'shopware'

client = Github(ACCESS_TOKEN, per_page=100)
user = client.get_user(START_USERNAME)
repo = user.get_repo(START_REPONAME)

g = nx.DiGraph()
g.add_node(repo.name + '(repo)', type='repo', lang=repo.language, owner=user.login)

stargazers = [s for s in repo.get_stargazers()]
# Add Stargazers to the graph
for sg in stargazers:
    g.add_node(sg.login + '(user)', type='user')
    g.add_edge(sg.login + '(user)', repo.name + '(repo)', type='gazes')

# Add other starred Repos from Stargazers
for i, sg in enumerate(stargazers):
    print(sg.login)
    try:
        for starred in sg.get_starred():
            g.add_node(starred.name + '(repo)', type='repo', lang=starred.language, \
                       owner=starred.owner.login)
            g.add_edge(sg.login + '(user)', starred.name + '(repo)', type='gazes')
    except Exception as e: #ssl.SSLError:
        print("Encountered an error fetching starred repos for", sg.login, "Skipping.")

    print("Processed", i+1, "stargazers' starred repos")
    print("Num nodes/edges in graph", g.number_of_nodes(), "/", g.number_of_edges())
    print("Rate limit", client.rate_limiting)




# Save Graph
nx.write_gpickle(g, "data/github.gpickle.1")

END = timeit.default_timer()
print("Duration: ", END-START)
