from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurações do Selenium
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Descomente para executar em modo headless

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def wait_for_element(locator, timeout=10):
    """Helper function to wait for an element to be visible."""
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

def click_element(locator, timeout=10):
    """Helper function to wait for an element to be clickable and then click it."""
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
    element.click()
    return element

# Função de teste para registro
def test_register():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/register.html')
    
    username_input = wait_for_element((By.ID, 'register-username'))
    password_input = driver.find_element(By.ID, 'register-password')
    
    username_input.send_keys('testuser')
    password_input.send_keys('testpassword')
    click_element((By.XPATH, '//button[@type="submit"]'))

    WebDriverWait(driver, 10).until(EC.url_contains('login.html'))
    print("Registration test passed!")

# Função de teste para login
def test_login():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/login.html')

    username_input = wait_for_element((By.ID, 'login-username'))
    password_input = driver.find_element(By.ID, 'login-password')
    
    username_input.send_keys('testuser')
    password_input.send_keys('testpassword')
    click_element((By.XPATH, '//button[@type="submit"]'))
    
    WebDriverWait(driver, 10).until(EC.url_contains('index.html'))

    assert 'index.html' in driver.current_url
    header = wait_for_element((By.TAG_NAME, 'h1'))
    assert header.text == 'Bem-vindo à Página Inicial'
    print("Login test passed and page content verified!")

# Função de teste para criar chave Pix
def test_create_pix_key():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/createpixkey.html')

    pix_key_input = wait_for_element((By.ID, 'create-pix-key'))
    create_button = click_element((By.ID, 'criarChaveBtn'))

    pix_key_input.clear()
    pix_key_input.send_keys('1234567890')

    create_button.click()
    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element((By.ID, 'message'), 'Chave Pix criada com sucesso')
    )
    print("Pix key creation test passed!")

# Função de teste para realizar uma transação Pix
def test_make_pix_transaction():
    driver.get('file:///C:/Users/rayan/Downloads/VeV_Back/front/pixin.html')

    try:
        pix_key_input = wait_for_element((By.ID, 'pay-pix-key'))
        value_input = wait_for_element((By.ID, 'pay-pix-amount'))

        # Preenchendo os valores
        driver.execute_script("arguments[0].value = '1234567890';", pix_key_input)
        driver.execute_script("arguments[0].value = '1000.00';", value_input)

        print(f"Pix key value set to: {pix_key_input.get_attribute('value')}")
        print(f"Value input set to: {value_input.get_attribute('value')}")

        click_element((By.XPATH, '//button[@type="submit"]'))

        # Aguardando a confirmação de transação
        WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element((By.ID, 'message'), 'Pix realizado com sucesso!')
        )
        print("Pix transaction test passed!")

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('error_screenshot.png')
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

# Função de teste para extrato
def test_extrato():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/extrato.html')

    try:
        pix_key_input = wait_for_element((By.ID, 'extrato-pix-key'))
        submit_button = click_element((By.ID, 'extratoBtn'))

        pix_key_input.clear()
        pix_key_input.send_keys('1234567890')

        submit_button.click()

        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.ID, 'extrato-message'), 'Transações:')
        )

        message_element = driver.find_element(By.ID, 'extrato-message')
        assert 'Transações:' in message_element.text
        print("Extrato test passed!")

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('error_screenshot.png')
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

# Função de teste para checar limite diário
def test_check_daily_limit():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/checklimit.html')

    pix_key_input = wait_for_element((By.ID, 'pix-key'))
    submit_button = click_element((By.XPATH, '//button[@type="submit"]'))

    pix_key_input.clear()
    pix_key_input.send_keys('1234567890')
    submit_button.click()

    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element((By.ID, 'daily-limit-message'), 'Limite diário')
    )

    message_element = driver.find_element(By.ID, 'daily-limit-message')
    assert 'Limite diário' in message_element.text
    print("Daily limit check test passed!")

# Função de teste para definir limite diário
def test_define_limit():
    driver.get('file:///C:/Users/rayan/Downloads/VeV_Back/front/dailyLimit.html')

    try:
        pix_key_input = wait_for_element((By.ID, 'pix-key'))
        limit_input = wait_for_element((By.ID, 'novo-limite'))

        pix_key_input.send_keys('1234567890')
        limit_input.send_keys('500.00')

        submit_button = click_element((By.XPATH, '//button[@type="submit"]'))

        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.ID, 'limit-message'), 'Limite diário definido como')
        )

        message_element = driver.find_element(By.ID, 'limit-message')
        assert 'Limite diário definido como' in message_element.text
        print("Define daily limit test passed!")

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('error_screenshot_define_limit.png')
        with open('page_source_define_limit.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

# Executar os testes
if __name__ == '__main__':
    try:
        test_register()         
        test_login()           
        test_create_pix_key()   
        test_make_pix_transaction()  
        test_extrato()
        test_check_daily_limit()
        test_define_limit()  
    finally:
        driver.quit()
