import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_into_sign_in_page():
    sign_in_link = driver.find_element('xpath', '/html/body/div/div/div[2]/div/a[1]/button')
    sign_in_link.click()


def fill_sign_in_form(email, password):
    email_input = driver.find_element('name', 'email')
    email_input.send_keys(email)
    password_input = driver.find_element('name', 'password')
    password_input.send_keys(password)
    sign_in_btn = driver.find_element('xpath', '/html/body/div/div/div/main/form/button')
    sign_in_btn.click()


def sign_out():
    dropdown_toggle_btn = driver.find_element('xpath', '//*[@id="navbarSupportedContent"]/ul/li[4]/a')
    dropdown_toggle_btn.click()
    sign_out_btn = driver.find_element('name', 'sign_out')
    sign_out_btn.click()


#assuming we have a friend to chat with him
def get_into_the_chat():
    chat_options_btn = driver.find_element('xpath', '/html/body/button')
    chat_options_btn.click()
    select_chat = driver.find_element('xpath', '//*[@id="staticBackdrop"]/div[2]/div/table[3]/tbody/tr/td')
    select_chat.click()


def send_msg(msg):
    msg_input = driver.find_element('name', 'new_message')
    msg_input.send_keys(msg)
    send_btn = driver.find_element('xpath', '/html/body/div[2]/div/div/div/form/button')
    send_btn.click()


def test_db(email):
    # create connection to database
    connection = sqlite3.connect("../../back/data/data.db")
    # create cursor
    cursor = connection.cursor()
    query = f"SELECT rowid, * FROM messages WHERE user_email_writer = ?"
    cursor.execute(query, (email,))
    msg_data = cursor.fetchone()
    if msg_data is None:
        res = False
    else:
        res = True
    # commit our command
    connection.commit()
    # close our connection
    connection.close()
    return res


def test_visual_msg(msg):
    msg_text = driver.find_element('xpath', '/html/body/div[2]/div/div/div[1]/div/div/div/p[1]').text
    if msg == msg_text:
        return True
    else:
        return False


def delete_msg():
    delete_btn = driver.find_element('name', 'delete_message')
    delete_btn.click()


#Checking for successful message sending
def test1():
    try:
        driver.get("http://127.0.0.1:5000")
        get_into_sign_in_page()
        correct_email = 'dorm369258@gmail.com'
        correct_password = '123456'
        correct_msg = 'hey'
        fill_sign_in_form(correct_email, correct_password)
        get_into_the_chat()
        send_msg(correct_msg)
        check_db = test_db(correct_email)
        check_visual_msg = test_visual_msg(correct_msg)
        if check_db and check_visual_msg:
            delete_msg()
            sign_out()
            print("test 1 success")
        else:
            print("test 1 fail")
    except:
        print("test 1 fail")


# main

# set the driver
service = Service("C:/development/chrom driver dic/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("http://127.0.0.1:5000")

# activate tests
test1()



#close driver
driver.close()