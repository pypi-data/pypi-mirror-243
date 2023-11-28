# arx - a simple data archiving tool

'arx' is a simple data archiving tool.  A local directory, or "repo",
is initialized (with the 'init' command) to be a staging ground and
mirror of a remote archive.  Files and directories can be copied into
the repo and then committed to the remote archive (with the 'commit'
command).  Files and directories in the remote archive can be checked
out from the archive for viewing and processing (with the 'checkout'
command).

Arx assumes a repository exists as tree of files on a remote server
accessible via ssh and rsync.  No other remote configuration is needed.

NOTE: Arx maintains only a write-once archive.  Once a file has been
committed to the repository it can't be changed or updated.

## installation

### requirements

`arx` only depends on one python package that's not included in the
standard library (`pyyaml`).  It otherwise depends on a couple of
non-python packages that are usually available by default in most
systems:

- ssh client
- rsync
- find

It is unlikely on most systems that these apps wouldn't be available.

## usage

### command line interface

Assuming an existing pre-configured remote of the form HOST:PATH,
initialize a local repo mirror:
```shell
$ arx init HOST:PATH my_repo
$ cd my_repo
$ arx config
root: /path/to/my_repo
remote: HOST:PATH
```

Add a file to the repo:
```shell
$ cp /path/to/other_file file2
```

List files in the archive and in the local repo:
```shell
$ arx list
- file1
+ file2
```
The '-'/'+' prefixes indicate files that only exist remotely/locally,
respectively.  No prefix indicates the file exists in both places.

Checkout a file from the archive:
```shell
$ arx checkout file1
$ arx list
  file1
+ file2
```

Commit a file to the repo:
```shell
$ arx commit file2
$ arx list
  file1
  file2
```

### python library

Arx also includes a python library from which all of the same
functionality can be accessed.

The basic interface is through the `Repo` class.  A new repo can be
created with the `Repo.init` method:
```python
import arx

repo = arx.Repo.init(HOST:PATH, '/path/to/my_repo')
```

You can then use the `checkout`, `commit`, and `list` methods:
```python
repo = arx.Repo('/path/to/my_repo')
for f in repo.list(remote=True):
    print(f)
repo.checkout('file1')
repo.commit('file2')
for f in repo.list():
    print(f)
```
