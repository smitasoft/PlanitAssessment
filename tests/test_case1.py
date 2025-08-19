import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_contact_form_validation():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("http://jupiter.cloud.planittesting.com")
        driver.find_element(By.LINK_TEXT, "Contact").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//a[text()='Submit']").click()
        time.sleep(1)

        error_messages = driver.find_elements(By.CLASS_NAME, "help-inline")
        assert error_messages, "Expected error messages but found none."

        driver.find_element(By.ID, "forename").send_keys("Smita")
        driver.find_element(By.ID, "email").send_keys("smita@example.com")
        driver.find_element(By.ID, "message").send_keys("This is a test message.")
        driver.find_element(By.XPATH, "//a[text()='Submit']").click()
        time.sleep(1)

        error_messages_after = driver.find_elements(By.CLASS_NAME, "help-inline")
        assert not error_messages_after, "Errors still present after filling mandatory fields."

    finally:
        driver.quit()