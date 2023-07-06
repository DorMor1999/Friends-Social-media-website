import os
import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_into_register_page():
    register_link = driver.find_element('xpath', '/html/body/div/div/div[2]/div/a[2]/button')
    register_link.click()


def fill_register_form(email, password, first_name, last_name, date, gender):
    email_input = driver.find_element('name', 'email')
    email_input.send_keys(email)
    password_input = driver.find_element('name', 'password')
    password_input.send_keys(password)
    first_name_input = driver.find_element('name', 'first_name')
    first_name_input.send_keys(first_name)
    last_name_input = driver.find_element('name', 'last_name')
    last_name_input.send_keys(last_name)
    date_input = driver.find_element('name', 'birthday')
    date_input.send_keys(date)
    if gender:
        radio_btn_male = driver.find_element("id", 'inlineRadio1')
        radio_btn_male.click()
    register_btn = driver.find_element("xpath", '/html/body/div/div/div/main/form/button')
    register_btn.click()


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


def delete_user():
    dropdown_toggle_btn = driver.find_element('xpath', '//*[@id="navbarSupportedContent"]/ul/li[4]/a')
    dropdown_toggle_btn.click()
    private_btn = driver.find_element('xpath', '//*[@id="navbarSupportedContent"]/ul/li[4]/ul/li[1]/a')
    private_btn.click()
    delete_accordion_btn = driver.find_element('xpath', '//*[@id="accordionFlushExample"]/div[6]/h2/button')
    delete_accordion_btn.click()
    delete_btn = driver.find_element('name', 'delete_user')
    delete_btn.click()


def db_test(email):
    # create connection to database
    connection = sqlite3.connect("../../back/data/data.db")
    # create cursor
    cursor = connection.cursor()
    query = f"SELECT rowid, * FROM users WHERE email = ?"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    if user_data is None:
        res = False
    else:
        res = True
    # commit our command
    connection.commit()
    # close our connection
    connection.close()
    return res


def dir_test(email):
    dir = f"../../front/static/assets/data/users/{email}"
    if os.path.exists(dir):
        return True
    else:
        return False


#Check status of successful registration
def test1():
    try:
        driver.get("http://127.0.0.1:5000")
        get_into_register_page()
        correct_email = 'right email'
        correct_password = 'right password'
        correct_first_name = "right first name"
        correct_last_name = "right last name"
        correct_date = "right date"
        correct_gender = True
        fill_register_form(correct_email, correct_password, correct_first_name, correct_last_name, correct_date, correct_gender)
        db_check = db_test(correct_email)
        dir_check = dir_test(correct_email)
        if db_check and dir_check:
            get_into_sign_in_page()
            fill_sign_in_form(correct_email, correct_password)
            delete_user()
            print("test 1 success")
        else:
            print("test 1 fail")
    except:
        print("test 1 fail")


#Check status of not successful registration because all the inputs wrong
def test2():
    try:
        driver.get("http://127.0.0.1:5000")
        get_into_register_page()
        wrong_email = ''
        wrong_password = ''
        wrong_first_name = ""
        wrong_last_name = ""
        wrong_date = ""
        wrong_gender = False
        fill_register_form(wrong_email, wrong_password, wrong_first_name, wrong_last_name, wrong_date, wrong_gender)
        error_messages = driver.find_elements('css selector', 'body > div > div > div > main > div > div > p')
        error_real_messages = ["First name needs to be Up to 20 letters and The first letter needs to be capital letter!", "Last name needs to be Up to 20 letters and The first letter needs to be capital letter!", "Age eighteen or older!", "You must select a gender!", "You can register only with gmail!", "Password must have six or more characters!"]
        for index in range(len(error_real_messages)):
            if error_messages[index].text != error_real_messages[index]:
                print("test 2 fail")
                return
        print("test 2 success")
    except:
        print("test 2 fail")


#Check status of not successful registration because we already have user with this email
def test3():
    try:
        driver.get("http://127.0.0.1:5000")
        get_into_register_page()
        wrong_email = 'exist email'
        correct_password = 'right password'
        correct_first_name = "right first name"
        correct_last_name = "right last name"
        correct_date = "right date"
        correct_gender = True
        fill_register_form(wrong_email, correct_password, correct_first_name, correct_last_name, correct_date, correct_gender)
        error_msg = driver.find_element("xpath", "/html/body/div/div/div/main/div/div")
        if error_msg.text == "We already have a user with this email!":
            print("test 3 success")
        else:
            print("test 3 fail")
    except:
        print("test 3 fail")


# main

# set the driver
service = Service("C:/development/chrom driver dic/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("http://127.0.0.1:5000")

# activate tests
test1()
test2()
test3()

#close driver
driver.close()