# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

datas_totales = [
    ('icono.ico', '.'),
]

a = Analysis(
    ['Principal.py'],
    pathex=['.'],
    binaries=[],
    datas=datas_totales,
    hiddenimports=[
        'pandas',
        'openpyxl',
        'sqlite3',
        'tkcalendar',
        'babel.numbers',
        'reportlab',
        'reportlab.pdfgen.canvas',
        'reportlab.lib.pagesizes',
        'reportlab.lib.colors',
        'urllib',
        'urllib.parse',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        # Notificaciones nativas y soporte del sistema
        'plyer',
        'plyer.platforms.win.notification',
        'win32api',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter.test',
        'unittest',
        'notebook', 
        'scipy', 
        'IPython', 
        'matplotlib', 
    ],
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
    name='Principal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icono.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Principal',
)