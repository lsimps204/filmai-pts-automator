""" Automates getting daily point updates from filmai.in streaming site 
    Currently Firefox only. """

import requests, time, shutil, zipfile, io, os, sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

print("Starting...")
geckopath = os.path.join(os.path.expanduser("~"), "geckodriver") # Installation path

# If the "geckodriver" executable (for running Firefox browser) does not exist, install it..
if not os.path.exists(geckopath):
    print("Downloading Firefox driver...")

    # Make request to download the driver, and extract the ZIP file if successful
    r = requests.get("https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-win64.zip", stream=True)
    if r.status_code == requests.codes.ok: #200
        print("Extracting file...")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path=geckopath)

# Add the geckodriver executable directory to system path
if shutil.which("geckodriver") is None:
    if "geckodriver" not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + geckopath


# Run the selenium tasks
if shutil.which("geckodriver") is not None:
    
    # Set username/password for the site as passed into script
    if len(sys.argv) == 3:
        username = sys.argv[1]
        password = sys.argv[2]
    else:
        print("Incorrect number of arguments...")
        sys.exit(1)

    print("Launching browser")
    browser = webdriver.Firefox()
    url = "https://www.filmai.in"

    #password = "2z1hre9y9test"

    # Run the selenium tasks to acquire the points
    browser.get((url))

    open_loginform_btn = browser.find_element_by_xpath("//div[@class='d-inline-block link-green loginBtn']")
    open_loginform_btn.click()

    uname_element = WebDriverWait(browser, 2).until(
        EC.presence_of_element_located((By.NAME, "login_name"))
    )

    pw_element = WebDriverWait(browser, 2).until(
        EC.presence_of_element_located((By.NAME, "login_password"))
    )

    login_btn = WebDriverWait(browser, 2).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-primary btn-block']"))
    )

    # uname_element = browser.find_element_by_name("login_name")
    # pw_element = browser.find_element_by_name("login_password")
    # login_btn =  browser.find_element_by_xpath("//button[@class='btn btn-primary btn-block']")

    uname_element.send_keys(username)
    pw_element.send_keys(password)
    login_btn.click()

    try:
        #get_point_btn = browser.find_element_by_xpath("//div[@class='upfv link-green transfer pts ptsplus']")
        get_point_btn = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='upfv link-green transfer pts ptsplus']"))
        )
        get_point_btn.click()
    except TimeoutException as e:
        print("Could not find the add points button. Points may already be added for the current day...")


    WebDriverWait(browser, 2).until \
        (EC.invisibility_of_element_located((By.XPATH, "//div[@class='upfv link-green transfer pts ptsplus']"))
    )

    browser.quit()