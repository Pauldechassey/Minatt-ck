# minattack.spec

from PyInstaller.utils.hooks import collect_submodules
from pathlib import Path

# Collect dynamically imported modules
backend_modules = collect_submodules('minattack.backend')
shared_modules = collect_submodules('minattack.shared')

block_cipher = None

datas = [
    ('.env', '.'),
    ('minattack/backend/app/database/schema.sql', 'minattack/backend/app/database'),
    ('minattack/backend/app/database/init.sql', 'minattack/backend/app/database'),
    ('minattack/backend/app/database/data_dump.sql', 'minattack/backend/app/database'),
]

a = Analysis(
    ['minattack/frontend/main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'uvicorn',
        'PySide6',
        *backend_modules,
        *shared_modules,
        'sklearn.externals.array_api_compat.numpy.fft',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='minattack',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True
)

#coll = COLLECT(
#    exe,
#    a.binaries,
#    a.zipfiles,
#    a.datas,
#    strip=False,
#    upx=True,
#    upx_exclude=[],
#    name='minattack'
#)
