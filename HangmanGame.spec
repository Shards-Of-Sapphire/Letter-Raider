# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['hangman_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\shaik\\OneDrive\\Desktop\\Hangman v1.0\\Hangman v1.0\\hangman (Python)\\images', 'images/'), ('C:\\Users\\shaik\\OneDrive\\Desktop\\Hangman v1.0\\Hangman v1.0\\hangman (Python)\\words.csv', '.'), ('C:\\Users\\shaik\\OneDrive\\Desktop\\Hangman v1.0\\Hangman v1.0\\hangman (Python)\\fonts\\press_start_2p\\PressStart2P-Regular.ttf', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HangmanGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\shaik\\OneDrive\\Desktop\\Hangman v1.0\\Hangman v1.0\\hangman (Python)\\icon.ico'],
)
