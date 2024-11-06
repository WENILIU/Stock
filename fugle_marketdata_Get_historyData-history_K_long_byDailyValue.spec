# -*- mode: python -*-

block_cipher = None


a = Analysis(['D:\\model Data\\Code\\Fugle_Trade\\fugle_marketdata_Get_historyData-history_K_long_byDailyValue.py'],
             pathex=['D:\\model Data\\Code\\Fugle_Trade'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          name='fugle_marketdata_Get_historyData-history_K_long_byDailyValue',
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
               name='fugle_marketdata_Get_historyData-history_K_long_byDailyValue')
