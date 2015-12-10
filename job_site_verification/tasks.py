__author__ = 'boredom23309'
import getpass
import time
from datetime import timedelta

from celery.decorators import periodic_task
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

def login_to_cas(driver, username, password):
    # Set username and password, then submit
    username_elem = driver.find_element_by_id('username')
    username_elem.send_keys(username)
    password_elem = driver.find_element_by_id('password')
    password_elem.send_keys(password)

    submit = driver.find_element_by_tag_name("button")
    submit.click()

    try:
        status = driver.find_element_by_id('status')
        if "credentials you provided cannot be determined to be authentic" in status.text:
            raise Exception("Bad credentials")
    except NoSuchElementException:
        print "Credentials Accepted by CAS"

    if driver.current_url.startswith("https://cas.tamu.edu"):
        try:
            print "Duo Enabled"
            print "Waiting 15 seconds for duo iframe to populate"
            time.sleep(15)
            print "Logging in with Duo"
            if driver.find_element_by_tag_name('iframe'):
                driver.switch_to.frame(driver.find_element_by_id('duo_iframe'))
                duo_login = driver.find_element_by_id('login-button')
                duo_login.click()
            print "Selected First Duo Auth. Waiting 10 seconds for duo notification..."
            time.sleep(10)
        except NoSuchElementException:
            print "Duo Not Enabled"

    return driver

def get_be_form_field_names(driver, loc):
    input_types = ["text", "field", "button", "radio", "select"]
    names = []
    driver.get(loc)
    for it in input_types:
        elems = driver.find_elements("type", it)
        for e in elems:
            names.append(e.get_attribute("name"))
    return names

@periodic_task(run_every=timedelta(days=1))
def fetch_form_fields():
    pass

@periodic_task(run_every=timedelta(days=1))
def fetch_job_stubs():
    pass

@periodic_task(run_every=timedelta(days=1))
def put_jobs():
    pass