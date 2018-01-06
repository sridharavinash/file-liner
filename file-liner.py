#!/usr/local/bin/python3

import requests
import os
import re
import argparse

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

parser = argparse.ArgumentParser(description='Get comments for a file in pull request.')
parser.add_argument("url", help="The full url of the repo containing the pull request e.g https://github.com/<owner>/<repo>/pull/<pr_id>")

args =  parser.parse_args()

parts = args.url.split("/")

owner = parts[-4]
repo = parts[-3]
prId = int(parts[-1])

GITHUB_URL="https://api.github.com/graphql"
GITHUB_TOKEN=os.getenv('GITHUB_TOKEN')
DATA= open("./comments.graphql").read()

# get the first value of the diff hunk line number
diff_re = re.compile("@@ -(\d+).*@@")

def calc_start_line(diff_hunk):
    ''' Get the start of the line of the comment from the diffHunk'''
    global diff_re
    found_start =  diff_re.search(diff_hunk)
    if found_start == None:
        return 0
    pos = int(found_start[1])
    for i in diff_hunk.split('\n')[1:]:
        if i[0] != '-':
            pos +=1
    return pos

client = Client(
    transport=RequestsHTTPTransport(url=GITHUB_URL,
                                    headers={
                                        'Authorization': 'bearer ' + GITHUB_TOKEN,
                                    },
                                    use_json=True),
)
query = gql(DATA)
variables={"owner": owner, "repo": repo, "pr_id": prId}


result = client.execute(query, variables)

for r in result['repository']['pullRequest']['reviews']['nodes']:
    for n in r['comments']['nodes']:
        print(n['author']['login'])
        print(n['path'])
        print(n['bodyText'])
        print(calc_start_line(n['diffHunk']))
