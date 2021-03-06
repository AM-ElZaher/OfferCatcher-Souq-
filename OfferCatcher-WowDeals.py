import datetime
import os
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

try:
    os.remove('final_Discounts.csv')
    os.remove('Discount.csv')
except:
    print("No files")


def job():

    options = Options()
    options.headless = True
    driver = webdriver.Chrome()
    driver.get("https://deals.souq.com/eg-en/wow-deals/c/15860")

    # Scrolling Page
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

    # Create CSV file columns
    df = pd.DataFrame(columns=['Product', 'NewPrice', 'Discount', 'Link'])

    # Get item name
    prodTitle = driver.find_elements_by_xpath("//*[contains(@class,'itemTitle')]")
    for (idx, pTitle) in enumerate(prodTitle):
        df.loc[idx, 'Product'] = pTitle.text
        print(pTitle.text)

    # Get item Price
    newPrice = driver.find_elements_by_xpath("//*[contains(@class,'is block sk-clr1')]")
    for (idx, pnPrice) in enumerate(newPrice):
        df.loc[idx, 'NewPrice'] = pnPrice.text
        print(pnPrice.text)

    # Get item Discount
    prodDiscount = driver.find_elements_by_xpath("//*[contains(@class,'discounts-box')]")
    for (idx, pDis) in enumerate(prodDiscount):
        noPerc = pDis.text.replace('%', '')
        finalDic = noPerc.replace(' OFF', '')
        df.loc[idx, 'Discount'] = finalDic
        print(finalDic)

    # Get item link
    links = driver.find_elements_by_css_selector(".title-row a")
    for (idx, iLink) in enumerate(links):
        df.loc[idx, 'Link'] = iLink.get_attribute('href')
        print(iLink.get_attribute("href"))

    # add collected items to table

    df.to_csv('Discount.csv')
    driver.quit()

    # Deleting empty rows
    df = pd.read_csv('Discount.csv')
    new_df = df.dropna()
    new = new_df[new_df['Discount'] > '40']
    new.to_csv('final_Discounts.csv')

    # Send Mail
    mail_content = '''Latest Discounts list for (wow deals) on Souq Egypt
    '''
    sender_address = '@gmail.com'
    sender_pass = 'PASSWORD'
    receiver_address = '@gmail.com'
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Latest Discounts list for (wow deals) on Souq Egypt'
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = 'final_Discounts.csv'
    attach_file = open(attach_file_name, 'rb')
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)
    payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    session = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    session.ehlo()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
    timeNow = datetime.datetime.now().__str__()
    logfile = open('log.txt', 'a')
    logfile.write('\n' + 'Last run: ' + ' ' + timeNow)
    logfile.close()


# schedule.every(20).seconds.do(job)
schedule.every(20).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("01:59").do(job)
while 1:
    schedule.run_pending()
    time.sleep(1)
