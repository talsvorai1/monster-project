from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def positive_test(valid_city):
    #open the website
    driver.get("http://localhost")
    #in index.html: name = "city"
    search = driver.find_element(By.NAME, "city")
    search.send_keys(valid_city) 	#write inside search window
    #to press enter:
    search.send_keys(Keys.RETURN)
    #in result.html class = "card". if found it means name is valid and city is returned, not error:
    if driver.find_element(By.CLASS_NAME, "card"):
        print("Positive test - Name found by webstie - Test successful")
    else:
        print("Positive test - Name was not found by website - Test unseccessful")

    driver.close()
    driver.quit()

def main():
    my_valid_city = "Barcelona"
    positive_test(my_valid_city)
    
if __name__ == '__main__':
    main()
