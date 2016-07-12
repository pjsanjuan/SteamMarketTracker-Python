import wx
from lxml import html
import requests
import PIL.Image
import PIL.ImageTk
import Tkinter
from io import BytesIO
import webbrowser
import csv

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = 'icon.png'

api_key = '7C28D264D4A05EB3ED84423B00F0F392'
base_profile_URL = ('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
                    + '?key=7C28D264D4A05EB3ED84423B00F0F392&steamids=')
steamTax = 1.15
# 76561198033724063
# baseURL string. DO NOT MODIFY
baseURL = 'http://steamcommunity.com/market/priceoverview/?currency=13&appid=730&market_hash_name='
class ProfileSearch:
    def __init__(self):
        self.root = Tkinter.Toplevel()
        # self.search_param = Tkinter.StringVar()
        self.profile_arg = Tkinter.IntVar()
        self.profile_button = Tkinter.Button(self.root, text="Enter 64bit Steam ID", command = self.GotoProfile).grid(row=0, column=0)
        self.profile_entry = Tkinter.Entry(self.root, textvariable=self.profile_arg).grid(row=0, column=2)
        self.root.mainloop()

    def GotoProfile(self):
        profile_id = str(self.profile_arg.get())
        if(len(profile_id) != 17):
            top = Tkinter.Toplevel()
            top.title("Error")

            msg = Tkinter.Message(top, text="Invalid Profile ID")
            msg.pack()

            button = Tkinter.Button(top, text="Dismiss", command=top.destroy)
            button.pack()
            return
        profile_URL = base_profile_URL + profile_id
        # print(self.profile_URL)
        try:
            page = requests.get(profile_URL)
            page.raise_for_status()
            # print(self.page)
            y = ProfileDisplay(page)
        except requests.HTTPError:
            print('Profile URL Not Found')
class ProfileDisplay:
    def __init__(self, page):
        self.root = Tkinter.Toplevel()
        self.page = page
        self.page_dict = self.page.json()
        # Check to see if player proile exists based on the 64 bit ID number
        if len(self.page_dict['response']['players']) == 0:
            top = Tkinter.Toplevel()
            top.title("Error")

            msg = Tkinter.Message(top, text="Player not found")
            msg.pack()

            button = Tkinter.Button(top, text="Dismiss", command=top.destroy)
            button.pack()
            self.root.destroy()
            return
        # at this point the player profile DOES exist.
        self.page_dict_list = self.page_dict['response']['players'][0]
        if self.page_dict_list['personastate'] == 1:
            self.online_status = 'Online'
        else:
            self.online_status = 'Offline'
        # Display profile image ----------------------------------------------
        self.r = requests.get(self.page_dict_list['avatarfull'])
        self.img = PIL.Image.open(BytesIO(self.r.content))
        self.img = self.img.resize((150, 150), PIL.Image.ANTIALIAS)
        self.photo = PIL.ImageTk.PhotoImage(self.img)
        self.img_label = Tkinter.Label(self.root, image=self.photo)
        self.img_label.pack()


        self.text = (
            'Name: ' + self.page_dict_list['personaname'] + '\n' +
            'Profile URL: ' + self.page_dict_list['profileurl'] + '\n' +
            'Online Status: ' + self.online_status
        )
        self.text_label = Tkinter.Label(self.root,text = self.text).pack()
        self.root.mainloop()
class Weapon:
    def __init__(self, link_p, *args):
        self.url = link_p
        if(args[0] != None):
            self.name = args[0]
        else:
            self.name = 'No name provided'
        if(args[1] != None):
            self.purchase_price = args[1]
        else:
            self.purchase_price = '0'
class AddItem:
    def __init__(self):
        self.root = Tkinter.Toplevel()
        # Need 3 StringVar/IntVar
        self.link_arg = Tkinter.StringVar()
        self.name_arg = Tkinter.StringVar()
        self.price_arg= Tkinter.DoubleVar()
        # Need 3 Entry Fields
        self.link_entry = Tkinter.Entry(self.root, textvariable=self.link_arg).grid(row=2, column=3)
        self.name_entry = Tkinter.Entry(self.root, textvariable=self.name_arg).grid(row=1, column=3)
        self.price_entry= Tkinter.Entry(self.root, textvariable=self.price_arg).grid(row=3, column=3)
        #Need 3 Labels for Text for Entry
        self.name_label = Tkinter.Label(self.root,text="Name: ").grid(row=1,column=2)
        self.link_label = Tkinter.Label(self.root, text="Link: ").grid(row=2, column=2)
        self.price_label= Tkinter.Label(self.root, text="Price: ").grid(row=3, column=2)

        # Button to add entries to market_store.txt
        self.add_button = Tkinter.Button(self.root,text="Add to List",command=self.AddToList).grid(row=4,column=4)
        self.root.mainloop()

    def AddToList(self):
        temp1 = self.link_arg.get()
        # test if link entered is a valid connection
        try:
            r = requests.get(temp1)
            # raise signal if not a valid link
            r.raise_for_status()

        except requests.HTTPError:
            print("Error - Cannot Access Link. Please  make sure Link is valid or if Steam is down")
            error_popup = Tkinter.Toplevel()
            error_popup.title('Error')
            error__label = Tkinter.Label(error_popup, text='Cannot Access Link. Please  make sure Link is valid or if Steam is down')
            error_popup.after(3000, error_popup.destroy)
            error_popup.mainloop()
        temp2 = self.name_arg.get()
        temp3 = str(self.price_arg.get())

        # Check for duplicate links
        with open('market_store.txt','r') as csv_file:
            read_csv = csv.reader(csv_file, delimiter=',')
            line_counter = 0
            for row in read_csv:
                if row[0] == temp1:
                    print('Duplicate found at line ' + str(line_counter) + '.\n')
                    duplicate_popup = Tkinter.Toplevel()
                    duplicate_label = Tkinter.Label(duplicate_popup,text="Duplicate found at line " + str(line_counter + 1))
                    duplicate_label.pack()
                    duplicate_popup.title("Error - Duplicate Link Found")
                    duplicate_popup.mainloop()
                    return
                line_counter += 1
        # Did not find any duplicate links
        with open('market_store.txt', 'a') as f:
            f.write(temp1 + ',' + temp2 + ',' + temp3)
        self.root.destroy()
class Calculator:
    def __init__(self):
        self.root = Tkinter.Toplevel()
        self.root.title("Calculator")

        # Display entry box-----------------
        self.price_arg = Tkinter.DoubleVar()
        self.price_label = Tkinter.Label(self.root, text='Enter price')
        self.price_label.pack()
        self.price_entry = Tkinter.Entry(self.root, textvariable=self.price_arg)
        self.price_entry.pack()
        self.price_button = Tkinter.Button(self.root, text ="Calculate!",command=self.LaunchCalculation).pack()
        # Display info
        self.root.mainloop()

    def LaunchCalculation(self):
        self.calc_results_popup = Tkinter.Toplevel()
        # Get value (int)
        value = self.price_arg.get()
        print(value)
        break_even_value = value * steamTax
        fifteen_cent_profit = (value+0.15)*steamTax
        text_to_display = ('Break even value: ' + str(break_even_value) + '\n' +
                            '15c Profit: ' + str(fifteen_cent_profit) + '\n'
                           )
        self.text_label = Tkinter.Label(self.calc_results_popup,text=text_to_display).pack()

        self.calc_results_popup.mainloop()


    # Takes in a list of Weapon objects.
class SteamScraperApp:
    def __init__(self, list_of_items_p):
        self.list_of_items = list_of_items_p
        self.l_arr = []
        self.row_counter = 0
        self.column = 0
        self.root = Tkinter.Tk()
        self.list_items()

    def refresh(self):
        self.row_counter = 0
        self.column = 0
        self.price_label.grid_forget()
        self.list_items()

    # @staticmethod
    def open_profile(self):
        x = ProfileSearch()

    # @staticmethod
    def open_item_adder(self):
        z = AddItem()

    # @staticmethod
    def open_calculator(self):
        xy = Calculator()

    def open_steam_status(self):
        webbrowser.open('https://steamstat.us/',new=2)

    def list_items(self):
        for item in self.list_of_items:
            # Print the text Information ------------------------------------------------------------
            # Prices for profit
            break_even_price = str("%.2f" % (float(item.purchase_price) * steamTax))
            fifteen_cent = str("%.2f" % ((float(item.purchase_price) + 0.15) * steamTax))
            twenty_cent = str("%.2f" % ((float(item.purchase_price) + 0.20) * steamTax))
            twenty_five_cent = str("%.2f" % ((float(item.purchase_price) + 0.25) * steamTax))
            thrity_cent = str("%.2f" % ((float(item.purchase_price) + 0.30) * steamTax))
            # Split the url using '/' as the delimiter
            hash_name = item.url.split('/')

            # Generate the json URL for the item/weapon. Something along the lines of
            # http://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name=StatTrak%E2%84%A2%20P250%20%7C%20Steel%20Disruption%20%28Factory%20New%29
            request_url = baseURL + hash_name[-1]
            # Create json
            try:
                page = requests.get(request_url)
                # print("RequestURL:" + request_url)
                page.raise_for_status()
            except requests.HTTPError:
                print("Unable to make request for item" + item.name)
                continue

            json_dict = page.json()
            text_to_display = (
                "\n\nName: " + item.name + '\n' +
                "Purchase Price: " + item.purchase_price + '\n' +
                "Median Price: " + json_dict[u'median_price'] + '\n' +
                #"Lowest Price: " + json_dict[u'lowest_price'] + '\n' +
                "Break Even: " + break_even_price + '\n' +
                "15c Profit: " + fifteen_cent + '\n' +
                "20c Profit: " + twenty_cent + '\n' +
                "25c Profit: " + twenty_five_cent + '\n' +
                "30c Profit: " + thrity_cent + '\n' +
                "--------------------------------------------------\n"
            )
            self.price_label = Tkinter.Label(self.root, text=text_to_display)
            self.price_label.grid(row=self.row_counter, column=0)
            # Display the image -------------------------------------------------------------------------
            # Get img_url
            page = requests.get(item.url)
            tree = html.fromstring(page.content)
            # Grab image URL using Xpath
            img_url = tree.xpath('//*[@id="mainContents"]/div[2]/div/div[1]/img/@src')
            try:
                self.temp = img_url[0]
            except IndexError:
                print("img_url[0] == None:")
                print(item.url)
                continue
            # Display the image
            r = requests.get(img_url[0])
            img = PIL.Image.open(BytesIO(r.content))
            img = img.resize((150, 150), PIL.Image.ANTIALIAS)
            photo = PIL.ImageTk.PhotoImage(img)
            img_label = Tkinter.Label(self.root, image=photo)
            img_label.grid(row=self.row_counter, column=2)
            self.l_arr.append(photo)

            # Increment row for formatting purposes
            self.row_counter += 1

        refresh_button = Tkinter.Button(self.root, text="Refresh", command=self.refresh)
        refresh_button.place(x=0, y=0)

        profile_button = Tkinter.Button(self.root, text="Profile", command=self.open_profile)
        profile_button.place(x=350, y=0)
        add__to_button = Tkinter.Button(self.root, text="Add Item to List", command=self.open_item_adder)
        add__to_button.place(x=250, y=0)
        calc_button    = Tkinter.Button(self.root, text="Calculator", command=self.open_calculator)
        calc_button.place(x=170, y=0)
        service_stat_button = Tkinter.Button(self.root, text="Steam Service Stat", command=self.open_steam_status)
        service_stat_button.place(x=50, y=0)
        self.root.mainloop()

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Open', self.OpenWindow)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print 'Tray icon was left-clicked.'

    def on_hello(self, event):
        print 'Hello, world!'

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

    def OpenWindow(self, event):
        x = SteamScraperApp(l_o_i_read)

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    app = App(False)


    with open('market_store.txt') as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        print(read_csv)
        for row in read_csv:
            l_o_i_read.append(Weapon(row[0], row[1], row[2]))

    app.MainLoop()

l_o_i_read = []

if __name__ == '__main__':
    main()