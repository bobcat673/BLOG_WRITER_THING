#imports
import csv
import os
import time
import kivy
import selenium
from kivy.uix.widget import Widget
import openai as ai
import requests
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty, ObjectProperty




#cleaning files
file = open("ai.txt","w+")
file.write("")
file.close()
file = open("ai_out.txt","w+")
file.write("")
file.close()
file = open("ai_title.txt","w+")
file.write("")
file.close()
#global vars
global links
global int_amount
global number_input
global text_input



#sending the promt
def the_fun_part():
    with open("ai.txt", "r") as promt_part:
        ai.api_key = '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' #your openai api key
        for link in promt_part:
            completions = ai.Completion.create(model='text-davinci-003', temperature=0.8, prompt=link, max_tokens=3000, n=1)
            time.sleep(10)
            completions = completions["choices"][0]["text"]
            promt = "write a title for the output of this prompt " + link
            title = ai.Completion.create(model='text-davinci-003', temperature=0.8, prompt=promt, max_tokens=3000, n=1)
            out_title = title["choices"][0]["text"]
            time.sleep(10)
            with open("ai_out.txt", "a") as output:
                completions = "OUTPUT> " + completions + "<END"
                completions = completions.strip().replace("\n", " ")
                completions = completions.strip().replace("\n\n", " ")
                completions = completions + "\n"
                output.write(completions)
            with open("ai_title.txt", "a") as title_out:
                out_title = "TITLE>" + out_title + "<END_TITLE"
                out_title = out_title.strip().replace("\n", " ")
                out_title = out_title + "\n"
                title_out.write(out_title)
    import web


def format_for_ai():
    with open("out.csv", "r+") as prep:
        for link in prep:
            with open("ai.txt", "a+") as for_ai:
                input = "write a review about" + link #edit promt here if youd like
                input = [input]
                for each in input:
                    modify = input[0]
                    for_ai.write(modify)
                    input.pop(0)

    the_fun_part()

#scraps the title from amazon
def scraper():
    with open('links.csv', newline='') as f:
        try:
            os.remove("out.csv")
        except:
            print("error")
            exit()
        reader = csv.reader(f)
        File = open("out.csv", "w")
        for x in range(int_amount + 1):
            readerout = reader.__next__()
            readout = ''.join(readerout)
            HEADERS = ({
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0 .2403 .157Safari / 537.36 ',
                'Accept-Language': 'en-US, en;q=0.5'})
            webpage = requests.get(readout, headers=HEADERS)
            soup = BeautifulSoup(webpage.content, "html.parser")
            try:
                title = soup.find("span", attrs={"id": 'productTitle'})
                title_value = title.string
                title_string = title_value.strip().replace(',', '')

            except AttributeError:
                title_string = "NA"

            File.write(f"{title_string}\n")
        File.close()
    format_for_ai()


def link_file():
    global links
    try:
        os.remove("links.csv")
    except:
        print("error")
        exit()
    with open('links.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for link in links:
            writer.writerow([link])

        file.close()

    scraper()


def start(number_input, text_input):
    global links
    global int_amount
    amount = number_input
    int_amount = int(amount) - 1
    links = text_input
    links = links.split(",")
    link_file()

class Third(Screen):
    name = StringProperty('third')
    pass
class MainMenu(Screen):
    global number_input
    name = StringProperty('main_menu')
    def button_hit(self):
        global number_input
        number_input =  self.ids.number_input.text

class OtherMenu(Screen):
    global number_input
    name = StringProperty('other_menu')
    def submit(self):
        global number_input
        global text_input
        text_input = self.ids.textput.text
        start(number_input,text_input)


class RootWidget(Widget):
    state = StringProperty('set_main_menu_state')
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def on_state(self, instance, value):
        if value == 'main_menu':
            self.screen_manager.current = 'main_menu'

    def set_state(self, state):
        if state == 'main_menu':
            self.screen_manager.current = 'other_menu'
        if state == 'other_menu':
            self.screen_manager.current = 'main_menu'
        if state == 'other_menu':
            self.screen_manager.current = 'third'



class TestApp(App):

    def build(self):
        return Builder.load_file("text.kv")

if __name__ == '__main__':
    TestApp().run()













    

