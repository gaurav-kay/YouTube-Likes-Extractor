from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, WebDriverException

driver = webdriver.Chrome('D:/Download/chromedriver_win32/chromedriver.exe')
driver.implicitly_wait(5)
# get user to login
driver.get('https://youtube.com')
try:
    driver.find_element_by_css_selector('#buttons > ytd-button-renderer > a').click()

    # print("Enter \"done\" when you're done logging in")

    while driver.current_url[:23] != "https://www.youtube.com":
        print(driver.current_url, driver.current_url[:23])
        sleep(2)

    driver.maximize_window()  # to view the liked videos section

    driver.find_element_by_xpath('//*[@title="Liked videos"]').click()  # goes to likes page
    driver.get(str(driver.current_url) + "&disable_polymer=true")  # takes to legacy page where the below class selections work

    # edit these variable if all links aren't loaded as per internet speed etc
    loop_time = 60 * 6  # in seconds
    internet_buffer_time = 2

    time_end = time() + loop_time
    while time() < time_end:
        try:
            driver.find_element_by_tag_name('html').send_keys(Keys.END)
            driver.find_element_by_css_selector('#pl-video-list > button').click()
            sleep(internet_buffer_time)
        except NoSuchElementException:
            break

    sleep(2)  # give a second to calm tf down
    html = driver.page_source

    with open('liked_videos_raw_html.txt', 'w', encoding='utf-8') as f:
        f.write(html)

    with open('liked_videos_raw_html.txt', 'r', encoding='utf-8') as f:
        file_soup = BeautifulSoup(f.read(), 'lxml')

    links = file_soup.select('a.pl-video-title-link.yt-uix-tile-link.yt-uix-sessionlink.spf-link ')
    
    print(len(links))
except WebDriverException:
    print("Window Closed! Ending process...")
