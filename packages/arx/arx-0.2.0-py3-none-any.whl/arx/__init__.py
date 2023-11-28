import os
import stat
import logging
import subprocess
from pathlib import Path

import yaml

__version__ = '?.?.?'
try:
    from .__version__ import version as __version__
except ModuleNotFoundError:
    try:
        import setuptools_scm
        __version__ = setuptools_scm.get_version(fallback_version='?.?.?')
    except ModuleNotFoundError:
        pass
    # FIXME: fallback_version is not available in the buster version
    # (3.2.0-1)
    except TypeError:
        __version__ = setuptools_scm.get_version()
    except LookupError:
        pass

########################################

PROG = 'arx'

########################################

class ArxError(Exception):
    """An arx command exception"""
    pass


########################################

def _find_files(*paths, remote=None, depth=None):
    """list all files in the specified paths

    If remote is specified the command is executed on the specified
    remote host over ssh.

    If `depth` is a positive integer, the depth of the listing will be
    limited to the number of directories specified in the number.

    Returns a tuple of (files, errors), where errors is the error
    string if any errors are encountered.

    """
    # FIXME: rsync has a --list-only option that may be useful instead
    # of find?
    cmd = []
    if remote:
        cmd += [
            'ssh', '-T', remote,
        ]
    cmd += [
        'find',
        # follow symbolic links on the command line
        '-H',
    ]
    cmd += list(map(str, paths))
    # if not using the depth option filter for onlye files
    if depth is None:
        cmd += [
            # find only files
            '-type', 'f',
        ]
    if depth is not None:
        if not isinstance(depth, int):
            raise ArxError("list depth must be an int greater than 0")
        cmd += ['-maxdepth', str(int(depth))]
    logging.debug(' '.join(cmd))
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    files = []
    errors = None
    while True:
        line = proc.stdout.readline().strip()
        if not line:
            break
        # skip hidden files
        if '/.' in line:
            continue
        files.append(Path(line))
    proc.stdout.close()
    ret = proc.wait()
    # FIXME: should we throw a different kind of error here?
    if remote and ret == 255:
        raise ArxError(proc.stderr.read().strip())
    if ret != 0:
        errors = proc.stderr.read().strip()
    logging.debug(f"errors: {errors}")
    return files, errors


def _read_only(path):
    """remove write permission from path"""
    cur = stat.S_IMODE(path.stat().st_mode)
    # ugo-w
    path.chmod(cur & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)

########################################

class RSync:
    """rsync process context manager

    Used for transfering files from src to dst.  Use the `add` method
    of the returned Rsync object to add file paths to transfer.

    """
    def __init__(self, src, dst):
        self.cmd = [
            'rsync',
            '--verbose',
            '--compress',
            '--progress',
            '--ignore-existing',
            '--files-from=-',
            '--recursive',
            '--chmod=F-w',
            str(src),
            str(dst),
        ]
        logging.debug(' '.join(self.cmd))

    def __enter__(self):
        self.proc = subprocess.Popen(
            self.cmd,
            stdin=subprocess.PIPE,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
            text=True,
        )
        return self

    def add(self, path):
        logging.debug(f"  rsync: {path}")
        self.proc.stdin.write(str(path) + '\n')

    def __exit__(self, etype, value, traceback):
        self.proc.stdin.close()
        ret = self.proc.wait()
        # FIXME: this should be a connection error, should we throw a
        # different kind of error here?
        if ret == 255:
            raise ArxError(self.proc.stderr.read().strip())
        elif ret != 0:
            raise RuntimeError(self.proc.stderr.read().strip())

########################################

class Remote:
    """class representing an archive remote, accessible via SSH

    """
    def __init__(self, remote):
        """initialize remote

        The `remote` argument should be of the form:

        path
        :path
        [user@]host:path
        [user@]host:

        If the path is not specified it is assumed to be '.'.

        """
        hostpath = remote.split(':')
        if len(hostpath) == 1:
            host = ''
            path = hostpath[0]
        else:
            host, path = hostpath
        if path == '':
            path = '.'
        self.host = host
        self.path = Path(path)
        logging.debug(self)

    @property
    def remote(self):
        if self.host:
            return f'{self.host}:{self.path}'
        else:
            return f'{self.path}'

    def __str__(self):
        return '<Remote {}>'.format(self.remote)

    def test(self):
        """test validity of remote

        Will raise ArxError if the remote is not configured correctly.
        Will also resolve the remote path to be absolute.

        """
        if self.host:
            cmd = ['ssh', '-T', self.host]
        else:
            cmd = ['sh', '-c']
        cmd += [f'cd {self.path} && pwd']
        logging.debug("remote command: " + ' '.join(cmd))
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        stdout, stderr = proc.communicate()
        if proc.returncode == 255:
            raise ArxError(f"Could not connect to remote '{self.host}'.")
        elif proc.returncode == 1:
            raise ArxError(f"Remote path '{self.path}' not found.  Please check remote configuration and try again.")
        elif proc.returncode != 0:
            err = str(stderr).strip()
            raise ArxError(f"Unknown ssh connection error, return code {proc.returncode}: {err}")
        self.path = Path(stdout.strip())

########################################

class Repo:
    """class representing a local version of a remote archive

    """
    CDIR = f'.{PROG}'

    def __init__(self, path):
        """initialize repo at path

        Config file will be loaded and remote will be extracted.

        """
        self.root = Path(path).resolve()
        cfile = self.root.joinpath(self.CDIR, 'config')
        with open(cfile) as f:
            self.config = yaml.safe_load(f)
        logging.debug(self)
        self.remote = Remote(self.config['remote'])

    def __str__(self):
        return '<Repo {}>'.format(self.root)

    @classmethod
    def init(cls, remote, path, force=False):
        """initialize a repository at path for remote

        The `remote` argument should be of the form:

        [user@]host[:path]

        If `force` is True the repo will be initialized even if a repo
        has already been initialized for the path.

        """
        cpath = Path(path).joinpath(cls.CDIR)
        if cpath.exists() and not force:
            raise ArxError(f"Repo path already initialized: {cpath}")
        # configure and test the remote
        remote = Remote(remote)
        remote.test()
        # make config directory
        try:
            cpath.mkdir(parents=True)
        except FileExistsError:
            pass
        # write config file
        with open(cpath.joinpath('config'), 'w') as f:
            f.write(yaml.dump({
                'remote': remote.remote,
            }))
        logging.info(f"initialized {PROG} repo at {cpath}")
        return cls(path)

    @classmethod
    def find(cls, path=None):
        """find the repo for a given path

        """
        if not path:
            path = Path(os.getcwd())
        for root in [path] + list(path.parents):
            logging.debug(f"checking {root}...")
            if root.joinpath(cls.CDIR).exists():
                break
        else:
            raise ArxError(f"Directory '{path}' does not appear to be a {PROG} repo (sub)directory. Try running 'init' first.")
        return cls(root)

    ##########

    def _resolve_path(self, path):
        """resolve path relative to repo root

        """
        try:
            return Path(path).relative_to(self.root)
        except ValueError:
            return Path(path)

    def commit(self, *paths):
        """commit paths to the archive

        Any file paths that already exist in the archive will not be
        committed, and a warning will be issued.

        """
        # find all files and check that they exist (will throw an
        # ArxError if not)
        files, errors = _find_files(*paths)
        if errors:
            raise ArxError("The following errors were encountered:\n"+errors)
        files = [f.relative_to(self.root) for f in files]
        try:
            with RSync(self.root, self.remote.remote) as rs:
                for path in files:
                    rs.add(path)
        except subprocess.CalledProcessError:
            raise ArxError("Failed to transfer some paths to archive.")
        # FIXME: make this configurable
        # lock all local files committed to the remote
        # for f in files:
        #     _read_only(f)

    def checkout(self, *paths):
        """checkout paths from the archive

        Files are copied into the local directory from the remote
        repo.

        """
        paths = [self._resolve_path(path) for path in paths]
        try:
            with RSync(self.remote.remote, self.root) as rs:
                for path in paths:
                    rs.add(path)
        except subprocess.CalledProcessError:
            raise ArxError("Failed to retrieve some paths from archive.")

    def list(self, *paths, remote=False, depth=None):
        """list of files in the repo

        If `remote` is True files on the remote will be listed.

        If `depth` is a positive integer, the depth of the listing
        will be limited to the number of directories specified in the
        number.

        Returns a tuple of (files, errors) where `file` is the list of
        files and `errors` is any encountered errors.

        """
        if remote:
            root = self.remote.path
            remote = self.remote.host
        else:
            root = self.root
            remote = None
        if paths:
            # resolve all paths to be relative to the root paths,
            # which should be absolute
            paths = [root.joinpath(self._resolve_path(path)) for path in paths]
        else:
            paths = [root]
        files, errors = _find_files(*paths, remote=remote, depth=depth)
        files = [f.relative_to(root) for f in files]
        return files, errors
