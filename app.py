import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import openai
from secret import EMAIL, PASSWORD, OPENAI_API_KEY
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração da API da OpenAI
openai.api_key = OPENAI_API_KEY

# Caminho do arquivo de cookies
COOKIE_FILE = "linkedin_cookies.pkl"

# Configuração do Selenium
options = Options()
# Configuração das opções do Chrome
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

# Add these lines to specify Chrome binary path
if os.name == 'posix':  # Linux/Mac
    CHROME_PATHS = [
        '/usr/bin/google-chrome',
        '/usr/bin/chrome',
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser'
    ]
else:  # Windows
    CHROME_PATHS = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]

chrome_binary = None
for path in CHROME_PATHS:
    if os.path.exists(path):
        chrome_binary = path
        break

if chrome_binary:
    options.binary_location = chrome_binary
    print(f"Using Chrome binary at: {chrome_binary}")
else:
    print("Chrome binary not found in common locations. Please install Chrome or specify the correct path.")
    exit(1)

try:
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
except Exception as e:
    print(f"Error initializing Chrome driver: {e}")
    print("Please make sure Chrome is installed and the binary path is correct.")
    exit(1)

def login():
    """ Realiza login e salva os cookies na primeira vez """
    try:
        driver.get("https://www.linkedin.com/login")
        time.sleep(3)

        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        
        username.send_keys(EMAIL)
        password.send_keys(PASSWORD)
        password.send_keys(Keys.RETURN)
        time.sleep(60)

        # Salvar cookies
        with open(COOKIE_FILE, "wb") as file:
            pickle.dump(driver.get_cookies(), file)
        print("Cookies salvos.")
    except Exception as e:
        print(f"Erro durante o login: {e}")
        driver.quit()
        exit(1)

def load_cookies():
    """ Carrega os cookies salvos e faz login automaticamente """
    driver.get("https://www.linkedin.com")
    time.sleep(3)
    
    with open(COOKIE_FILE, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    
    print("Cookies carregados, recarregando página...")
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(5)

# Verifica se já existem cookies salvos
if os.path.exists(COOKIE_FILE):
    try:
        load_cookies()
    except Exception as e:
        print("Erro ao carregar cookies:", e)
        login()
else:
    login()

# Acessa o feed principal
driver.get("https://www.linkedin.com/feed/")
time.sleep(5)

def comment_post():
    # Selecionar o primeiro post usando XPath
    try:
        xpaths = [
            "/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/div[3]/div/div[1]/div[1]/div/div/div/div/div/div/div/div[2]/div[1]/div/span/span",
            "/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/div[3]/div/div[1]/div[1]/div/div/div/div/div/div/div"
        ]
        # Add explicit wait for post visibility
        wait = WebDriverWait(driver, 10)
        try:
            first_post = wait.until(EC.presence_of_element_located(
            (By.XPATH, xpaths[0])
        ))
        except:
            first_post = wait.until(EC.presence_of_element_located(
            (By.XPATH, xpaths[1])
        ))
        
        
        # Use a more robust selector for post content
        post_content = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "div.feed-shared-update-v2 span.break-words"
        ))).text
        print("Conteúdo do Post:", post_content)

        print("Lendo o post...")
        # Gerar um comentário engajador com OpenAI
        prompt = f"""
        Leia este post e gere um comentário engajador:
        
        Post: {post_content}

        Responda de forma profissional, breve e envolvente, com no máximo 10 palavras e simplifique o texto para que seja fácil de entender. Porém se for algo preconceituoso ou ofensivo, com um emoji de desgosto.
        """
        print("Gerando comentário...")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "Você é um especialista em interações profissionais no LinkedIn."},
                        {"role": "user", "content": prompt}]
            )
            comment_text = response["choices"][0]["message"]["content"]
            print("Comentário gerado:", comment_text)
        except Exception as e:
            print("Erro ao gerar comentário com OpenAI:", str(e))
            driver.quit()
            exit(1)

        # Improved selectors for interaction buttons
        comment_button = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 
            "button[aria-label*='Comment']"
        )))
        comment_button.click()
        time.sleep(2)

        # Improved comment box selector
        comment_box = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "div[role='textbox'][contenteditable='true']"
        )))
        comment_box.click()
        time.sleep(1)
        comment_box.send_keys(comment_text.replace(".", "").replace('"', ''))
        time.sleep(1)
        comment_box.send_keys(Keys.RETURN)
        time.sleep(2)
        # vai abrir um botão de comment, clicar nele
        xpath_button_finish = "/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/div[3]/div/div[1]/div[1]/div/div/div/div/div/div/div/div[5]/div[2]/div[1]/div/form/div/div/div[2]/div[2]/button/span"
        comment_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, xpath_button_finish
        )))
        time.sleep(2)
        comment_button.click()
        time.sleep(2)


        print("Comentário publicado!")

    except Exception as e:
        print("Erro ao processar:", str(e))

while True:
    try:
        comment_post()
        time.sleep(10)
        driver.refresh()
    except Exception as e:
        print("Erro ao processar:", str(e))
        time.sleep(10)
        driver.refresh()

# Fechar o navegador
driver.quit()
