from constants import *
from driver import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(executable_path=driver_path)
driver.get(site)


links = []
idx = 2 
while True:
    xpath = f'//*[@id="result"]/div[{idx}]/div/div/div[2]/div/h3/a'
    try:
        element = driver.find_element(By.XPATH, xpath)
        link = element.get_attribute("href")
        links.append(link)
        idx += 1
    except NoSuchElementException:
        break

for link in links:
    driver.get(link)
    div_xpath = '//*[@id="wrapper"]/div/section[2]/div/div/div/div[2]'

    try:
        div_element = driver.find_element(By.XPATH, div_xpath)
        div_text = div_element.text
        file_name = '_'.join(div_text.split('\n')[0].split(' '))
        with open(f'data/{file_name}.txt', 'w') as f:
            f.write(div_text)
    except Exception as e:
        print(f"Error extracting text from the div: {str(e)}")

driver.quit()