import locale
from locale import gettext as _
import os
import gi
from gi.repository import GLib, Gio, Gtk
gi.require_version('Gtk', '3.0')
from Po_Translator2 import Po_Translator2


# Translation Constants:
APPNAME = "po_translator"
TRANSLATIONS_PATH = "/usr/share/locale"
# SYSTEM_LANGUAGE = os.environ.get("LANG")

# Translation functions:
locale.bindtextdomain(APPNAME, TRANSLATIONS_PATH)
locale.textdomain(APPNAME)
# locale.setlocale(locale.LC_ALL, SYSTEM_LANGUAGE)


class MainWindow(Gtk.Window):
    def __init__(self, application):
        # Gtk Builder
        self.application = application
        self.builder = Gtk.Builder()

        # Translate things on glade:
        self.builder.set_translation_domain(APPNAME)

        self.builder.add_from_file(os.path.dirname(
            os.path.abspath(__file__)) + "/../ui/MainWindow.glade")
        self.builder.connect_signals(self)

        # Add Window
        self.window: Gtk.Window = self.builder.get_object("main_window")
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_application(application)
        self.window.set_default_size(400, 300)
        self.window.connect('destroy', application.onExit)

        self.defineComponents()

        self.init_variables()

        self.window.show_all()

        # Set version
        try:
            version = open("data/version").readline()
            print(version)
            self.dialog_about.set_version(version)
        except:
            pass

    def init_variables(self):
        self.pot_file_path=""
        self.selected_lang_codes=[]
        self.translator=Po_Translator2()

        self.chck_lang_list = [
            self.chck_lng_tr,
            self.chck_lng_ar,
            self.chck_lng_de,
            self.chck_lng_es,
            self.chck_lng_zh,
            self.chck_lng_Ja,
            self.chck_lng_it,
            self.chck_lng_ru
        ]

        self.lang_code_list = [
            "tr",
            "ar",
            "de",
            "es",
            "zh-CN",
            "ja",
            "it",
            "ru"
        ]



    def defineComponents(self):
        self.btn_about: Gtk.Button = self.builder.get_object("btn_about")
        self.dialog_about: Gtk.AboutDialog = self.builder.get_object(
            "dialog_about")
        
        self.chck_lng_tr: Gtk.CheckButton = self.builder.get_object("chck_lng_tr")
        self.chck_lng_ar: Gtk.CheckButton = self.builder.get_object("chck_lng_ar")
        self.chck_lng_de: Gtk.CheckButton = self.builder.get_object("chck_lng_de")
        self.chck_lng_es: Gtk.CheckButton = self.builder.get_object("chck_lng_es")
        self.chck_lng_zh: Gtk.CheckButton = self.builder.get_object("chck_lng_zh-CN")
        self.chck_lng_Ja: Gtk.CheckButton = self.builder.get_object("chck_lng_Ja")
        self.chck_lng_it: Gtk.CheckButton = self.builder.get_object("chck_lng_it")
        self.chck_lng_ru: Gtk.CheckButton = self.builder.get_object("chck_lng_ru")

        self.file_po: Gtk.FileChooserButton = self.builder.get_object("file_po")
        self.btn_translate: Gtk.Button = self.builder.get_object("btn_translate")

    def fill_lang_codes(self):
        for i,l in enumerate(self.chck_lang_list):
            if l.get_active():
                self.selected_lang_codes.append(self.lang_code_list[i])
            
        
    def on_btn_about_clicked(self, b):
        self.dialog_about.set_visible(True)

    def on_chck_lng_toggled(self,b):
        pass

    def on_file_po_file_set(self,f):
        self.pot_file_path=self.file_po.get_filename()
        print(self.file_po.get_filename())

    def on_btn_translate_clicked(self,b):
        if os.path.exists(self.pot_file_path):
            self.fill_lang_codes()
            self.translator.start_translation(self.pot_file_path,self.selected_lang_codes)
        else:
            print("pot file not found, please try again")


    def destroy(self):
        self.window.destroy()
