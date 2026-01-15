# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for TaskTimestamp

import os

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),  # dataフォルダを含める
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TaskTimestamp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # UPX無効化（Windows Defender誤検知対策）
    console=False,  # コンソール非表示（GUIアプリ）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,  # UPX無効化
    upx_exclude=[],
    name='TaskTimestamp',
)
