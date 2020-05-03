import time
import psycopg2.extras
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from selenium import webdriver
from bs4 import BeautifulSoup
from settings import URL_TRIP_RU, URL_TRIP_EN, PASSWORD

connection = psycopg2.connect(user="postgres",
                              password=PASSWORD,
                              host="localhost",
                              port="5434",
                              database="postgres")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

driver = webdriver.Chrome('/Users/gg.khachatryan/Desktop/chromedriver')

cursor.execute('select url from reviews')
urls = cursor.fetchall()
urls_ru = [URL_TRIP_RU+i[0] for i in urls]
urls_en = [URL_TRIP_EN+i[0] for i in urls]
print(len(urls_en))
for index, url in enumerate(urls_en[473:]):

    print(index, url)
    driver.get(url)
    status = True
    while status is True:
        review_star = []
        # time.sleep(10)
        try:
            driver.find_element(By.XPATH, "//*[@class='ui_icon caret-down location-review-review-list-parts-ExpandableReview__caret--3Ud_i']").click()

        except ElementNotInteractableException:
            time.sleep(0.3)
            continue
        except NoSuchElementException:
            break
        except:
            time.sleep(0.4)
            continue
        json_user = driver.page_source
        soup = BeautifulSoup(json_user, features="html.parser")
        a = soup.findAll("div", {"class": "location-review-review-list-parts-SingleReview__mainCol--1hApa"})
        for i in a:
            text = i.find("q", {"class": "location-review-review-list-parts-ExpandableReview__reviewText--gOmRC"}).text
            star = i.find("div", {"class": "location-review-review-list-parts-RatingLine__bubbles--GcJvM"}).span['class'][1][-2:-1]
            review_star.append((text, star))
        cursor.executemany('insert into dataset_en (text,star) values (%s,%s)', review_star)
        connection.commit()

        try:
            driver.find_element(By.XPATH, "//*[@class='ui_button nav next primary ']").click()
        except:
            status = False

driver.quit()

