from googletrans import Translator
import polib
import threading

class Po_Translator2:
    def __init__(self):
        pass

    def get_po_file(self,file):
        po = polib.pofile(file)
        return [e.msgid for e in po]

    def get_translation_api(self,text, lang_code):
        translator = Translator()
        translation = translator.translate(text, src='en', dest=lang_code)
        return translation.text

    def translate_and_generate_po(self,pot_file, lang_code):
        source_texts = self.get_po_file(pot_file)
        translations = {}

        # Translate each text and store the translations in a dictionary
        for text in source_texts:
            translation = self.get_translation_api(text, lang_code)
            translations[text] = translation
            print(translation)

        # Generate the new PO file with the translations
        self.generate_po_file(pot_file, translations,lang_code)

    def generate_po_file(self,pot_file_path, translations,lang_code):
        last_slash_index = pot_file_path.rfind('/')
        # Extract the path before the last '/'
        path = pot_file_path[:last_slash_index + 1]

        po = polib.pofile(pot_file_path)
        for entry in po:
            msgid = entry.msgid
            if msgid in translations:
                entry.msgstr = translations[msgid]
        po.save(f"{path}{lang_code}.po")
        print(f"{path}{lang_code}.po saved")

    def generate_translation(self):
        for l in self.lang_codes:
            self.translate_and_generate_po(self.pot_file_path,l)

    def start_translation(self,pot_file_path,lang_codes):
        self.pot_file_path=pot_file_path
        self.lang_codes=lang_codes
        threading.Thread(target=self.generate_translation).start()
