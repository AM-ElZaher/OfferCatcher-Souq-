from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import schedule
import datetime
from selenium.webdriver.common.keys import Keys

options = Options()
options.headless = True
driver = webdriver.Chrome()
driver.get("https://deals.souq.com/eg-en/wow-deals/c/15860")

#Scrolling Page
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

#Create CSV file columns
df = pd.DataFrame(columns=['Product', 'Price', 'Discount', 'Link'])

#Get item name
prodTitle = driver.find_elements_by_xpath("//*[contains(@class,'itemTitle')]")
for (idx, pTitle) in enumerate(prodTitle):
    df.loc[idx, 'Product'] = pTitle.text
    print(pTitle.text)


#Get item Price
prodPrice = driver.find_elements_by_xpath("//*[contains(@class,'is block sk-clr1')]")
for (idx, pPrice) in enumerate(prodPrice):
    df.loc[idx, 'Price'] = pPrice.text
    print(pPrice.text)

#Get item Discount
prodDiscount = driver.find_elements_by_xpath("//*[contains(@class,'discounts-box')]")
for (idx, pDis) in enumerate(prodDiscount):
    noPerc = pDis.text.replace('%', '')
    finalDic = noPerc.replace(' OFF','')
    df.loc[idx, 'Discount'] = finalDic
    print(finalDic)

#Get item link
links = driver.find_elements_by_css_selector(".title-row a")
for (idx, iLink) in enumerate(links):
    df.loc[idx, 'Link'] = iLink.get_attribute('href')
    print(iLink.get_attribute("href"))

df.to_csv('Discount.csv')
driver.quit()
