import csv
import re
import pdb
import requests
from lxml import etree
import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def validate(item):    
    if item == None:
        item = ''
    if type(item) == int or type(item) == float:
        item = str(item)
    if type(item) == list:
        item = ' '.join(item)
    return item.strip()

def main(username, password, url, message):    
    delay_time = 10
    desired_cap = {
         'browser': 'Chrome',
         'browser_version': '83.0',
         'os': 'Windows',
         'os_version': '10',
         'resolution': '1024x768',
         'name': 'Yelp'
    }
    driver = webdriver.Remote(
        command_executor='https://username:key@hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=desired_cap
    )
    # load message page
    driver.get(url)
    # check if it loads the message page directly
    try:
        msg_input = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.XPATH, '//textarea[@class="send-message-textarea js-send-message-textarea"]')))
    except:
        print("Message input isn't loaded yet.")
        # if fail, login with the given creds
        # fill up the username form
        try:
            em_input = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.XPATH, '//form[@id="ajax-login"]//input[@id="email"]')))
            em_input.send_keys(username)
        except:
            print("Email input isn't loaded yet.")
        # fill up the password form
        try:
            pw_input = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.XPATH, '//form[@id="ajax-login"]//input[@id="password"]')))
            pw_input.send_keys(password)
        except:
            print("Password input isn't loaded yet.")
        # click on the terms and service checkbox
        try:
            tos_check = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.XPATH, '//input[@class="checkbox js-terms-checkbox gdpr-login-check"]')))
            tos_check.click()
        except:
            print("TOS check isn't loaded yet.")
        # submit auth form
        try:
            sm_bt = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.XPATH, '//button[@class="ybtn ybtn--primary ybtn--big submit ybtn-full"]')))
            sm_bt.click()
        except:
            print("Submit button isn't loaded yet.")
        # if welcome popup is open, close it
        try:
            wp_btn = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.XPATH, '//a[@class="lemon--a__06b83__IEZFH dismiss-link__06b83__1Ye3K"]')))
            wp_btn.click()
        except:
            print("Welcome Popup isn't loaded yet.")
    # fill up the message input with given message
    try:
        msg_input = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.XPATH, '//textarea[@class="send-message-textarea js-send-message-textarea"]')))
        msg_input.send_keys(message) 
    except:
        print("Message input isn't loaded yet.")
    # submit the message
    try:
        send_btn = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "small__a0b92__1sSnK link__a0b92__29O4k")]')))
        send_btn.click()
    except:
        print("Message input isn't loaded yet.")
    print('Replied successfully')
    
if __name__ == '__main__':    
    if len(sys.argv) < 5:
        print('Required usename and password')
        exit(0)  
    main(
        sys.argv[1], # username
        sys.argv[2], # password
        sys.argv[3], # link
        sys.argv[4]  # reply message
    )
