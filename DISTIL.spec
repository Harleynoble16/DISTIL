# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['distil_gui.py'],
    pathex=[],
    binaries=[],
datas=[
    ("sounds/jarvis_online.mp3", "sounds"),
    ("haarcascade_frontalface_default.xml", "."),
],
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
    [],
    exclude_binaries=True,
    name='DISTIL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DISTIL',
)
app = BUNDLE(
    coll,
    name='DISTIL.app',
    icon='distil.icns',
    bundle_identifier='com.harley.distil',
    info_plist={
        "NSCameraUsageDescription": "DISTIL uses the camera for eye tracking."
    },
)
