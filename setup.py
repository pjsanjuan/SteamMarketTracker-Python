import cx_Freeze
import sys


executables = [cx_Freeze.Executable('webscrape.py', base='Win32GUI', icon='icon.ico')]

cx_Freeze.setup(
    name = 'SteamApp',
    
    options=
    {
        'build_exe': {
            'packages':['Tkinter','lxml.etree','lxml','gzip'],
            'include_files':['icon.png','market_sell.txt','market_buy.txt','settings.json'],
            'excludes': ['collections.abc']
        }
    },
    
    version = '0.01',
    executables = executables
)

# http://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20P250%20%7C%20Valence%20%28Field-Tested%29,Test,2.5
# http://steamcommunity.com/market/listings/730/AWP%20%7C%20Asiimov%20%28Field-Tested%29,AWP Asiimov FT,40.0
# http://steamcommunity.com/market/listings/730/Sticker%20%7C%20FaZe%20Clan%20%7C%20Cologne%202016,Faze Sticker,0.38

# global root
# if (root == None):
#     root = Tkinter.Tk()
#     self.root = root
#     print 'root is taken by' + str(self)
# else:
#     self.root = Tkinter.Toplevel()

# def root_owner_caller(self):
#     checkForRootOwnership(self.root)
#     self.root.destroy()

# self.root.protocol('WM_DELETE_WINDOW', self.root_owner_caller)