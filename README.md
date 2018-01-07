# FileLiner 

Returns the `filename` and the `line number` of comments in a file in a pull request. Also returns the `author` and the `comment` made by the author in a `dict`.  Multiple comments for line are stored in a list.

### Usage
```
usage: file-liner.py [-h] url

Get comments for a file in pull request.

positional arguments:
  url         The full url of the repo containing the pull request e.g
              https://github.com/<owner>/<repo>/pull/<pr_id>

optional arguments:
  -h, --help  show this help message and exit

```

### Example

```
> python3 file-liner.py example_owner/example_repo/pull/222

{'blah/c.go:12': [{'author': 'Bob', 'comment': 'This is test comment for line 12 in  somefile/c.go'}], 'blah/c.go:102': [{'author': 'Alice', 'comment': 'Test comment on line 102'}, {'author':'Jane', 'comment': 'Multiple comment on the same line'}]}
```

