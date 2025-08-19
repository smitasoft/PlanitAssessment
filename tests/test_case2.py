# tests/test_case2.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def test_contact_form_success():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("http://jupiter.cloud.planittesting.com")
        driver.find_element(By.LINK_TEXT, "Contact").click()

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "forename"))).send_keys("Smita")
        driver.find_element(By.ID, "email").send_keys("smita@example.com")
        driver.find_element(By.ID, "message").send_keys("Automated test message.")

        driver.find_element(By.XPATH, "//a[text()='Submit']").click()

        success_msg = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-success"))
        ).text

        assert "Thanks Smita" in success_msg, f"Unexpected success message: {success_msg}"
        print("✅ Success message validated.")

    finally:
        driver.quit()