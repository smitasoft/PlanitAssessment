from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 1: Navigate to home page
driver.get("http://jupiter.cloud.planittesting.com")

# Step 2: Go to Contact page
driver.find_element(By.LINK_TEXT, "Contact").click()
time.sleep(1)
# Step 3: Click Submit without filling anything
driver.find_element(By.XPATH, "//a[text()='Submit']").click()
time.sleep(1)

# Step 4: Verify error messages
error_messages = driver.find_elements(By.CLASS_NAME, "help-inline")
print("Error messages found:")
for error in error_messages:
    print("-", error.text)
# Step 5: Fill mandatory fields
driver.find_element(By.ID, "forename").send_keys("Smita")
driver.find_element(By.ID, "email").send_keys("smita@example.com")
driver.find_element(By.ID, "message").send_keys("This is a test message.")

# Step 6: Click Submit again
driver.find_element(By.XPATH, "//a[text()='Submit']").click()
time.sleep(1)

# Step 7: Validate errors are gone
error_messages_after = driver.find_elements(By.CLASS_NAME, "help-inline")
if not error_messages_after:
    print("✅ All errors cleared after filling mandatory fields.")
else:
    print("❌ Some errors still present:")
    for error in error_messages_after:
        print("-", error.text)

driver.quit()
