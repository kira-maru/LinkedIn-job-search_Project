from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import os

# Uploading data
load_dotenv(".env")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
phone_number = os.getenv("PHONE_NUMBER")

# Setting driver
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.linkedin.com/")
WAIT = WebDriverWait(driver, 10)


def find_and_click(wait, by, value):
    """Finds and clicks an element by provided method and its value"""
    try:
        element = wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
    except Exception as e:
        print(f"Error clicking element {value}: {e}")


def input_data(wait, by, value, data, *args):
    """Finds and inputs data to an element by provided method and its value;
    possible to provide args which are keys that will be pressed after inputting data"""
    try:
        element = wait.until(EC.element_to_be_clickable((by, value)))
        if args:
            element.send_keys(data, *args)
        else:
            element.send_keys(data)
    except Exception as e:
        print(f"Error clicking element {value}: {e}")


# LOG IN PAGE
find_and_click(WAIT, By.CLASS_NAME, "nav__button-secondary")  # proceed to log in page
input_data(WAIT, By.ID, "username", email)  # username input
input_data(WAIT, By.ID, "password", password)  # password input
find_and_click(WAIT, By.CLASS_NAME, "btn__primary--large")  # log in button click

# JOB SEARCH PAGE
find_and_click(WAIT, By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[3]/a')  # clicks 'job' icon
input_data(WAIT, By.CSS_SELECTOR, ".jobs-search-box__inner .relative input", "Python developer", Keys.ENTER)

# Making list of all available jobs on page 1
job_offers = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "jobs-search-results__list-item"))
)
job_ids = [offer.get_attribute("data-occludable-job-id") for offer in job_offers]

# Apply to all jobs that don't require additional information beside enclosing CV
for offers in job_ids:
    find_and_click(WAIT, By.ID, offers)
    find_and_click(WAIT, By.CSS_SELECTOR, ".jobs-apply-button--top-card button")  # clicks 'Easy Apply' button
    try:
        short_apply = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-jobs-document-upload__container"))
        )
        input_data(WAIT, By.CLASS_NAME, "artdeco-text-input--input", phone_number)  # inputs phone number
        find_and_click(WAIT, By.CLASS_NAME, "artdeco-button")  # clicks 'proceed'
        short_apply.click()
    except NoSuchElementException:
        print("Additional information required. Returning to the offers' page")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        find_and_click(WAIT, By.CLASS_NAME, "artdeco-modal__dismiss")
        find_and_click(WAIT, By.NAME, "discard_application_confirm_btn")
        WAIT = WebDriverWait(driver, 10)

driver.quit()




