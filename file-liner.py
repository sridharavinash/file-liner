#!/usr/local/bin/python3

import requests
import os
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
print(result)
