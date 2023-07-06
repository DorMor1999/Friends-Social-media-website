import os
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


def fill_post_form(location, text):
    location_input = driver.find_element('name', 'location')
    location_input.send_keys(location)
    text_input = driver.find_element('name', 'text')
    text_input.send_keys(text)
    submit_btn = driver.find_element('name', 'new_post')
    submit_btn.click()


def test_db(email):
    # create connection to database
    connection = sqlite3.connect("../../back/data/data.db")
    # create cursor
    cursor = connection.cursor()
    query = f"SELECT rowid, * FROM posts WHERE writer_email = ?"
    cursor.execute(query, (email,))
    post_data = cursor.fetchone()
    if post_data is None:
        res = False
    else:
        res = True
    # commit our command
    connection.commit()
    # close our connection
    connection.close()
    return res, post_data[0]


def dir_test(post_id):
    dir = f"../../front/static/assets/data/posts/post_{post_id}"
    if os.path.exists(dir):
        return True
    else:
        return False


def add_like():
    like_btn = driver.find_element('name', 'like')
    like_btn.click()


def add_comment():
    toggle_new_comment_btn = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[5]/div/div[2]/button')
    toggle_new_comment_btn.click()
    input_comment = driver.find_element('name', 'text_comment')
    input_comment.send_keys('hey!')
    submit_btn = driver.find_element('name', 'comment')
    submit_btn.click()


def delete_post():
    delete_btn = driver.find_element('name', 'delete_post')
    delete_btn.click()


#Checking for a successful post test upload like and comment
def test1():
    try:
        driver.get("http://127.0.0.1:5000")
        get_into_sign_in_page()
        correct_email = 'right email'
        correct_password = 'right password'
        fill_sign_in_form(correct_email, correct_password)
        correct_text = 'hey'
        correct_location = "tel aviv"
        fill_post_form(correct_location, correct_text)
        check_db = test_db(correct_email)
        check_dir = dir_test(check_db[1])
        if check_db[0] and check_dir:
            add_like()
            add_comment()
            delete_post()
            sign_out()
            print("test 1 success")
        else:
            print("test 1 fail")
    except:
        print("test 1 fail")


#Unsuccessful post test upload test
def test2():
    try:
        driver.get("http://127.0.0.1:5000")
        get_into_sign_in_page()
        correct_email = 'right email'
        correct_password = 'right password'
        fill_sign_in_form(correct_email, correct_password)
        wrong_text = ''
        wrong_location = ""
        fill_post_form(wrong_location, wrong_text)
        error_msg = driver.find_element('xpath', '//*[@id="panelsStayOpen-collapseOne"]/div/div/div')
        if error_msg.text == "You must have a text!":
            sign_out()
            print("test 2 success")
        else:
            print("test 2 fail")
    except:
        print("test 2 fail")


# main

# set the driver
service = Service("C:/development/chrom driver dic/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("http://127.0.0.1:5000")

# activate tests
test1()
test2()


#close driver
driver.close()