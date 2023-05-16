import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from webdriver_manager import chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

class Teste_Proiect_Final(unittest.TestCase):
    DIGEST_AUTHENTICATION = (By.LINK_TEXT, "Digest Authentication")
    USERNAME = 'admin'
    PASSWORD = 'admin'
    AUTH_CONFIRM_MESSAGE = (By.TAG_NAME, 'p')
    RESULT_MESSAGE = (By.ID, "result")
    FORM_AUTHENTICATION = (By.LINK_TEXT, "Form Authentication")
    JAVA_SCRIPT_ALERTS = (By.LINK_TEXT, "JavaScript Alerts")
    ALERT_BUTTON = (By.XPATH, '//button[text()="Click for JS Alert"]')
    CONFIRM_BUTTON = (By.XPATH, '//button[text()="Click for JS Confirm"]')
    PROMPT_BUTTON = (By.XPATH, '//button[text()="Click for JS Prompt"]')
    CONTEXT_MENU = (By.LINK_TEXT, "Context Menu")
    CONTEXT_BOX = (By.ID, "hot-spot")
    LOGIN_BUTTON = (By.XPATH, "//i[@class='fa fa-2x fa-sign-in']")
    SUCCESS_MESSAGE = (By.XPATH, '//div[@class="flash success"]')

    def setUp(self):      #  aceasta metoda este obligatorie
        self.driver = webdriver.Chrome() # se initializeaza driverul Chrome
        self.driver.maximize_window() # se mareste pagina ca sa putem urmari evolutia testelor
        self.driver.implicitly_wait(5) # se foloseste pentru eventualele intarzieri de procesare a codului
        sleep(2) # se foloseste pentru a putea noi ca si useri sa identificam stadiile rularii si unde ar putea sa se blocheze codul
        self.driver.get("https://the-internet.herokuapp.com/") #linkul web se poate pune aici sau la fiecare test unitar de mai jos

    def tearDown(self):  # metoda care inchide browserul dupa rularea tuturor testelor
        self.driver.quit()

    # se verifica daca titlul paginii este corect
    def test_1_page_title_corect(self):
        expected_title = "The Internet"
        actual_title = self.driver.title
        assert actual_title == expected_title, f"Titlu incorect: {actual_title}"

    # se valideaza mesajul de confirmare dupa introducerea corecta a userului si a parolei in meniul digest_auth
    def test_2_mesaj_corect_user_pass_corecte(self):
        self.driver.get("https://the-internet.herokuapp.com/")
        self.driver.get(f'https://{self.USERNAME}:{self.PASSWORD}@the-internet.herokuapp.com/digest_auth')
        sleep(3)
        confirm_message = self.driver.find_element(*self.AUTH_CONFIRM_MESSAGE).text
        self.assertEqual(confirm_message, "Congratulations! You must have the proper credentials.")

    # se verifică linkul de pe elementul xpath=//h2 sa fie corect
    def test_3_atribut_href_corect(self):
        actual_link = self.driver.find_element(By.XPATH, '//a[@href="http://elementalselenium.com/"]').get_attribute('href')
        assert actual_link == 'http://elementalselenium.com/', 'Link-ul este gresit'

    # Se verifica mesajul de confirmare la apasarea butonului "OK" din pop-up-ul generat din butonul "Click for JS Alert"
    def test_4_alert(self):
        self.driver.find_element(*self.JAVA_SCRIPT_ALERTS).click()
        self.driver.find_element(*self.ALERT_BUTTON).click()
        obj = self.driver.switch_to.alert # Ne-am mutat de pe pagina noastra pe fereastra de alerta si am salvat fereastra intro variabila obj
        print(f"Mesajul de pe fereastra de alerta este: {obj.text}") # metoda text extrage textul din alerta din cazul nostru (din elementul obj)
        obj.accept() # Dam OK la alerta noastra
        sleep(2)
        message = self.driver.find_element(*self.RESULT_MESSAGE).text
        sleep(4)
        self.assertEqual(message, "You successfully clicked an alert", "Mesajul nu este cel asteptat")

    # Se verifica mesajul de confirmare la apasarea butonului "OK" din pop-up-ul generat din butonul "Click for JS Confirm"
    def test_5_confirm_ok(self):
        self.driver.find_element(*self.JAVA_SCRIPT_ALERTS).click()
        self.driver.find_element(*self.CONFIRM_BUTTON).click()
        obj = self.driver.switch_to.alert
        print(f"Mesajul de pe fereastra este: {obj.text}")
        obj.accept() # echivalent cu ok
        message = self.driver.find_element(*self.RESULT_MESSAGE).text
        sleep(2)
        self.assertEqual(message,"You clicked: Ok","Mesajul nu este cel asteptat")

    # Se verifica mesajul de confirmare la apasarea butonului "Cancel" din pop-up-ul generat din butonul "Click for JS Confirm"
    def test_6_confirm_cancel(self):
        self.driver.find_element(*self.JAVA_SCRIPT_ALERTS).click()
        self.driver.find_element(*self.CONFIRM_BUTTON).click()
        obj = self.driver.switch_to.alert
        obj.dismiss()  ## cu dismiss dam cancel la pop-up de confirm alert
        message = self.driver.find_element(*self.RESULT_MESSAGE).text
        sleep(2)
        self.assertEqual(message, "You clicked: Cancel", "Mesajul nu este cel asteptat")

    # Se verifica mesajul de confirmare la completarea unui mesaj si apasarea butonului "OK"
    # din pop-up-ul generat din butonul "Click for JS Prompt"
    def test_7_prompt_mesaj_ok(self):
        self.driver.find_element(*self.JAVA_SCRIPT_ALERTS).click()
        self.driver.find_element(*self.PROMPT_BUTTON).click()
        obj = self.driver.switch_to.alert
        input_text = "Diana"
        sleep(2)
        obj.send_keys(input_text) # Trimitem textul Diana in text-field-ul promptului
        obj.accept()
        message = self.driver.find_element(*self.RESULT_MESSAGE).text
        sleep(2)
        self.assertEqual(message, f"You entered: {input_text}", "Mesajul nu este cel asteptat")

    # Se verifica mesajul de confirmare la completarea unui mesaj si apasarea butonului "Cancel"
    # din pop-up-ul generat din butonul "Click for JS Prompt"
    def test_8_prompt_cancel(self):
        self.driver.find_element(*self.JAVA_SCRIPT_ALERTS).click()
        self.driver.find_element(*self.PROMPT_BUTTON).click()
        obj = self.driver.switch_to.alert
        obj.dismiss()  # cu dismiss dam cancel la pop-up de confirm alert
        message = self.driver.find_element(*self.RESULT_MESSAGE).text
        sleep(2)
        self.assertEqual(message, "You entered: null", "Mesajul nu este cel asteptat")

    # confirmare ca am selectat "OK" dintr-un click dreapta dintr-un context menu
    def test_9_context_menu(self):
        self.driver.find_element(*self.CONTEXT_MENU).click()
        context_box = self.driver.find_element(*self.CONTEXT_BOX) # alerta apare doar in dreptunghiul respectiv
        context_box.click() # folosind click() facem click stanga, click-ul normal
        sleep(2)
        action = ActionChains(self.driver)  # action chains ne ajutam sa facem click dreapta
        action.context_click(context_box).perform() # cu metoda context_click accesam metoda perform() care e adevaratul click dreapta
        sleep(3)
        self.driver.switch_to.alert.accept() # ne-am mutat pe alerta care a aparut si am dat click pe OK
        sleep(2)

    # confirmarea url asteptat fata de cel real dupa accesarea linkului "Form Authentication"
    def test_10_url_login_auth_corect(self):
        self.driver.find_element(*self.FORM_AUTHENTICATION).click()
        expected_url = "https://the-internet.herokuapp.com/login"
        actual_url = self.driver.current_url
        assert actual_url == expected_url, f"URL incorect:{actual_url}"

    # dupa accesarea linkului "Form Authentication" se verifica daca butonul de Login este afisat
    def test_11_buton_login_displayed(self):
        self.driver.find_element(*self.FORM_AUTHENTICATION).click()
        buton_login = self.driver.find_element(*self.LOGIN_BUTTON)
        sleep(2)
        self.assertTrue(buton_login.is_displayed(), "Butonul de Login nu este afisat")

    # se verifica ca la accesarea cu user si parola corecte in meniul "Form Authentication"
    # mesajul sa contina textul "secure"
    def test_12_verif_secure(self):
        self.driver.find_element(*self.FORM_AUTHENTICATION).click()
        self.driver.find_element(By.ID, "username").send_keys('tomsmith')
        self.driver.find_element(By.ID, "password").send_keys('SuperSecretPassword!')
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        url_dupa_logare = self.driver.current_url
        self.assertTrue("secure" in url_dupa_logare, 'Noul url nu contine secure')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.SUCCESS_MESSAGE))
        assert self.driver.find_element(*self.SUCCESS_MESSAGE).is_displayed() == True
