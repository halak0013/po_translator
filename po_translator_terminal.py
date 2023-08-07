import subprocess
from src.Po_Translator2 import Po_Translator2


if __name__ == '__main__':

    translator=Po_Translator2()
    translator.pot_file_path=""
    translator.lang_codes=[]
    translator.update_path=""

    translator.generate_translation()