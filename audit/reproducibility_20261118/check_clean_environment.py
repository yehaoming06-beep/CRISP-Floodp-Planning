#!/usr/bin/env python3
"""Attempt the declared pinned dependencies in an isolated temporary venv."""
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]


def main():
    target = Path(tempfile.mkdtemp(prefix='crisp-repro-20261118-'))
    result = {'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
              'original_pyvenv_cfg': Path(sys.prefix, 'pyvenv.cfg').read_text(),
              'existing_versions': {name: importlib.metadata.version(name) for name in
                  ('numpy','pandas','scipy','scikit-learn','gurobipy','openpyxl','pytest')},
              'fresh_environment': str(target), 'system_site_packages_requested': False,
              'requirements': str(ROOT / 'requirements.txt')}
    subprocess.run([sys.executable, '-m', 'venv', str(target)], check=True)
    command = [str(target/'bin/python'), '-m', 'pip', 'install', '--disable-pip-version-check',
               '--retries', '0', '--timeout', '30', '-r', str(ROOT/'requirements.txt')]
    result['command'] = command
    with (OUT/'clean_environment_install.txt').open('w') as log:
        answer = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                env={**os.environ, 'PIP_NO_INPUT':'1'})
    result['install_exit_code'] = answer.returncode
    result['status'] = 'PASS_INSTALL' if answer.returncode==0 else 'BLOCKED'
    result['scope'] = 'Fresh dependency installation attempt only; numerical reruns otherwise use the original working environment.'
    if answer.returncode==0:
        result['pip_check'] = subprocess.run([str(target/'bin/python'), '-m','pip','check'],
                                            capture_output=True,text=True).stdout.strip()
    (OUT/'environment.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
