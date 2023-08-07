import os
import subprocess
import polib
import threading
import requests
from urllib.parse import quote
import json


class Po_Translator2:
    def __init__(self):
        pass

    def get_po_file(self, file):
        path = self.get_path(file)

        po = polib.pofile(file)
        return [e.msgid for e in po if e.msgstr == ""]

    def get_translation_api(self, text, lang_code):
        text = quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={lang_code}&dt=t&q={text}"
        result = ""
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open("/tmp/translate/t.txt", "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            with open("/tmp/translate/t.txt", "r") as f:
                tr = f.readline()
                print(tr)
                for d in json.loads(tr)[0]:
                    while not type(d) == str:
                        d = d[0]
                    result += d
            return result
        except requests.exceptions.RequestException as e:
            print(f"File download error: {e}")
        return "null"

    def translate_and_generate_po(self, pot_file, lang_code):
        source_texts = self.get_po_file(pot_file)
        translations = {}

        # Translate each text and store the translations in a dictionary
        for text in source_texts:
            translation = self.get_translation_api(text, lang_code)
            translations[text] = translation
            print(translation)

        # Generate the new PO file with the translations
        self.generate_po_file(pot_file, translations, lang_code)

    def get_path(self, pot_file_path):
        last_slash_index = pot_file_path.rfind('/')
        # Extract the path before the last '/'
        path = pot_file_path[:last_slash_index + 1]
        return path

    def generate_po_file(self, pot_file_path, translations, lang_code):
        path = self.get_path(pot_file_path)
        po = polib.pofile(pot_file_path)
        for entry in po:
            msgid = entry.msgid
            if msgid in translations:
                entry.msgstr = translations[msgid]
        po.save(f"{path}{lang_code}.po")
        print(f"{path}{lang_code}.po saved")

    def is_po_file_exists(self, lang_code):
        po_file = f"{self.get_path(self.pot_file_path)}{lang_code}.po"
        if os.path.exists(po_file):
            return po_file
        else:
            return self.pot_file_path

    def update_pot_from_files(self):
        update_pot_command = f"xgettext -o {self.pot_file_path} --files-from={self.update_path}"
        subprocess.run(update_pot_command, shell=True)

        # Loop through each language
        for lang in self.lang_codes:
            if subprocess.run(["test", "-f", f"po/{lang}.po"]).returncode == 0:
                print(f"Updating {lang}.po")
                update_po_command = f"msgmerge -o {self.get_po_file(self.pot_file_path)}/{lang}.po {self.get_po_file(self.pot_file_path)}/{lang}.po {self.pot_file_path}"
                subprocess.run(update_po_command, shell=True)
            else:
                print(f"Generating {lang}.po")
                subprocess.run(
                    ["cp", self.pot_file_path, f"{self.get_po_file(self.pot_file_path)}/{lang}.po"])

    def generate_translation(self):
        if self.is_po_file_active:
            self.update_pot_from_files()
        for l in self.lang_codes:
            self.translate_and_generate_po(self.is_po_file_exists(l), l)
        print("finished")

    def start_translation(self, pot_file_path, lang_codes, update_path="", is_po_file_active=False):
        self.pot_file_path = pot_file_path
        self.lang_codes = lang_codes
        self.update_path: str = update_path
        self.is_po_file_active = is_po_file_active
        threading.Thread(target=self.generate_translation).start()
