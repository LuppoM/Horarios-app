# -*- mode: python ; coding: utf-8 -*-
import os
import subprocess

block_cipher = None

a = Analysis(
    ['lanzador.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HorariosGolosinas',
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
    icon=['icono.ico'],
)

# ==============================================================================
# PROCESO DE FIRMA AUTOMÁTICA POST-COMPILACIÓN
# ==============================================================================

exe_generado = os.path.join(DISTPATH, f'{exe.name}.exe')
NOMBRE_CERTIFICADO = 'mi_certificado.cer'
CERT_PATH = os.path.join(SPECPATH, NOMBRE_CERTIFICADO)
CERT_PASS = 'TuContraseña'  # Cambiá por tu contraseña si aplica
TIMESTAMP_URL = 'http://timestamp.digicert.com'

signtool_cmd = [
    'signtool',
    'sign',
    '/f',
    CERT_PATH,
    '/p',
    CERT_PASS,
    '/tr',
    TIMESTAMP_URL,
    '/td',
    'sha256',
    '/fd',
    'sha256',
    exe_generado,
]

if os.path.exists(exe_generado) and os.path.exists(CERT_PATH):
    try:
        print(f'\n[+] Firmando lanzador: {exe_generado}')
        subprocess.run(signtool_cmd, check=True)
        print('[✔] Lanzador firmado exitosamente.\n')
    except subprocess.CalledProcessError as e:
        print(f'[✘] Error durante la firma con signtool: {e}')
    except FileNotFoundError:
        print('[✘] Error: No se encontró "signtool.exe" en el PATH de Windows.')