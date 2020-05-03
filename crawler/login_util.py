from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def login(name, pwd):
    chrome_option = Options()
    chrome_option.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_option)
    driver.get("https://accounts.douban.com/passport/login")

    driver.find_element_by_class_name("account-tab-account").click()
    driver.find_element_by_css_selector(".account-tabcon-start #username").send_keys(name)
    driver.find_element_by_css_selector(".account-tabcon-start #password").send_keys(pwd)
    driver.find_element_by_css_selector("#account > div.login-wrap > div.login-right > div > div.account-tabcon-start > div.account-form > div.account-form-field-submit").click()

    driver.get("https://www.douban.com/group/")
    cookies = driver.get_cookies()

    dbcl = None
    ck = None
    bid = None
    for c in cookies:
        if c['name'] == 'dbcl2':
            dbcl = c['value']
        elif c['name'] == 'ck':
            ck = c['value']
        elif c['name'] == 'bid':
            bid = c['value']

    return dbcl, ck, bid
