import os, sys
from pathlib import Path
_marker = Path(os.environ['CRISP_ACCESS_LOG'])
with _marker.open('a') as f: f.write('guard enabled pid=%s\n' % os.getpid())
def _guard(event, args):
    if event in ('open', 'os.listdir', 'os.scandir') and args and isinstance(args[0], (str, bytes, os.PathLike)):
        path = os.path.realpath(os.fsdecode(args[0]))
        if path == '/Users/yehaoming' or path.startswith('/Users/yehaoming/'):
            with _marker.open('a') as f: f.write('BLOCKED external user path: %s\n' % path)
            raise PermissionError('Clean reproduction forbids original user/workspace files')
sys.addaudithook(_guard)
