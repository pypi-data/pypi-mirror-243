import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
import requests

def wrapper(url: str, selenium_method: bool = False, selenium_class_identifier: tuple = None) -> bs:
    if selenium_method is not False: # check the type of wrapper
        try: # get code at an """alternative method"""
            # dont open edge at user computer
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")

            # selenium driver
            driver = webdriver.Chrome(options=options) # chrome bc firefox is TOO slow and edge is too buged

            # delete devtools message &others popups
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")

            driver.get(url) # get page

            # wait load the page and the element be viewed
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((selenium_class_identifier[0], selenium_class_identifier[1])))
            # selenium_class_identifier value 1example: =(By.CLASS_NAME, '<element class>')
            # selenium_class_identifier value 2example: =(By.ID, '<element id>')

            page_code = driver.page_source # get page source code

            driver.quit() # close driver

            soup = bs(page_code, 'html.parser') # get soup
        except TimeoutException as err: #exception
            return f"Selenium couldn't find the element... Error: {str(err)}"
    else: # default wrapper (only requests.get and bs html.parser)
        try:
            resp = requests.get(url) # request page
            soup = bs(resp.content, 'html.parser') # get code
        except Exception as err: # exception
            return f"Something went wrong! Error: {str(err)}"
    return soup # always return the soup

class GoogleTools:
    ## FINE
    def currency_conversion(base_currency: str, target_currency: str, only_float=True) -> tuple | dict:
        url_ = f"https://www.google.com/finance/quote/{base_currency.upper()}-{target_currency.upper()}" # base url
            
        soup = wrapper(url=url_) # get soup (default method)
        
        currency_value = float(f"{float(soup.find('div', attrs={'class': 'YMlKec fxKbKc'}).text):.4f}") # find the value of the currency and turn into a float with up to 4 decimals
        last_update = soup.find('div', attrs={'class': 'ygUjEc', 'jsname': 'Vebqub'}).text.replace('\u202f', ' ').replace(' · Disclaimer', '') # finding the last update of the currency and filter it to remove bullshit

        conversion_dict = { # formatting the wrapped data to return it prettyfied
            'conversion': [
                f'1 {base_currency}',
                f'{currency_value:.2f} {target_currency}'
            ],
            'float': currency_value,
            'last_update': last_update
        }

        if only_float is not True: # filtering return
            return conversion_dict
        else:
            return conversion_dict['float']

    def translater(source_language: str, target_language: str, text: str) -> str:
        text = text.replace(' ', '%20') # making the text appropriate for the URL
        
        url_ = f'https://translate.google.com/?sl={source_language}&tl={target_language}&text={text}&op=translate' # base url

        soup = wrapper(url=url_, selenium_method=True, selenium_class_identifier=(By.CLASS_NAME, 'ryNqvb')) # get soup (selenium method)

        translated_text = soup.find('span', attrs={'class': 'ryNqvb', 'jsname': 'W297wb'}).text # finding the translation

        return translated_text # fuck yeah returning it

    ## TODO
    def bard_api(question: str):
        print(f"""Let's see... "{question}", ooh, such a nice question, but i can't respond it, i'm under development :)""") # haha

class GoogleToolsTests:
    def test_currency_conversion():
        print(f"TESTING CURRENCY CONVERSION:\n`only_float=True`:\n{GoogleTools.currency_conversion('USD', 'BRL')}\n\n`only_float=False`:\n{GoogleTools.currency_conversion('USD', 'BRL', False)}\n")

    def test_translater(text_: str):
        print(f"TESTING TRANSLATER:\n{GoogleTools.translater('pt', 'en', text_)}")

    def test_bard(question_: str):
        GoogleTools.bard_api(question_)

if __name__ == '__main__':
    test = GoogleToolsTests

    test.test_currency_conversion()

    #test.test_translater('Me chamo João Zacchello, sou programador, só isso.')

    #test.test_bard('Qual o técnico atual do Corinthians?')
