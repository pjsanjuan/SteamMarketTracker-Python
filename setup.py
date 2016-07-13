import cx_Freeze
import sys


executables = [cx_Freeze.Executable('webscrape.py', base='Win32GUI')]

cx_Freeze.setup(
    name = 'SteamApp',
    
    options=
    {
        'build_exe': {
            'packages':['Tkinter','lxml.etree','lxml','gzip'],
            'include_files':['icon.png','market_store.txt'],
            'excludes': ['collections.abc']
        }
    },
    
    version = '0.01',
    executables = executables
)