from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome
options = Options()
options.add_argument("--start-maximized")  # Optional: "--headless" for background execution
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Step 1: Navigate to home page
    driver.get("http://jupiter.cloud.planittesting.com")

    # Step 2: Go to Contact page
    driver.find_element(By.LINK_TEXT, "Contact").click()

    # Step 3: Fill mandatory fields
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "forename"))).send_keys("Smita")
    driver.find_element(By.ID, "email").send_keys("smita@example.com")
    driver.find_element(By.ID, "message").send_keys("Automated test message.")

    # Step 4: Submit the form
    driver.find_element(By.XPATH, "//a[text()='Submit']").click()

    # Step 5: Validate success message
    success_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-success"))
    ).text

    assert "Thanks Smita, we appreciate your feedback." in success_msg
    print("✅ Success message validated.")

except Exception as e:
    print(f"❌ Test failed: {e}")

finally:
    driver.quit()