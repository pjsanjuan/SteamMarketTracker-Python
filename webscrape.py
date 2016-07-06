from lxml import html
import requests
import PIL.Image
import PIL.ImageTk
import tkinter
from io import BytesIO
import csv
#######################################################################################################
# root = tkinter.Tk()
api_key = '7C28D264D4A05EB3ED84423B00F0F392'
base_profile_URL = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=7C28D264D4A05EB3ED84423B00F0F392&steamids='
steamTax = 1.15
# 76561198033724063
# baseURL string. DO NOT MODIFY
baseURL = 'http://steamcommunity.com/market/priceoverview/?currency=13&appid=730&market_hash_name='
class ProfileSearch:
    def __init__(self):
        self.root = tkinter.Toplevel()
        # self.search_param = tkinter.StringVar()
        self.profile_arg = tkinter.IntVar()
        self.profile_button = tkinter.Button(self.root, text="Enter 64bit Steam ID", command = self.GotoProfile).grid(row=0, column=0)
        self.profile_entry = tkinter.Entry(self.root, textvariable=self.profile_arg).grid(row=0, column=2)
        self.root.mainloop()

    def GotoProfile(self):
        self.profile_id = str(self.profile_arg.get())
        if(len(self.profile_id) != 17):
            top = tkinter.Toplevel()
            top.title("Error")

            msg = tkinter.Message(top, text="Invalid Profile ID")
            msg.pack()

            button = tkinter.Button(top, text="Dismiss", command=top.destroy)
            button.pack()
            return
        self.profile_URL = base_profile_URL+self.profile_id
        # print(self.profile_URL)
        try:
            self.page = requests.get(self.profile_URL)
            self.page.raise_for_status()
            # print(self.page)
            y = ProfileDisplay(self.page)
        except requests.HTTPError:
            print('Profile URL Not Found')


class ProfileDisplay:
    def __init__(self, page):
        self.root = tkinter.Toplevel()
        self.page = page
        self.page_dict = self.page.json()
        # Check to see if player proile exists based on the 64 bit ID number
        if len(self.page_dict['response']['players']) == 0:
            top = tkinter.Toplevel()
            top.title("Error")

            msg = tkinter.Message(top, text="Player not found")
            msg.pack()

            button = tkinter.Button(top, text="Dismiss", command=top.destroy)
            button.pack()
            self.root.destroy()
            return
        # at this point the player profile DOES exist.
        self.page_dict_list = self.page_dict['response']['players'][0]
        if self.page_dict_list['personastate'] == 1:
            self.online_status = 'Online'
        # Display profile image ----------------------------------------------
        self.r = requests.get(self.page_dict_list['avatarfull'])
        self.img = PIL.Image.open(BytesIO(self.r.content))
        self.img = self.img.resize((150, 150), PIL.Image.ANTIALIAS)
        self.photo = PIL.ImageTk.PhotoImage(self.img)
        self.img_label = tkinter.Label(self.root, image=self.photo)
        self.img_label.pack()


        self.text = (
            'Name: ' + self.page_dict_list['personaname'] + '\n' +
            'Profile URL: ' + self.page_dict_list['profileurl'] + '\n' +
            'Online Status: ' + self.online_status
        )
        self.text_label = tkinter.Label(self.root,text = self.text).pack()
        self.root.mainloop()

# Must take in link as argument.
# Optional arguments: item name and purchase price (string)
class Weapon:
    def __init__(self, link_p,*args):
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
        self.root = tkinter.Toplevel()
        # Need 3 StringVar/IntVar
        self.link_arg = tkinter.StringVar()
        self.name_arg = tkinter.StringVar()
        self.price_arg= tkinter.IntVar()
        # Need 3 Entry Fields
        self.link_entry = tkinter.Entry(self.root, textvariable=self.link_arg).grid(row=2, column=3)
        self.name_entry = tkinter.Entry(self.root, textvariable=self.name_arg).grid(row=1, column=3)
        self.price_entry= tkinter.Entry(self.root, textvariable=self.price_arg).grid(row=3, column=3)
        #Need 3 Labels for Text for Entry
        self.name_label = tkinter.Label(self.root,text="Name: ").grid(row=1,column=2)
        self.link_label = tkinter.Label(self.root, text="Link: ").grid(row=2, column=2)
        self.price_label= tkinter.Label(self.root, text="Price: ").grid(row=3, column=2)

        # Button to add entries to market_store.txt
        self.add_button = tkinter.Button(self.root,text="Add to List",command=self.AddToList).grid(row=4,column=4)
        self.root.mainloop()

    def AddToList(self):
        self.temp1 = self.link_arg.get()
        #test if link entered is a valid connection
        try:
            self.r = requests.get(self.temp1)
            # raise signal if not a valid link
            self.r.raise_for_status()
            self.temp2 = self.name_arg.get()
            self.temp3 = str(self.price_arg.get())
            with open('market_store.txt','a') as f:
                f.write(self.temp1 + ',' + self.temp2 + ',' + self.temp3)
            self.root.destroy()
        except requests.HTTPError:
            print("Error - Cannot Access Link. Please  make sure Link is valid or if Steam is down")
            self.error_popup = tkinter.Toplevel()
            self.error_popup.title('Error')
            self.error__label = tkinter.Label(self.error_popup, text='Cannot Access Link. Please  make sure Link is valid or if Steam is down')
            self.error_popup.after(3000, self.error_popup.destroy)
            self.error_popup.mainloop()


# Takes in a list of Weapon objects.
class SteamScraperApp:
    def __init__(self, list_of_items_p):
        self.list_of_items = list_of_items_p
        self.l_arr = []
        self.row_counter = 0
        self.column = 0
        self.root = tkinter.Tk()

    def refresh(self):
        self.row_counter = 0
        self.column = 0
        self.price_label.grid_forget()
        self.list_items()

    def open_profile(self):
        x = ProfileSearch()

    def open_item_adder(self):
        z = AddItem()

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
                "Name: " + item.name + '\n' +
                "Purchase Price: " + item.purchase_price + '\n' +
                "Median Price: " + json_dict[u'median_price'] + '\n' +
                "Lowest Price: " + json_dict[u'lowest_price'] + '\n' +
                "Break Even: " + break_even_price + '\n' +
                "15c Profit: " + fifteen_cent + '\n' +
                "20c Profit: " + twenty_cent + '\n' +
                "25c Profit: " + twenty_five_cent + '\n' +
                "30c Profit: " + thrity_cent + '\n' +
                "--------------------------------------------------\n"
            )
            self.price_label = tkinter.Label(self.root, text=text_to_display)
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
            img_label = tkinter.Label(self.root, image=photo)
            img_label.grid(row=self.row_counter, column=2)
            self.l_arr.append(photo)

            # Increment row for formatting purposes
            self.row_counter += 1

        refresh_button = tkinter.Button(self.root, text="Refresh",command = self.refresh).place(x=0,y=0)
        profile_button = tkinter.Button(self.root, text="Profile", command=self.open_profile).place(x=300 ,y=0)
        add__to_button = tkinter.Button(self.root,text="Add Item to Inspection List",command=self.open_item_adder).place(x=150,y=0)
        self.root.mainloop()

# item1 = Weapon('http://steamcommunity.com/market/listings/730/AK-47%20%7C%20Redline%20(Field-Tested)','AK-47 | Redline (Field Tested)','5.75')
# item2 = Weapon('http://steamcommunity.com/market/listings/730/AWP%20%7C%20Worm%20God%20(Minimal%20Wear)','AWP | Worm God (Minimal Wear)','0.83')
# item3 = Weapon('http://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Blood%20Tiger%20%28Minimal%20Wear%29','M4A1-S | Blood Tiger (Minimal Wear)','1.68')
# item4 = Weapon('http://steamcommunity.com/market/listings/730/M4A4%20%7C%20Griffin%20%28Minimal%20Wear%29','M4A4 | Griffin (Minimal Wear)','1.53')
#
# l_o_i = []
# l_o_i.append(item1)
# l_o_i.append(item2)
# l_o_i.append(item3)
# l_o_i.append(item4)
#
# print(l_o_i)
#
# x = SteamScraperApp(l_o_i)
# x.list_items()

l_o_i_read= []

with open('market_store.txt') as csv_file:
    read_csv = csv.reader(csv_file,delimiter=',')
    print(read_csv)
    for row in read_csv:
        l_o_i_read.append(Weapon(row[0],row[1],row[2]))

print(l_o_i_read)
x = SteamScraperApp(l_o_i_read)
x.list_items()
# csv_file.close()
# Terminate program

