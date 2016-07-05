from lxml import html
import requests
import PIL.Image
import PIL.ImageTk
import tkinter
from io import BytesIO
#ignore text
#######################################################################################################
# root = tkinter.Tk()
api_key = '7C28D264D4A05EB3ED84423B00F0F392'
steamTax = 1.15
# baseURL string. DO NOT MODIFY
baseURL = 'http://steamcommunity.com/market/priceoverview/?currency=13&appid=730&market_hash_name='
class Profile:
    def __init__(self):
        self.root = tkinter.Toplevel()
        self.root.title('Profile')
        # Print the information
        self.profile_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=7C28D264D4A05EB3ED84423B00F0F392&steamids=76561198033724063'
        self.page = requests.get(self.profile_url)
        self.page_json = self.page.json()
        self.list = self.page_json['response']['players'][0]

        print(self.list['avatar'])
        try:
            self.img = requests.get(self.list['avatarfull'])

        except requests.HTTPError:
            print("Cannot connect")

        # print(self.img.content)
        # Display the image--------------------------------------------------
        self.avatar = PIL.Image.open(BytesIO(self.img.content))
        self.avatar = self.avatar.resize((150, 150), PIL.Image.ANTIALIAS)
        self.photo = PIL.ImageTk.PhotoImage(self.avatar)
        self.avatar_label = tkinter.Label(self.root, image=self.photo)
        self.avatar_label.grid(row = 0, column = 0)
        # Display the text=----------------------------------------------------
        if self.list['personastate'] == 1:
            self.online_status = 'Online'

        # Display the text
        self.text_info = ('Name: ' + self.list['personaname'] + '\n' +
                          'Profile URL: ' + self.list['profileurl'] + '\n'+
                          'Online Status: ' + self.online_status
                          )

        self.text_label = tkinter.Label(self.root, text = self.text_info)
        self.text_label.grid(row=1, column=0)

        # img = PIL.Image.open(BytesIO(r.content))
        # img = img.resize((150, 150), PIL.Image.ANTIALIAS)
        # photo = PIL.ImageTk.PhotoImage(img)
        # img_label = tkinter.Label(self.root, image=photo)
        # img_label.grid(row=self.row_counter, column=2)

        # for i in self.list:
        #     print(i,self.list[i])



        # Display Name
        self.root.mainloop()
class Weapon:
    def __init__(self,name_p,link_p,purchase_price_p):
        self.name = name_p
        self.url = link_p
        self.purchase_price = purchase_price_p

class SteamScraperApp:
    def __init__(self,list_of_items_p):
        self.list_of_items = list_of_items_p
        self.l_arr = []
        # self.p_arr = []
        self.row_counter = 0
        self.column = 0
        self.root = tkinter.Tk()
        # self.price_label
        # self.root.mainloop()

    def refresh(self):
        self.row_counter = 0
        self.column = 0
        self.price_label.grid_forget()
        self.list_items()

    def open_profile(self):
        x = Profile()


    def list_items(self):

        for item in self.list_of_items:
            # Print the text Information ------------------------------------------------------------
            break_even_price = str( "%.2f" % (float(item.purchase_price) * steamTax))
            fifteen_cent = str( "%.2f" % ((float(item.purchase_price) + 0.15) * steamTax))
            twenty_cent = str("%.2f" % ((float(item.purchase_price) + 0.20) * steamTax))
            twenty_five_cent = str("%.2f" % ((float(item.purchase_price) + 0.25) * steamTax))
            thrity_cent = str("%.2f" % ((float(item.purchase_price) + 0.30) * steamTax))

            hash_name = item.url.split('/')


            request_URL = baseURL + hash_name[-1]
            # print(request_URL)
            # Create json
            try:
                page = requests.get(request_URL)
                page.raise_for_status()
            except requests.HTTPError:
                print("Unable to make request for item" + item["Name"])
                continue

            json_dict = page.json()
            self.price_label = tkinter.Label(self.root, text=
                "Name: " + item.name + '\n' +
                "Purchase Price: " + item.purchase_price + '\n' +
                "Median Price: " + json_dict[u'median_price'] + '\n' +
                # "Lowest Price: " + json_dict[u'lowest_price'] + '\n' +
                "Break Even: " + break_even_price + '\n' +
                "15c Profit: " + fifteen_cent + '\n' +
                "20c Profit: " + twenty_cent + '\n' +
                "25c Profit: " + twenty_five_cent + '\n' +
                "30c Profit: " + thrity_cent + '\n' +
                "--------------------------------------------------\n")
            self.price_label.grid(row=self.row_counter, column=0)
            # Display the image -------------------------------------------------------------------------
            # Get img_url
            page = requests.get(item.url)
            tree = html.fromstring(page.content)
            img_url = tree.xpath('//*[@id="mainContents"]/div[2]/div/div[1]/img/@src') # //*[@id="mainContents"]/div[2]/div/div[1]/img
            try:
                print(img_url[0])
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
        profile_button = tkinter.Button(self.root, text="Profile", command=self.open_profile).place(x=200, y=0)
        self.root.mainloop()


item1 = Weapon('AK-47 | Redline (Field Tested)','http://steamcommunity.com/market/listings/730/AK-47%20%7C%20Redline%20(Field-Tested)','5.75')
item2 = Weapon('AWP | Worm God (Minimal Wear)','http://steamcommunity.com/market/listings/730/AWP%20%7C%20Worm%20God%20(Minimal%20Wear)','0.83')
item3 = Weapon('M4A1-S | Blood Tiger (Minimal Wear)','http://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Blood%20Tiger%20%28Minimal%20Wear%29','1.68')
l_o_i = []
l_o_i.append(item1)
l_o_i.append(item2)
l_o_i.append(item3)

x = SteamScraperApp(l_o_i)
x.list_items()


