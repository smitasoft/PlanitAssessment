from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ---------- Setup ----------
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get("https://jupiter.cloud.planittesting.com/")
    print("🌐 Opened Jupiter Toys homepage.")
    return driver

# ---------- Navigate to Shop ----------
def navigate_to_shop(driver):
    wait = WebDriverWait(driver, 10)
    shop_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Shop")))
    shop_link.click()
    print("✅ Navigated to Shop page.")

# ---------- Add Items to Cart ----------
def add_items_to_cart(driver, item_name, quantity):
    wait = WebDriverWait(driver, 10)
    for i in range(quantity):
        add_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//h4[text()='{item_name}']/following-sibling::p//a[text()='Buy']")))
        add_button.click()
        time.sleep(0.3)
    print(f"🧸 Added {quantity} x {item_name} to cart.")

# ---------- Go to Cart ----------
def go_to_cart(driver):
    wait = WebDriverWait(driver, 10)
    cart_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Cart')]")))
    cart_link.click()
    print("🛒 Navigated to Cart page.")

# ---------- Verify Subtotals ----------
def verify_subtotals(driver, expected_items):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'cart-items')]")))
    print("🔍 Verifying subtotals for each product...")

    for item_name, expected_qty in expected_items.items():
        row_xpath = f"//table[contains(@class,'cart-items')]//tr[td[contains(.,'{item_name}')]]"

        try:
            price_text = driver.find_element(By.XPATH, f"{row_xpath}/td[2]").text
            qty_value = driver.find_element(By.XPATH, f"{row_xpath}/td[3]//input").get_attribute("value")
            subtotal_text = driver.find_element(By.XPATH, f"{row_xpath}/td[4]").text

            price = float(price_text.replace("$", "").strip())
            qty = int(qty_value.strip())
            subtotal = float(subtotal_text.replace("$", "").strip())
            expected_subtotal = round(price * qty, 2)

            print(f"🧾 {item_name}: Price=${price}, Qty={qty}, Subtotal=${subtotal}")
            assert qty == expected_qty, f"❌ Quantity mismatch for {item_name}: expected {expected_qty}, got {qty}"
            assert subtotal == expected_subtotal, f"❌ Subtotal mismatch for {item_name}: expected ${expected_subtotal}, got ${subtotal}"

        except Exception as e:
            print(f"⚠️ Could not verify {item_name}: {str(e)}")

    print("✅ Subtotal verification complete.")

# ---------- Main Test Runner ----------
def main():
    driver = setup_driver()
    try:
        navigate_to_shop(driver)
        add_items_to_cart(driver, "Stuffed Frog", 2)
        add_items_to_cart(driver, "Fluffy Bunny", 5)
        add_items_to_cart(driver, "Valentine Bear", 3)
        go_to_cart(driver)

        expected_items = {
            "Stuffed Frog": 2,
            "Fluffy Bunny": 5,
            "Valentine Bear": 3
        }

        verify_subtotals(driver, expected_items)

    finally:
        print("🧹 Closing browser...")
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    main()