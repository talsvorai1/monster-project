from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#import time
from selenium.webdriver.common.by import By
import time
###
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
###



def negative_test(invalid_city):
    #open the website
    driver.get("http://52.200.162.71")
    #in index.html: name = "city"
    search = driver.find_element(By.NAME, "city")
    search.send_keys(invalid_city) 	#write inside search window
    #to press enter
    search.send_keys(Keys.RETURN)
    #in invalid_name.html checking return "Invalid name inserted - try again!":
    error_message = driver.find_element(By.TAG_NAME, "h1").text #getting text from h1 element
    assert error_message == "Invalid name inserted - try again!"
    print("Negative test - Error returned - Test successful")
    driver.close()
    driver.quit()



def main():
    my_invalid_city = "kjwvknhwekjvh"
    time.sleep(3) #wait 3 seconds
    negative_test(my_invalid_city)


if __name__ == '__main__':
    main()