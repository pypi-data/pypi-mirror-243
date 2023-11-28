import os
import logging
import argparse
from pathlib import Path

from . import __version__, Repo, ArxError

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO').upper(),
    style='{',
    format='{levelname}: {message}',
)

##########

parser = argparse.ArgumentParser(
    description="""simple data archiving tool

A local directory, or "repo", is initialized (with the 'init' command)
to be stagging ground and mirror of a remote archive.  Files and
directories can be copied into the repo and then committed to the
remote archive (with the 'commit' command).  Files and directories in
the remote archive can be checked out from the archive for viewing and
processing (with the 'checkout' command).
""",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    '--version', action='version', version=__version__,
    help="print version and exit",
)
subparsers = parser.add_subparsers(
    metavar='COMMAND',
)

def _subcommand(func, **kwargs):
    name = func.__name__.split('_')[1]
    proc = subparsers.add_parser(
        name,
        help=func.__doc__.splitlines()[0],
        description=func.__doc__.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        **kwargs
    )
    proc.set_defaults(func=func)
    return proc

##########

def cmd_init(remote, path, force=False):
    """initialize repo for remote

    """
    Repo.init(remote, path, force=force)


sp = _subcommand(cmd_init)
sp.add_argument(
    'remote',
    help="remote host path (e.g. 'user@ssh.example.edu:archive')",
)
sp.add_argument(
    'path',
    help="directory to initialize into",
)
sp.add_argument(
    '--force', '-f', action='store_true',
    help="force initialization even if directory already initialized",
)

##########

def cmd_config():
    """dump the repo config

    """
    repo = Repo.find()
    print(f"root: {repo.root}")
    for key, val in repo.config.items():
        print(f"{key}: {val}")


sp = _subcommand(cmd_config, aliases=['conf'])

##########

def cmd_commit(paths):
    """commit paths to the archive

    Any file paths that already exist in the archive will not be
    committed, and a warning will be issued.

    """
    repo = Repo.find()
    cdir = Path(os.getcwd())
    repo.commit(*[cdir.joinpath(path) for path in paths])


sp = _subcommand(cmd_commit, aliases=['ci', 'push'])
sp.add_argument(
    'paths', nargs='+',
    help="paths to commit (recursively) to the archive",
)

##########

def cmd_checkout(paths):
    """checkout paths from the archive

    """
    repo = Repo.find()
    cdir = Path(os.getcwd())
    repo.checkout(*[cdir.joinpath(path) for path in paths])


sp = _subcommand(cmd_checkout, aliases=['co', 'pull'])
sp.add_argument(
    "paths", nargs='+',
    help="paths to checkout",
)

##########

def cmd_list(paths, local=None, remote=None, depth=None):
    """list archive files

    If --local or --remote is specified, the files are simply listed.
    If neither is specified, list both remote and local files with the
    following prefixes:
      '-' files exist on the remote only
      '+' files exist locally only

    """
    repo = Repo.find()
    cdir = Path(os.getcwd()).relative_to(repo.root)
    paths = [cdir.joinpath(path) for path in paths]
    lfiles = set()
    rfiles = set()
    error = None
    if local:
        lfiles, lerrors = repo.list(*paths, depth=depth)
        lfiles = set(lfiles)
    if remote:
        rfiles, rerrors = repo.list(*paths, remote=True, depth=depth)
        rfiles = set(rfiles)
    if local and remote:
        files = \
            [('  ', f) for f in lfiles & rfiles] + \
            [('- ', f) for f in rfiles - lfiles] + \
            [('+ ', f) for f in lfiles - rfiles]
    elif not local:
        files = [('', f) for f in rfiles]
        error = rerrors
    elif not remote:
        files = [('', f) for f in lfiles]
        error = lerrors

    for f in sorted(files, key=lambda f: f[1]):
        print(f'{f[0]}{f[1].relative_to(cdir)}')

    if error:
        msg = "The following errors were encountered:\n"
        msg += str(error)
        raise ArxError(msg)

    # for d in difflib.unified_diff(
    #         rfiles, lfiles,
    #         fromfile='remote',
    #         tofile='local',
    #         n=1000000000,
    #         lineterm='',
    # ):
    #     print(d)


sp = _subcommand(cmd_list, aliases=['ls'])
sp.add_argument(
    "paths", nargs='*', metavar='path', default='.',
    help="paths to list [default: '.']",
)
g = sp.add_mutually_exclusive_group()
g.add_argument(
    "--local", "-l", dest='remote', action='store_false',
    help="list local paths only",
)
g.add_argument(
    "--remote", "-r", dest='local', action='store_false',
    help="list remote paths only",
)
g.add_argument(
    "--depth", "-d", metavar='N', type=int,
    help="limit depth of listing to N levels",
)

##########

def cmd_help():
    """this help

    """
    parser.print_help()

sp = _subcommand(cmd_help)

########################################

def main():
    args = parser.parse_args()
    logging.debug(args)
    if 'func' not in args:
        parser.print_help()
        parser.exit()
    kwargs = dict(args._get_kwargs())
    del kwargs['func']
    try:
        args.func(**kwargs)
    except ArxError as e:
        raise SystemExit(f"Error: {e}")


if __name__ == '__main__':
    main()
