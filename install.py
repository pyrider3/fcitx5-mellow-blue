#!/usr/bin/env python3
"""Install the theme, optionally enable the locally built animation addon."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--animation', action='store_true')
parser.add_argument('--no-restart', action='store_true')
args = parser.parse_args()
data = Path(os.environ.get('XDG_DATA_HOME', Path.home()/'.local/share'))
config = Path(os.environ.get('XDG_CONFIG_HOME', Path.home()/'.config'))
state = Path(os.environ.get('XDG_STATE_HOME', Path.home()/'.local/state'))/'fcitx5-mellow-blue'
theme = data/'fcitx5/themes/mellow-blue'
classic = config/'fcitx5/conf/classicui.conf'
addon = data/'fcitx5/addon/smoothui.conf'
if args.animation:
    version = subprocess.check_output(['fcitx5', '--version'], text=True)
    if not re.search(r'\b5\.1\.23\b', version):
        raise SystemExit('Animation build targets Fcitx5 5.1.23. Install theme without --animation on other versions.')
    if not (root/'libsmoothui.so').is_file():
        raise SystemExit('Run python3 build.py before installing animation.')
state.mkdir(parents=True, exist_ok=True)
backup = state/'backup.json'
saved = json.loads(backup.read_text()) if backup.exists() else {}
for path in [classic] + ([addon] if args.animation else []):
    if str(path) not in saved:
        saved[str(path)] = path.read_text() if path.exists() else None
if 'theme_existed' not in saved:
    saved['theme_existed'] = theme.exists()
    if theme.exists():
        shutil.copytree(theme, state/'theme.before')
backup.write_text(json.dumps(saved, ensure_ascii=False, indent=2))
shutil.copytree(root/'themes/mellow-blue', theme, dirs_exist_ok=True)
classic.parent.mkdir(parents=True, exist_ok=True)
text = classic.read_text() if classic.exists() else ''
for key, value in [('Theme', 'mellow-blue'), ('DarkTheme', 'mellow-blue'), ('UseAccentColor', 'False')]:
    pattern = rf'(?m)^{key}=.*$'
    text = re.sub(pattern, f'{key}={value}', text) if re.search(pattern, text) else text.rstrip()+f'\n{key}={value}\n'
classic.write_text(text)
if args.animation:
    base = data/'fcitx5-smoothui'
    base.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root/'libsmoothui.so', base/'libsmoothui.next.so')
    (base/'libsmoothui.next.so').replace(base/'libsmoothui.so')
    addon.parent.mkdir(parents=True, exist_ok=True)
    addon.write_text(f'''[Addon]
Name=Mellow Blue Animation
Name[zh_CN]=Mellow Blue 动画
Type=SharedLibrary
Library={base}/libsmoothui
Category=UI
Version=1.0.0
UIPriority=150
OnDemand=True
Configurable=True

[Addon/Dependencies]
0=core:5.1.23

[Addon/OptionalDependencies]
0=xcb
1=wayland
2=notificationitem
3=dbus
4=waylandim
''')
if not args.no_restart:
    subprocess.run(['fcitx5-remote', '-r'], check=True)
    if args.animation:
        subprocess.run(['fcitx5', '-r', '-d'], check=True)
print('Installed Mellow Blue. Backup:', backup)
