import time
import psycopg2.extras
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from settings import URL, PASSWORD




connection = psycopg2.connect(user="postgres",
                              password=PASSWORD,
                              host="localhost",
                              port="5434",
                              database="postgres")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

review_href = []
driver = webdriver.Chrome('/Users/gg.khachatryan/Desktop/chromedriver')
url = URL
driver.get(url)
time.sleep(2)
json_user = driver.page_source
soup = BeautifulSoup(json_user,features="html.parser")
a = soup.findAll("a", {"class": "review_count"})
for i in a:
    if (str(i['href']),) is not review_href:
        review_href.append((str(i['href']),))
for t in range(33):
    driver.find_element(By.XPATH, "//*[@class='ui_button nav next primary ']").click()
    time.sleep(4)
    json_user = driver.page_source
    soup = BeautifulSoup(json_user, features="html.parser")
    a = soup.findAll("a", {"class": "review_count"})
    for i in a:
        if (str(i['href']),) is not review_href:
            review_href.append((str(i['href']),))

driver.quit()

cursor.executemany('insert into reviews (url) values (%s)',review_href)
connection.commit()
