#!/usr/bin/env python3
"""Restore configuration saved by install.py; keep input schemes intact."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--no-restart', action='store_true')
args = parser.parse_args()

state = Path(os.environ.get('XDG_STATE_HOME', Path.home()/'.local/state'))/'fcitx5-mellow-blue'
backup = state/'backup.json'
if not backup.exists():
    raise SystemExit('No Mellow Blue installation backup found.')
saved = json.loads(backup.read_text())
for name, value in saved.items():
    if name == 'theme_existed':
        continue
    p = Path(name)
    if value is None:
        p.unlink(missing_ok=True)
    else:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(value)
data = Path(os.environ.get('XDG_DATA_HOME', Path.home()/'.local/share'))
theme = data/'fcitx5/themes/mellow-blue'
if theme.exists():
    shutil.rmtree(theme)
if saved['theme_existed']:
    shutil.copytree(state/'theme.before', theme)
backup.unlink()
if (state/'theme.before').exists():
    shutil.rmtree(state/'theme.before')
if not args.no_restart:
    subprocess.run(['fcitx5-remote', '-r'], check=True)
    subprocess.run(['fcitx5', '-r', '-d'], check=True)
print('Restored previous configuration.')
