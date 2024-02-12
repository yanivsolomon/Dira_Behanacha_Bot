import time
from selenium import webdriver
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options

# This is a bot that is fetching all of the cities that are open for a raffle on "Dira B'Hanacha"
# and sorting it alphabetically.


# code for running Edge on headless mode - (referring to it in the driver section)
opt = Options()
opt.add_argument("--headless")


# setup and teardown (fixture)
@pytest.fixture()
def test_setup():
    global driver
    driver = webdriver.Edge(options=opt, executable_path="C:\Program Files (x86)\msedgedriver.exe")
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield
    driver.close()
    driver.quit()
    print("test completed")


def test_hagrala(test_setup):
# get the website
    driver.get("https://www.dira.moch.gov.il/ProjectsList")
    time.sleep(3)
# click on "state of the project" and choose "open for registration"
    driver.find_element_by_xpath("//span[@id='select2-slctStatus-container']").click()
    driver.find_element_by_xpath("//input[@aria-label='Search']").send_keys("פתוח להרשמה")
    driver.find_element_by_xpath("//input[@aria-label='Search']").send_keys(Keys.ENTER)
    driver.find_element_by_xpath("//a[@class='btn btn-success btn-green']").click()


# go to bottom of the screen
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# make a list for page 1
    mylist = []
# Get the total number of rows in the table
    total_rows = len(driver.find_elements_by_xpath("//*[@id='divView']/div/div[7]/div/div[1]/table/tbody/tr"))

# Iterate over the rows dynamically
    for i in range(1, total_rows + 1):
        xpath = f"//*[@id='divView']/div/div[7]/div/div[1]/table/tbody/tr[{i}]/td[6]"
        number = driver.find_element_by_xpath(xpath).text
        mylist.append(number)

# move to page 2
    driver.find_element_by_xpath("//b[normalize-space()='»']").click()
    time.sleep(2)

# make a list for page 2
    mylist2 = []
# Get the total number of rows in the table
    total_rows = len(driver.find_elements_by_xpath("//*[@id='divView']/div/div[7]/div/div[1]/table/tbody/tr"))

# Iterate over the rows dynamically
    for i in range(1, total_rows + 1):
        xpath = f"//*[@id='divView']/div/div[7]/div/div[1]/table/tbody/tr[{i}]/td[6]"
        number = driver.find_element_by_xpath(xpath).text
        mylist2.append(number)

# connect both lists
    mylist.extend(mylist2)

# getting distinct cities (no duplicates)
    myset = set(mylist)

# print + sort alphabetically
    print("The cities open for Hagrala is:", sorted(myset))