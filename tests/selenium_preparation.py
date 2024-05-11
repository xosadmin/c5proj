from selenium import webdriver
from selenium.webdriver.common.by import By
import apps.randomprofile as rp

driver = webdriver.Chrome()

def register_new_account(email,password,pincode):
    driver.get("http://127.0.0.1:5000/register")
    username_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")
    repeat_password_input = driver.find_element(By.ID, "repeat_password")
    pin_code_input = driver.find_element(By.ID, "pin_code")
    submit_button = driver.find_element(By.ID, "dosubm")

    username_input.send_keys(email)
    password_input.send_keys(password)
    repeat_password_input.send_keys(password)
    pin_code_input.send_keys(pincode)
    submit_button.click()

def login(email,password):
    driver.get("http://127.0.0.1:5000/login")
    username_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "doSubmit")

    username_input.send_keys(email)
    password_input.send_keys(password)
    submit_button.click()
