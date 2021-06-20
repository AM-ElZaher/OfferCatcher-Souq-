from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.headless = True

driver = webdriver.Chrome()
driver.get("https://deals.souq.com/eg-en/wow-deals/c/15860")

# items = driver.find_element_by_class_name("//*[contains(@class,'discount')]")
# for item in items:
#     dis = item.text
#     noPerc = dis.replace('%', '')
#     noOFF = noPerc.replace('OFF','')
#     print(noOFF)

prodTitle = driver.find_elements_by_xpath("//*[contains(@class,'itemTitle')]")
for pTitle in prodTitle:
    itemName = pTitle
    print(pTitle.text)

prodDiscount = driver.find_elements_by_xpath("//*[contains(@class,'discount')]")
for pDis in prodDiscount:
    itemName = pDis
    # noPerc = dis.replace('%', '')
    # noOFF = noPerc.replace('OFF','')
    print(pDis.text)


driver.quit()
