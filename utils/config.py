import configparser
import json

VERSION = "0.95"

default_config = {
    "GENERAL": {
        "version": VERSION,
        "league": "League",
        "stashtabMacro": "yes",
        "projectURL": "https://github.com/Ethck/Path-of-Accounting/",
        "releaseURL": "https://api.github.com/repos/Ethck/Path-of-Accounting/releases",
    },
    "GUI": {
        "useGUI": "yes",
        "timeout": "4",
        "backgroundColor": "#1a1a1a",
        "backgroundColor2": "#1f1f1f",
        "headerColor": "#0d0d0d",
        "fontColor": "#e6b800",
        "font": "Courier",
        "fontSize": "12",
    },
    "HOTKEYS": {
        "basicSearch": "alt+d",
        "advSearch": "alt+v",
        "openWiki": "alt+w",
        "openTrade": "alt+t",
        "searchBase": "alt+c",
        "showInfo": "alt+f",
        "hideout": "f5",
    },
}

config = configparser.ConfigParser()
config.read("settings.cfg")
config2 = configparser.ConfigParser()

needs_write = False

try:
    config2.set("GENERAL", "version", VERSION)
except configparser.NoSectionError:
    config2.add_section("GENERAL")
    config2.set("GENERAL", "version", VERSION)

try:
    v = config["GENERAL"]["version"]
    v.replace("v", "")
    if float(v) <= 0.93:  # Incase of major change, delete settings
        settings = open("settings.cfg", "w")
        settings.truncate(0)
        settings.close()
        v = 0
    if v != VERSION:
        needs_write = True
except Exception:
    needs_write = True


def read_config(section, key):
    global needs_write
    try:
        value = config.get(section, key)
        try:
            config2.set(section, key, value)
        except configparser.NoSectionError:
            config2.add_section(section)
            config2.set(section, key, value)
        return value
    except configparser.NoSectionError:
        config.add_section(section)
        needs_write = True
        return read_config(section, key)
    except configparser.NoOptionError:
        needs_write = True
        config.set(section, key, default_config[section][key])
        return read_config(section, key)


LEAGUE = read_config("GENERAL", "league")

PROJECT_URL = read_config("GENERAL", "projectURL")

RELEASE_URL = read_config("GENERAL", "releaseURL")

USE_GUI = True if read_config("GUI", "useGUI") == "yes" else False
TIMEOUT_GUI = read_config("GUI", "timeout")
GUI_BG1 = read_config("GUI", "backgroundColor")
GUI_BG2 = read_config("GUI", "backgroundColor2")
GUI_FONT = read_config("GUI", "font")
GUI_FONT_SIZE = read_config("GUI", "fontSize")
GUI_FONT_COLOR = read_config("GUI", "fontColor")
GUI_HEADER_COLOR = read_config("GUI", "headerColor")

# This is what the API returns, so we can only be confident with
# these 10 results.
MIN_RESULTS = 10

STASHTAB_SCROLLING = (
    True if read_config("GENERAL", "stashtabMacro") == "yes" else False
)


BASIC_SEARCH = read_config("HOTKEYS", "basicSearch")
ADV_SEARCH = read_config("HOTKEYS", "advSearch")
BASE_SEARCH = read_config("HOTKEYS", "searchBase")

OPEN_WIKI = read_config("HOTKEYS", "openWiki")
OPEN_TRADE = read_config("HOTKEYS", "openTrade")

SHOW_INFO = read_config("HOTKEYS", "showInfo")
HIDEOUT = read_config("HOTKEYS", "hideout")


for section in config.sections():
    for (key, value) in config.items(section):
        if not config2.has_option(section, key):
            needs_write = True

if needs_write:
    try:
        settings = open("settings.cfg", "w")
        config2.write(settings)
    finally:
        settings.close()
