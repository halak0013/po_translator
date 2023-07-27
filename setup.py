#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import subprocess


def generate_mo_files():
    podir = "po"
    mo = []
    for po in os.listdir(podir):
        if po.endswith(".po"):
            os.makedirs("{}/{}/LC_MESSAGES".format(podir,
                        po.split(".po")[0]), exist_ok=True)
            mo_file = "{}/{}/LC_MESSAGES/{}".format(
                podir, po.split(".po")[0], "po_translator.mo")
            msgfmt_cmd = 'msgfmt {} -o {}'.format(podir + "/" + po, mo_file)
            subprocess.call(msgfmt_cmd, shell=True)
            mo.append(("/usr/share/locale/" + po.split(".po")[0] + "/LC_MESSAGES",
                       ["po/" + po.split(".po")[0] + "/LC_MESSAGES/po_translator.mo"]))
    return mo


changelog = "debian/changelog"
if os.path.exists(changelog):
    head = open(changelog).readline()
    try:
        version = head.split("(")[1].split(")")[0]
    except:
        print("debian/changelog format is wrong for get version")
        version = "0.0.0"
    f = open("data/version", "w")
    f.write(version)
    f.close()

data_files = [
    ("/usr/bin", ["po_translator"]),

    ("/usr/share/applications",
     ["tr.org.bismih.po_translator.desktop"]),  # /usr/share/icons

    ("/usr/share/icons",
     ["data/po_translator.svg"]),

    ("/usr/share/icons/hicolor/scalable/apps/",
     ["data/po_translator.svg"]),



    ("/usr/share/pardus/po_translator/ui",
     ["ui/MainWindow.glade"]),

    ("/usr/share/pardus/po_translator/src",
     ["src/MainWindow.py",
      "src/Main.py",
      "src/Po_Translator2.py"]),

    ("/usr/share/pardus/po_translator/data",
     ["data/po_translator.svg",
      "data/version"]),

] + generate_mo_files()

setup(
    name="po_translator",
    version=version,
    packages=find_packages(),
    scripts=["po_translator"],
    install_requires=["PyGObject", "polib","googletrans==4.0.0-rc1"],
    data_files=data_files,
    author="Muhammet Halak",
    author_email="halakmuhammet145@gmail.com",
    description="Translate pot file easily",
    license="GPLv3",
    keywords="po_translator, translate, po, pardus",
    url="https://github.com/halak0013/po_translator",
)
