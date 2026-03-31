from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import traceback


def click_only_necessary_cookies(driver: webdriver.Chrome) -> bool:
	# Prova vari selettori testuali per cliccare solo il consenso minimo necessario.
	xpaths = [
		"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'solo') and contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'necessari')]",
		"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'solo') and contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'essenziali')]",
		"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'rifiuta') and contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'non necessari')]",
	]

	for xpath in xpaths:
		try:
			button = WebDriverWait(driver, 5).until(
				EC.element_to_be_clickable((By.XPATH, xpath))
			)
			driver.execute_script("arguments[0].click();", button)
			print("Cliccato il pulsante cookie minimo necessario.")
			return True
		except TimeoutException:
			continue

	print("Banner cookie non trovato oppure bottone 'solo necessari' non disponibile.")
	return False


def wait_and_click(driver: webdriver.Chrome, xpaths: list[str], timeout: int = 10) -> bool:
	for xpath in xpaths:
		try:
			element = WebDriverWait(driver, timeout).until(
				EC.element_to_be_clickable((By.XPATH, xpath))
			)
			driver.execute_script("arguments[0].click();", element)
			return True
		except TimeoutException:
			continue
	return False


def configure_airbnb_search(driver: webdriver.Chrome) -> None:
	# 1) DOVE: Localita Porto Corallo, Villaputzu, CA
	print("Step 1/3: imposto la localita...")
	location_input_xpaths = [
		"//input[contains(@placeholder, 'Cerca destinazioni')]",
		"//input[contains(@placeholder, 'Dove')]",
		"//input[contains(@placeholder, 'Search destinations')]",
		"//input[contains(@placeholder, 'Where')]",
		"//input[contains(@aria-label, 'Dove')]",
		"//input[contains(@aria-label, 'Where')]",
	]

	location_input = None
	for xpath in location_input_xpaths:
		try:
			location_input = WebDriverWait(driver, 10).until(
				EC.element_to_be_clickable((By.XPATH, xpath))
			)
			break
		except TimeoutException:
			continue

	if location_input is None:
		raise TimeoutException("Campo localita non trovato.")

	location_input.click()
	location_input.send_keys("Localita Porto Corallo, Villaputzu, CA")

	# Evita ENTER diretto: puo innescare una navigazione prematura e bloccare i passaggi successivi.
	wait_and_click(
		driver,
		[
			"//div[@role='option'][1]",
			"//li[@role='option'][1]",
			"//div[contains(., 'Porto Corallo') and (@role='option' or @role='button')]",
		],
		timeout=6,
	)

	location_input.send_keys(Keys.TAB)

	# 2) QUANDO: Flessibile -> Una settimana -> Giugno 2026
	print("Step 2/3: imposto quando (flessibile, una settimana, giugno 2026)...")
	wait_and_click(
		driver,
		[
			"//div[contains(., 'Quando') and @role='button']",
			"//div[contains(., 'When') and @role='button']",
			"//button[contains(., 'Quando')]",
			"//button[contains(., 'When')]",
		],
		timeout=10,
	)

	if not wait_and_click(
		driver,
		[
			"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'flessibile')]",
			"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'flexible')]",
			"//div[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'flessibile') and @role='button']",
			"//div[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'flexible') and @role='button']",
		],
		timeout=10,
	):
		raise TimeoutException("Sezione flessibile non trovata.")

	if not wait_and_click(
		driver,
		[
			"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'una settimana')]",
			"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'week')]",
		],
		timeout=10,
	):
		raise TimeoutException("Opzione 'Una settimana' non trovata.")

	if not wait_and_click(
		driver,
		[
			"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'luglio')]",
			"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'lug')]",
			"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'giugno 2026')]",
			"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'giugno')]",
			"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'june 2026')]",
			"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'june')]",
		],
		timeout=10,
	):
		raise TimeoutException("Opzione 'Giugno 2026' non trovata.")

	# 3) CHI: 4 ospiti
	print("Step 3/3: imposto 4 ospiti...")
	wait_and_click(
		driver,
		[
			"//div[contains(., 'Chi') and @role='button']",
			"//div[contains(., 'Who') and @role='button']",
			"//button[contains(., 'Chi')]",
			"//button[contains(., 'Who')]",
		],
		timeout=10,
	)

	add_guest_button_xpaths = [
		"//button[contains(@aria-label, 'Aumenta il numero di ospiti')]",
		"//button[contains(@aria-label, 'Aumenta numero ospiti')]",
		"//button[contains(@aria-label, 'Aumenta il numero di Adulti')]",
		"//button[contains(@aria-label, 'Increase number of guests')]",
		"//button[contains(@aria-label, 'Increase number of Adults')]",
	]

	guest_button = None
	for xpath in add_guest_button_xpaths:
		try:
			guest_button = WebDriverWait(driver, 8).until(
				EC.element_to_be_clickable((By.XPATH, xpath))
			)
			break
		except TimeoutException:
			continue

	if guest_button is None:
		raise TimeoutException("Pulsante per aumentare gli ospiti non trovato.")

	for _ in range(4):
		driver.execute_script("arguments[0].click();", guest_button)

	print("Campi impostati: localita, flessibile una settimana in giugno 2026, 4 ospiti.")


def open_airbnb_with_selenium() -> None:
	options = Options()
	options.add_argument("--start-maximized")

	driver = webdriver.Chrome(options=options)
	try:
		url = "https://www.airbnb.it/"
		driver.get(url)

		WebDriverWait(driver, 15).until(
			EC.presence_of_element_located((By.TAG_NAME, "body"))
		)
		click_only_necessary_cookies(driver)
		try:
			configure_airbnb_search(driver)
		except Exception as exc:
			driver.save_screenshot("airbnb_error.png")
			print(f"Errore durante la compilazione filtri: {exc}")
			print("Screenshot salvato in: airbnb_error.png")
			print(traceback.format_exc())
			input("Premi Invio per chiudere il browser dopo aver controllato la pagina...")
			return
		print(f"Pagina aperta con Selenium: {driver.title}")

		input("Premi Invio per chiudere il browser...")
	finally:
		driver.quit()


if __name__ == "__main__":
	open_airbnb_with_selenium()
