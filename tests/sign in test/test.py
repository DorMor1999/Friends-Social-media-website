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


# test that check if we can get in if the user details correct
def test1():
    try:
        driver.get("http://127.0.0.1:5000")
        get_into_sign_in_page()
        correct_email = 'right email'
        correct_password = 'right password'
        fill_sign_in_form(correct_email, correct_password)
        dropdown_toggle_btn = driver.find_element('xpath', '//*[@id="navbarSupportedContent"]/ul/li[4]/a')
        dropdown_toggle_btn.click()
        sign_out_btn = driver.find_element('name', 'sign_out')
        sign_out_btn.click()
        print("test 1 success")
    except:
        print("test 1 fail")




# test that check if we get the correct error message when we try to get in with the wrong email
def test2():
    try:
        driver.get("http://127.0.0.1:5000")
        get_into_sign_in_page()
        incorrect_email = 'wrong email'
        correct_password = "dosn't matter"
        fill_sign_in_form(incorrect_email, correct_password)
        error_msg = driver.find_element('name', 'error_msg')
        if error_msg.text == "We do not have a user with this email!":
            print("test 2 success")
        else:
            print("test 2 fail")
    except:
        print("test 2 fail")




# test that check if we get the correct error message when we try to get in with the wrong password
def test3():
    try:
        driver.get("http://127.0.0.1:5000")
        get_into_sign_in_page()
        correct_email = 'right email'
        incorrect_password = 'wrong password'
        fill_sign_in_form(correct_email, incorrect_password)
        error_msg = driver.find_element('name', 'error_msg')
        if error_msg.text == "Incorrect password!":
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


