from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from tqdm import tqdm
import datetime
import os

class AppsflyerScraper(object):
    def __init__(self, driver):
        self.driver = driver


    def parse(self, login, password, geo, today):
        self.go_to_offers_page(login, password, geo, today)
        
    
    def go_to_offers_page(self, login, password, geo, today):
        now = datetime.datetime.now()
        self.driver.get('http://iris.superset.swaarm.com/superset/sqllab/')
        time.sleep(2)
        self.driver.find_element_by_id('username').click()
        self.driver.find_element_by_id('username').send_keys(login)
        self.driver.find_element_by_id('username').send_keys(Keys.TAB)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('password').send_keys(Keys.TAB)
        self.driver.find_element_by_id('password').send_keys(Keys.ENTER)
        time.sleep(0.5)
        self.driver.get('http://iris.superset.swaarm.com/superset/sqllab/')
        time.sleep(2)
        self.driver.find_element_by_xpath('//a[@class="ant-dropdown-trigger"]').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//a[.="100 000"]').click()

        for n in range(7):
            dd = datetime.timedelta(days=n)
            day = today - dd
            day = day.strftime("%Y-%m-%d")
            self.driver.find_element_by_xpath('//div[@class="ace_content"]').click()
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//textarea[@class="ace_text-input"]').send_keys(Keys.BACK_SPACE * 10000)
            string = F"SELECT user_connection_ip, COUNT(*) as quantity FROM clicks WHERE publisher_id in ('639', '640') and time>'{day} 00:00:00' and time<'{day} 23:59:59' and user_device_os='iOS' and user_geo_country='{geo}' GROUP BY user_connection_ip ORDER BY COUNT(*) as quantity DESC"
            self.driver.find_element_by_xpath('//div[@class="ace_content"]').click()          
            self.driver.find_element_by_xpath('//textarea[@class="ace_text-input"]').send_keys(string)
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//span[.="Run"]').click()
            try:
                element = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@class="ant-btn superset-button css-1n37w2-button"]'))
                )
                time.sleep(3)
                element.click()
            except:
                continue
        self.driver.quit()

    def new_name(self, downloadDir):          
        ext = "csv"
        i = 1
        for file in os.listdir(downloadDir):
            if file.endswith(ext):
                os.rename(f'{downloadDir}/{file}', f'{downloadDir}/{i}.{ext}')
                i = i + 1
        



def main():
    accs_cred = {'login':'admin', 'password':'6101.Pet'}
    
    login = accs_cred['login']
    password = accs_cred['password']
    today = datetime.datetime.now()
    day = today.strftime("_%d_%m_%Y")
    geos = ('US', 'GB', 'IT', 'DE', 'FR')

    for geo in geos:
        output_dir_name = '/home/nik/work/Eugene/new_reports/' + geo + str(day)
        os.mkdir(output_dir_name)
        os.environ['MOZ_HEADLESS'] = '1'
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", output_dir_name)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                            "text/plain, application/octet-stream, application/binary, text/csv, attachment/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
        driver = webdriver.Firefox(firefox_profile=fp)
        parser = AppsflyerScraper(driver)
        parser.parse(login, password, geo, today)
        parser.new_name(output_dir_name)

    

if __name__ == '__main__':
    main()