#!/usr/bin/env python3
"""Rebuild against the pinned Fcitx5 source without installing system packages."""
from pathlib import Path
import subprocess, shutil, shlex
root=Path(__file__).resolve().parent
scratch=root/'.build'
scratch.mkdir(parents=True,exist_ok=True)
def run(args,cwd=None): subprocess.run([str(x) for x in args],cwd=cwd,check=True)
def clone(url,path):
    if not path.exists(): run(['git','clone','--depth','1',url,path])
prefix=scratch/'deps'
clone('https://github.com/KDE/extra-cmake-modules.git',scratch/'ecm')
run(['cmake','-S',scratch/'ecm','-B',scratch/'ecm-build','-DBUILD_TESTING=OFF','-DBUILD_DOC=OFF',f'-DCMAKE_INSTALL_PREFIX={prefix}'])
run(['cmake','--install',scratch/'ecm-build'])
clone('https://github.com/nlohmann/json.git',scratch/'json')
run(['cmake','-S',scratch/'json','-B',scratch/'json-build','-DJSON_BuildTests=OFF',f'-DCMAKE_INSTALL_PREFIX={prefix}'])
run(['cmake','--install',scratch/'json-build'])
source=scratch/'fcitx5'
if not source.exists():
    run(['git','clone','--depth','1','--branch','5.1.23','https://github.com/fcitx/fcitx5.git',source])
    run(['git','submodule','update','--init','--depth','1','third_party/yoga'],source)
if 'FCITX_ADDON_FACTORY_V2(smoothui,' not in (source/'src/ui/classic/classicui.cpp').read_text():
    run(['git','apply',root/'src/fcitx5.patch'],source)
shutil.copy2(root/'src/motion.h',source/'src/ui/classic/motion.h')
build=scratch/'build'
run(['cmake','-S',source,'-B',build,f'-DCMAKE_PREFIX_PATH={prefix}','-DENABLE_TEST=OFF','-DENABLE_TESTING_ADDONS=OFF','-DENABLE_ENCHANT=OFF','-DENABLE_DOC=OFF','-DUSE_SYSTEM_PLASMA_WAYLAND_PROTOCOLS=OFF','-DBUILD_SPELL_DICT=OFF','-Wno-author'])
run(['cmake','--build',build,'--target','classicui','-j','4'])
# Link to installed Fcitx5 ABI at runtime, not to intermediate build libraries.
link=build/'src/ui/classic/CMakeFiles/classicui.dir/link.txt'
run([arg for arg in shlex.split(link.read_text()) if not arg.startswith('-Wl,-rpath,')],link.parent.parent.parent)
shutil.copy2(build/'bin/libclassicui.so',root/'libsmoothui.so')
print('Built '+str(root/'libsmoothui.so')+'. Run install.py to apply it.')
