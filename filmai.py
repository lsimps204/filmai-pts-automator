""" Automates getting daily point updates from filmai.in streaming site 
    Chrome and Firefox only.
    Run command: python filmai.py <username> <password> <browser> """

import requests, time, shutil, zipfile, io, os, sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

print("Starting...")

# Set username/password for the site as passed into script, and set the browser for use
if len(sys.argv) == 4:
    username = sys.argv[1]
    password = sys.argv[2]
    usr_browser = sys.argv[3]
else:
    print("Incorrect number of arguments...")
    sys.exit(1)

# Set variables depending on browser (Firefox or Chrome)
if usr_browser.strip().lower() == "firefox":
    driverpath = os.path.join(os.path.expanduser("~"), "geckodriver") # Installation path
    driver_link = "https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-win64.zip"
    browser = webdriver.Firefox 
    driver_string = "geckodriver"
elif usr_browser.strip().lower() == "chrome":
    driverpath = os.path.join(os.path.expanduser("~"), "chromedriver") # Installation path
    driver_link = "https://chromedriver.storage.googleapis.com/2.45/chromedriver_win32.zip"
    browser = webdriver.Chrome
    driver_string = "chromedriver"
else:
    print("Invalid browser entered. Quitting...")
    sys.exit(1)

# If the executable (for running Chrome/Firefox browser) does not exist, install it..
if not os.path.exists(driverpath):
    print("Downloading {} driver...".format(driver_string[0:driver_string.index('d')]))

    # Make request to download the driver, and extract the ZIP file if successful
    r = requests.get(driver_link, stream=True)
    if r.status_code == requests.codes.ok: #200
        print("Extracting file...")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path=driverpath)

# Add the geckodriver executable directory to system path
if shutil.which(driver_string) is None:
    if driver_string not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + driverpath


# Run the selenium tasks
if shutil.which(driver_string) is not None:

    print("Launching browser")
    
    browser = browser() # Instantiate the browser driver
    browser.set_window_position(0, 0)
    browser.set_window_size(1024, 940)

    url = "https://www.filmai.in"

    #password = "2z1hre9y9test"

    # Run the selenium tasks to acquire the points
    browser.get((url))

    try:
        toggle_menu_icon = browser.find_element_by_xpath("//span[@class='navbar-toggler-icon']")
        toggle_menu_icon.click()
    except:
        pass

    open_loginform_btn = WebDriverWait(browser,3).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='d-inline-block link-green loginBtn']"))
    )

    #browser.find_element_by_xpath("//div[@class='d-inline-block link-green loginBtn']")
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