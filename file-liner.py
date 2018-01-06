#!/usr/local/bin/python3

import requests
import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

GITHUB_URL="https://api.github.com/graphql"
GITHUB_TOKEN=os.getenv('GITHUB_TOKEN')
DATA= open("../scratch/comments.graphql").read()
client = Client(
    transport=RequestsHTTPTransport(url=GITHUB_URL,
                                    headers={
                                        'Authorization': 'bearer ' + GITHUB_TOKEN,
                                    },
                                    use_json=True),
    
)
query = gql(DATA)
resultqueryg = client.execute(query)
print(result)

