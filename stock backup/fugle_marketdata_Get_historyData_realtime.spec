# -*- mode: python -*-

block_cipher = None


a = Analysis(['fugle_marketdata_Get_historyData_realtime.py'],
             pathex=['D:\\model Data\\Code\\Fugle_Trade'],
             binaries=[],
             datas=[],
             hiddenimports=['fugle_marketdata'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='fugle_marketdata_Get_historyData_realtime',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='fugle_marketdata_Get_historyData_realtime')
