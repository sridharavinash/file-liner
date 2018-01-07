#!/usr/local/bin/python3

import requests
import os
import re
import argparse

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class FileLiner(object):
    def __init__(self, gql_url, token, data):
        self.graphql_url = gql_url
        self.token = token
        self.diff_re = re.compile("@@ -(\d+).*@@")
        self.data = data
        self.query = None
        self.variables = None

    def client(self):
        client = Client(
            transport=RequestsHTTPTransport(url=self.graphql_url,
                                            headers={'Authorization': 'bearer ' + self.token},
                                            use_json=True)
        )
        return client

    def build_query(self, args):
        parts = args.url.split("/")
        try:
            owner = parts[-4]
            repo = parts[-3]
            prId = int(parts[-1])
        except IndexError:
            return False

        self.query = gql(self.data)
        self.variables={"owner": owner, "repo": repo, "pr_id": prId}
        return True

    def get_comments(self):
        try:
            result = self.client().execute(self.query, self.variables)
        except Exception as e:
            print("Error:",e)
            return {}

        results = {}
        for r in result['repository']['pullRequest']['reviews']['nodes']:
            for n in r['comments']['nodes']:
                filename = n['path']
                author = n['author']['login']
                comment = n['bodyText']
                line = self.get_line_for_comment(n['diffHunk'])
                key = filename+':'+str(line)
                if key not in results:
                    results[key] = [{'author': author, 'comment': comment}]
                else:
                    results[key].append({'author': author, 'comment': comment})
        return results

    def get_line_for_comment(self, diff_hunk):
        '''Get the start of the line of the comment from the diffHunk'''
        found_start =  self.diff_re.search(diff_hunk)
        if found_start == None:
            return 0
        pos = int(found_start[1])
        for i in diff_hunk.split('\n')[1:]:
            if i[0] != '-':
                pos +=1
        return pos

def main():
    parser = argparse.ArgumentParser(description='Get comments for a file in pull request.')
    parser.add_argument("url", help="The full url of the repo containing the pull request e.g https://github.com/<owner>/<repo>/pull/<pr_id>")

    args =  parser.parse_args()

    github_gql_url="https://api.github.com/graphql"
    github_token=os.getenv('GITHUB_TOKEN')
    if github_token == None:
        print("Error: No GITHUB_TOKEN environment variable set. ")
        exit(1)

    data= open("./comments.graphql").read()
    fl = FileLiner(gql_url=github_gql_url,token=github_token, data=data)
    if not fl.build_query(args):
        print("PR url is malformed, expecting <owner>/<repo>/pull/<pr_id>")
        exit(1)

    print(fl.get_comments())

if __name__ == '__main__':
    main()




