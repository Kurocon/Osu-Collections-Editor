# -*- mode: python -*-
import os
from glob import glob

print("#################################")
print("# Building OsuCollectionsEditor #")
print("#################################")

block_cipher = None

# Add staticfiles to build
static_files = [
  ('logging.conf', '.'),
  ('icons', 'icons')
]


# Build the exe with libraries

print("")
print("Building OCE with separate libraries")
print("####################################")
print("")
print("Analysing...")
print("")

a = Analysis(['oce.py'],
             pathex=[SPECPATH],
             binaries=static_files,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

print("")
print("Archiving")
print("")

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

print("")
print("Compiling executable")
print("")

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='oce',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='\icons\oce.ico' )

print("")
print("Collecting libraries")
print("")

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='oce')


# Build the portable exe

print("")
print("Building OCE portable (with included libraries)")
print("###############################################")
print("")
print("Analysing")
print("")

a = Analysis(['oce.py'],
             pathex=[SPECPATH],
             binaries=static_files,
             datas=static_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

print("")
print("Archiving")
print("")

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

print("")
print("Building executable")
print("")

portable_exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='oce_p',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='\icons\oce.ico' )

print("")
print("Collecting static files")
print("")

# Copy static files to portable dir
a.datas += [('logging.conf', 'logging.conf', 'DATA')]
for i in glob(os.path.join('icons', '*')):
  a.datas += [(i, i, 'DATA')]

portable_coll = COLLECT(portable_exe,
a.datas,
strip=False,
upx=True,
name="oce_portable"
)

print("")
print("Cleaning up")
print("")

# Remove portable executable on linux
if os.path.isfile(os.path.join(DISTPATH, "oce_p")):
    try:
        os.remove(os.path.join(DISTPATH, "oce_p"))
    except OSError:
        pass

# Remove portable executable on windows
if os.path.isfile(os.path.join(DISTPATH, "oce_p.exe")):
    try:
        os.remove(os.path.join(DISTPATH, "oce_p.exe"))
    except OSError:
        pass

# Rename the exe in the portable dir on Linux
if os.path.isfile(os.path.join(DISTPATH, "oce_portable", "oce_p")):
    try:
        os.rename(os.path.join(DISTPATH, "oce_portable", "oce_p"), os.path.join(DISTPATH, "oce_portable", "oce"))
    except WindowsError:
        os.remove(os.path.join(DISTPATH, "oce_portable", "oce"))
        os.rename(os.path.join(DISTPATH, "oce_portable", "oce_p"), os.path.join(DISTPATH, "oce_portable", "oce"))

# Rename the exe in the portable dir on Windows
if os.path.isfile(os.path.join(DISTPATH, "oce_portable", "oce_p.exe")):
    try:
        os.rename(os.path.join(DISTPATH, "oce_portable", "oce_p.exe"), os.path.join(DISTPATH, "oce_portable", "oce.exe"))
    except WindowsError:
        os.remove(os.path.join(DISTPATH, "oce_portable", "oce.exe"))
        os.rename(os.path.join(DISTPATH, "oce_portable", "oce_p.exe"), os.path.join(DISTPATH, "oce_portable", "oce.exe"))
