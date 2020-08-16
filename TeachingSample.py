import time
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def enter_search_items(job_to_search_for):
    job_search_box = driver.find_element_by_xpath('//*[@id="text-input-what"]')
    job_search_box.send_keys(job_to_search_for)
    # job_location_box = driver.find_element_by_xpath('//*[@id="text-input-where"]')
    # text_input = driver.find_element(by=By.ID,value='text-input-where')
    time.sleep(3)
    submit_button = driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/div/div/div/form/div[3]/button')
    submit_button.click()
    time.sleep(2)


def search_num_of_pages(num_of_pages):
    jobs = []
    page_count = 1
    while(page_count < num_of_pages):
        try:
            position_title = driver.find_elements_by_class_name('title')
        except NoSuchElementException:
            position_title = -1
        try:
            company_name_and_location = driver.find_elements_by_class_name('sjcl')
        except NoSuchElementException:
            company_name_and_location = -1
        try:
            position_descriptions = driver.find_elements_by_class_name('summary')
        except NoSuchElementException:
            position_descriptions = -1


        for (title, name_location, description) in zip(position_title,company_name_and_location,position_descriptions):
            name_location_split = name_location.text.splitlines()
            jobs.append({
                "Position title": title.text,
                "Company Name":  name_location_split[0],
                "Company Location": name_location_split[1],
                "Position Description": description.text
            })
        time.sleep(2)
        try:
            next_button = driver.find_element_by_xpath('//*[@id="resultsCol"]/nav/div/ul/li[6]/a')
            next_button.click()
        except NoSuchElementException:
            print("No More items to search through")
            break
        time.sleep(2)
        try:
            remove_popup_modal = driver.find_element_by_xpath('//*[@id="popover-x"]/a')
            remove_popup_modal.click()
        except NoSuchElementException:
            print('Good News, no annoying pop up modal!')
        page_count +=1
    return jobs


# Path I have the chrome driver on my labtop
PATH = "/Users/fuadmohamoud/Desktop/chromeDriver"

# instantiating the Driver (gives me access to all the functionality webdriver has)
driver = webdriver.Chrome(PATH)

# opens Url
driver.get("https://www.indeed.com")

# Dope Custom Function
enter_search_items('Data Scientist')

# Another dope custom function
# Returns list of jobs
jobs = search_num_of_pages(3)
driver.quit()

# convert list of jobs to panda data frame
# Excel spreedshet with columns being titles, rows having data
data = pd.DataFrame(jobs)

# Convert dataframe to Excel on my computer
data.to_excel('output.xlsx')