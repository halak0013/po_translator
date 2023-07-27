from translate import Translator

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import quote
import polib
class Po_Translator:
    def __init__(self):
        self.po_file_path=""

    def po_translate(self, po_file_path:str, lang_codes: list):
        pot_list = self.get_po_file(po_file_path)
        

    def get_translation_g(self,text,lang_code):
        # Selenium WebDriver'ı başlatırken headless modunu etkinleştirin
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Tarayıcının arayüzünü gizler
        lng_in = "en"
        lng_out = lang_code
        #text = "how much this apple \n pineapple =klyeia "
        url_encoded_text = quote(text)

        browser = webdriver.Firefox(options=firefox_options)  # Kullandığınız tarayıcıya göre uygun WebDriver'ı seçin

        browser.get(f"https://translate.google.com/?hl=tr&sl={lng_in}&tl={lng_out}&text={url_encoded_text}&op=translate")  # Çekmek istediğiniz web sayfasının URL'sini buraya yazın
        print(f"https://translate.google.com/?hl=tr&sl={lng_in}&tl={lng_out}&text={url_encoded_text}&op=translate")
        wait = WebDriverWait(browser, 10)
        translation_element = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ryNqvb")))

        browser.quit()  # Tarayıcıyı kapatır
        return [e.text for e in translation_element if e.text != " " and e.text != ""]



    def get_translation_t(self,text,lang_code):
        lng_in = "en"
        lng_out = lang_code
        if text is not None and text != "":
            try:
                translator = Translator(to_lang=lng_out,from_lang=lng_in)
                translation = translator.translate(text)
                if translation is not None:
                    return translation.split("\n")
                else:
                    return "**error**"
            except Exception as e:
                print("Translation error:", e)
                return "**error**"
        else:
            return "**error**"
        
    def get_po_file(self,file):
        po = polib.pofile(file)
        return [e.msgid for e in po]

