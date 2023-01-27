#imports
import selenium
from selenium import webdriver
import fileinput
import time
import re
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
global result_body
global result_title
global num_lines
global number


def data_prep_body():
    global num_lines
    global result_body
    global number
    file = open("ai_out.txt")
    lines = [number]
    print(type(lines))
    for position, line in enumerate(file):
        print(position ,"postion")
        print(lines)
        print(position ,"postion")
        print(num_lines ," num lines")
        if position in lines:
            print(position)
            print(lines)
            result_body = re.search("OUTPUT> (.*)<END", line )
            result_body= result_body.group(1)
            result_body = result_body.strip("\"")
            result_body = result_body.strip("\n")
        else:
            pass
def data_prep_tittle():
    global num_lines
    global result_title
    global number
    file = open("ai_title.txt")
    lines = [number]
    for position, line in enumerate(file):
        if position in lines:
            result_title = re.search("TITLE> (.*)<END_TITLE", line )
            result_title= result_title.group(1)
            result_title = result_title.strip("\"")
            result_title = result_title.strip("\n")
        else:
            pass


def start_post():
    driver.get("https://www.blogger.com")
    time.sleep(5)
    click = driver.find_element(By.XPATH,"/html/body/div[7]/div[2]/header/div[4]/div[2]/div/c-wiz/div[2]/div/div")
    action = ActionChains(driver)
    action.click(on_element=click)
    action.perform()
    time.sleep(5)
def input_body():
    global result_body
    body = driver.find_element(By.CLASS_NAME,"editable")
    action = ActionChains(driver)
    action.click(on_element=body)
    action.move_to_element(body).click().send_keys(result_body).perform()

def input_title():
    global result_title
    title = driver.find_element(By.XPATH, "/html/body/div[7]/c-wiz[2]/div/c-wiz/div/div[1]/div[1]/div[1]/div/div[1]/input")
    title.send_keys(result_title)
    time.sleep(5)
def main():

    global result_body
    global result_title
    global num_lines
    global number
    num_lines = sum(1 for line in open('ai_title.txt'))
    for x in range(num_lines):
        number = number+1
        data_prep_tittle()
        data_prep_body()
        start_post()
        input_body()
        input_title()
        print(result_title + "1")
        result_title = "shout not print this"
        result_body = "should not print this"
        print("post done")
    print("all done!!")

options = Options()
options.add_argument("--user-data-dir=YOUR PROFILE DIR")
options.add_argument('--profile-directory=YOUR PROFILE NAME')
driver = webdriver.Chrome(options=options)
number=-1
main()
exit()