import subprocess
from src.Po_Translator2 import Po_Translator2


if __name__ == '__main__':

    translator=Po_Translator2()
    translator.pot_file_path=""
    translator.lang_codes=[]
    po_update_files=""

    # Update POT file
    #update_pot_command = "xgettext -o po/pardus-android-emulator.pot --files-from=po/files"
    update_pot_command = f"xgettext -o {translator.pot_file_path} --files-from={po_update_files}"
    subprocess.run(update_pot_command, shell=True)

    # Loop through each language
    for lang in translator.lang_codes:
        if subprocess.run(["test", "-f", f"po/{lang}.po"]).returncode == 0:
            print(f"Updating {lang}.po")
            update_po_command = f"msgmerge -o {translator.get_po_file(translator.pot_file_path)}/{lang}.po {translator.get_po_file(translator.pot_file_path)}/{lang}.po {translator.pot_file_path}"
            subprocess.run(update_po_command, shell=True)
        else:
            print(f"Creating {lang}.po")
            subprocess.run(["cp", translator.pot_file_path, f"{translator.get_po_file(translator.pot_file_path)}/{lang}.po"])



    translator.generate_translation()