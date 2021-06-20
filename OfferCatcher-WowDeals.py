from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

from selenium.webdriver.common.keys import Keys

options = Options()
options.headless = True

driver = webdriver.Chrome()
driver.get("https://deals.souq.com/eg-en/wow-deals/c/15860")


scrolls = 6
while True:
    scrolls -= 1
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_UP)
    driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_UP)
    driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_UP)
    time.sleep(2)
    if scrolls < 0:
        break

time.sleep(2)


df = pd.DataFrame(columns=['Title', 'Discount', 'Link'])
prodTitle = driver.find_elements_by_xpath("//*[contains(@class,'itemTitle')]")
for (idx, pTitle) in enumerate(prodTitle):
    itemName = pTitle
    df.loc[idx, 'Title'] = pTitle.text
    print(pTitle.text)


prodDiscount = driver.find_elements_by_xpath("//*[contains(@class,'discounts-box')]")
for (idx, pDis) in enumerate(prodDiscount):
    itemDis = pDis
    df.loc[idx, 'Discount'] = pDis.text
    print(pDis.text)



links = driver.find_elements_by_css_selector(".title-row a")
for (idx, iLink) in enumerate(links):
    df.loc[idx, 'Link'] = iLink.get_attribute('href')
    print(iLink.get_attribute("href"))

df.to_csv('data.csv')
driver.quit()
