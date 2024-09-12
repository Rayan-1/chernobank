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
# chrome_options.add_argument("--headless")  # Executa o navegador em modo headless

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Função de teste para registro
def test_register():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/register.html')

    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'register-username'))
    )
    password_input = driver.find_element(By.ID, 'register-password')
    register_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    username_input.send_keys('testuser')
    password_input.send_keys('testpassword')
    register_button.click()

    WebDriverWait(driver, 10).until(EC.url_contains('login.html'))
    print("Registration test passed!")

# Função de teste para login
def test_login():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/login.html')

    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'login-username'))
    )
    password_input = driver.find_element(By.ID, 'login-password')
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    username_input.send_keys('testuser')
    password_input.send_keys('testpassword')
    submit_button.click()
    
    WebDriverWait(driver, 10).until(EC.url_contains('index.html'))
    
    assert 'index.html' in driver.current_url

    header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
    )
    assert header.text == 'Bem-vindo à Página Inicial'
    print("Login test passed and page content verified!")

    time.sleep(5)

# Função de teste para criar chave Pix
def test_create_pix_key():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/createpixkey.html')

    pix_key_input = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, 'create-pix-key'))
    )
    create_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, 'criarChaveBtn'))
    )

    pix_key_input.clear()
    pix_key_input.send_keys('1234567890')

    create_button.click()

    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element((By.ID, 'message'), 'Chave Pix criada com sucesso')
    )
    print("Pix key creation test passed!")

    time.sleep(3)

    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/index.html')
    time.sleep(4)
    
def test_make_pix_transaction():
    driver.get('file:///C:/Users/rayan/Downloads/VeV_Back/front/pixin.html')

    try:
        # Use WebDriverWait para garantir que os elementos estejam visíveis e interativos
        pix_key_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'pay-pix-key'))
        )
        value_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'pay-pix-amount'))
        )

        # Use JavaScript para definir os valores dos campos
        driver.execute_script("arguments[0].value = arguments[1];", pix_key_input, '1234567890')
        driver.execute_script("arguments[0].value = arguments[1];", value_input, '1000.00')

        # Verifique se os valores foram definidos corretamente
        print(f"Pix key value set to: {pix_key_input.get_attribute('value')}")
        print(f"Value input set to: {value_input.get_attribute('value')}")

        # Adicione um atraso antes de clicar no botão
        time.sleep(2)

        # Use WebDriverWait para garantir que o botão esteja clicável
        transfer_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
        )

       
        driver.execute_script("arguments[0].click();", transfer_button)
        print("Transfer button clicked.")

        # Aguarde até que a confirmação de transação seja visível
        WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element((By.ID, 'message'), 'Pix realizado com sucesso!')
        )
        print("Pix transaction test passed!")
        time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('error_screenshot.png')  

        
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

    finally:
       
        driver.switch_to.default_content()

      
        driver.get('file:///C:/Users/rayan/Downloads/VeV_Back/front/index.html')
        time.sleep(4)
 
def test_extrato():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/extrato.html')

    try:
        # Espera até que o campo da chave Pix esteja visível e interativo
        pix_key_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'extrato-pix-key'))
        )
        # Espera até que o botão de extrato esteja clicável
        submit_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, 'extratoBtn'))
        )

        # Preenche a chave Pix
        pix_key_input.clear()
        pix_key_input.send_keys('1234567890')

        # Clica no botão para obter o extrato
        submit_button.click()

        # Aguarda até que a resposta do extrato seja visível
        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.ID, 'extrato-message'), 'Transações:')
        )

        # Verifica o conteúdo do extrato
        message_element = driver.find_element(By.ID, 'extrato-message')
        print(message_element.text)
        assert 'Transações:' in message_element.text
        print("Extrato test passed!")
        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('error_screenshot.png')  # Salva uma captura de tela para depuração

        # Salva o HTML da página para análise
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

    finally:
        
        driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/index.html')
        time.sleep(4)

def test_check_daily_limit():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/checklimit.html')

    pix_key_input = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, 'pix-key'))
    )
    submit_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
    )

    # Defina a chave Pix que será usada para o teste
    pix_key = '1234567890'
    
    pix_key_input.clear()
    pix_key_input.send_keys(pix_key)
    submit_button.click()

    # Aguarde a resposta e verifique se a mensagem correta é exibida
    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element((By.ID, 'daily-limit-message'), 'Limite diário')
    )
    
    message_element = driver.find_element(By.ID, 'daily-limit-message')
    print(message_element.text)
    assert 'Limite diário' in message_element.text
    print("Daily limit check test passed!")

    time.sleep(5)
       
def test_define_limit():
    driver.get('file://C:\Users\levii\OneDrive\Área de Trabalho\trabalho VeV\back_VeV\VeV_Back\front\dailyLimit.html')

    try:
        # Localiza o campo da chave Pix e o valor do novo limite
        pix_key_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'pix-key'))
        )
        limit_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'novo-limite'))
        )

        # Preenche a chave Pix e o novo limite
        pix_key_input.send_keys('1234567890')
        limit_input.send_keys('500.00')

        # Clica no botão para definir o limite
        submit_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
        )
        submit_button.click()

        # Aguarda até que a mensagem de sucesso seja exibida
        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.ID, 'limit-message'), 'Limite diário definido como')
        )

        message_element = driver.find_element(By.ID, 'limit-message')
        print(message_element.text)
        assert 'Limite diário definido como' in message_element.text
        print("Define daily limit test passed!")

        time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('error_screenshot_define_limit.png')  # Salva uma captura de tela para depuração

        # Salva o HTML da página para análise
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
