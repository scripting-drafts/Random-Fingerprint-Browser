from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pyvirtualdisplay import Display
import time
import random

userAgentList = open('PATH_TO_YOUR_USER_AGENTS_LIST.txt').read().splitlines()
localesList = ['ar-DZ', 'ar-EG', 'ar-IQ', 'ar-MA', 'ar-SA', 'ar-AE', 'bn-BD', 'bn-IN', 'zh-CN', 'zh-TW', 'zh-HK', 'nl-BE', 'nl-NL', 'en-GB', 'en-US', 'en-CA', 'en-IN', 'en-AU', 'en-NZ', 'en-ZA', 'fr-BE', 'fr-CH', 'fr-FR', 'fr-CA', 'fr-LU', 'de-AT', 'de-DE', 'de-CH', 'it-CH', 'it-IT', 'pt-PT', 'pt-BR', 'pt-AO', 'pt-MZ', 'es-ES', 'es-MX', 'es-MX', 'es-CO', 'es-CL', 'es-PE', 'es-VE', 'es-DO', 'sv-FI', 'sv-SE', 'ta-IN', 'ta-LK']

class DisplayProfileDriver:
    def setDisplay(self):
        x = random.randint(800, 1000)
        y = random.randint(600, 1000)
        display = Display(visible=1, size=(x, y))
        display.start()

        self.display = display
        self.x = x
        self.y = y

    def setProfile(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.set_preference('privacy.trackingprotection.enabled', True)
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)
        profile.set_preference("intl.accept_languages", random.choice(localesList).lower())
        profile.set_preference('general.useragent.override', random.choice(userAgentList))
        profile.update_preferences()

        self.profile = profile

    def getProxy(self):
        driver = webdriver.Firefox(self.profile)
        driver.implicitly_wait(10)
        driver.set_window_size(self.x, self.y)
        driver.get("https://sslproxies.org/")

        ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
        ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]

        self.driver = driver
        self.ips = ips
        self.ports = ports

    def setProxyProfile(self):
        proxyNum = random.randint(0, 19)
        print("Proxy selected: {}".format(self.ips[proxyNum] + ":" + self.ports[proxyNum]))
        proxyProfile = webdriver.FirefoxProfile()
        proxyProfile.set_preference("network.proxy.type", 1)
        proxyProfile.set_preference("network.proxy.http", str(self.ips[proxyNum]))
        proxyProfile.set_preference("network.proxy.http_port", int(self.ports[proxyNum]))
        proxyProfile.set_preference("network.proxy.ssl", str(self.ips[proxyNum]))
        proxyProfile.set_preference("network.proxy.ssl_port", int(self.ports[proxyNum]))
        proxyProfile.set_preference("dom.webdriver.enabled", False)
        proxyProfile.set_preference('useAutomationExtension', False)
        proxyProfile.set_preference('privacy.trackingprotection.enabled', True)
        proxyProfile.set_preference("browser.cache.disk.enable", False)
        proxyProfile.set_preference("browser.cache.memory.enable", False)
        proxyProfile.set_preference("browser.cache.offline.enable", False)
        proxyProfile.set_preference("network.http.use-cache", False)
        proxyProfile.set_preference("intl.accept_languages", random.choice(localesList).lower())
        proxyProfile.set_preference('general.useragent.override', random.choice(userAgentList))
        proxyProfile.update_preferences()

        self.proxyProfile = proxyProfile

    def setProxyDriver(self):
        proxyDriver = webdriver.Firefox(self.proxyProfile)
        proxyDriver.implicitly_wait(10)
        proxyDriver.set_window_size(self.x, self.y)

        self.proxyDriver = proxyDriver

    def getProxyDriver(self):
    	return self.proxyDriver

    def cleanDriverDisplay(self):
        self.driver.delete_all_cookies()
        self.driver.quit()
        self.display.stop()

    def cleanProxyDriverDisplay(self):
        self.proxyDriver.delete_all_cookies()
        self.proxyDriver.quit()
        self.display.stop()


ddp = DisplayProfileDriver()
ddp.setDisplay()
ddp.setProfile()
ddp.getProxy()
ddp.cleanDriverDisplay()

ddp.setDisplay()
ddp.setProxyProfile()
ddp.setProxyDriver()


try:
	ddp.getProxyDriver().get("https://www.whatismybrowser.com/")
except WebDriverException:
	ddp.getProxyDriver().get("https://www.whatismybrowser.com/")

time.sleep(30)
ddp.cleanProxyDriverDisplay()
