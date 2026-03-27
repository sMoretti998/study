from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.set_window_size(1200, 900)
driver.get("https://lms.pegaso.multiversity.click/accedi?redirect=%252F")

wait = WebDriverWait(driver, 20)
username_input = wait.until(EC.visibility_of_element_located((By.ID, "username")))
password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))

username_input.send_keys("smoretti_0312500123")
password_input.send_keys("T4rt0s5o1998@")

# Trova e clicca il pulsante "Accedi"
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[span[text()='Accedi']])[1]")))
actions = ActionChains(driver)
actions.move_to_element(login_button).click().perform()

# Attendi che il loader "Caricamento..." sparisca
wait.until(EC.invisibility_of_element_located((By.XPATH, "//span[contains(text(), 'Caricamento...')]")))

print("Login effettuato e caricamento completato!")
input("Premi INVIO per chiudere il browser...")
driver.quit()