import json
import os

from InquirerPy import inquirer, prompt
from InquirerPy.separator import Separator

from src.constants import DEFAULT_CONFIG

from src.questions import *
from src.i18n import t, set_lang, get_lang, bootstrap_lang_from_config

LANGUAGE_CHOICES = ["English", "Français"]
LANGUAGE_CODES = {"English": "en", "Français": "fr"}
LANGUAGE_NAMES = {"en": "English", "fr": "Français"}


def configure():
    bootstrap_lang_from_config()
    default_config = DEFAULT_CONFIG

    try:
        with open("config.json", "r") as openfile:
            user_config = default_config | json.load(openfile)
    except FileNotFoundError:
        print(t("generating_default_config"))
        user_config = default_config
    except json.JSONDecodeError:
        print(t("config_broken"))
        user_config = default_config

    set_lang(user_config.get("language", "en"))

    changed_config = {}
    while True:
        loop_config = user_config | changed_config

        menu_choices = [
            t("menu_language"),
            t("menu_weapon"),
            t("menu_table"),
            t("menu_flags"),
            Separator(),
            t("menu_basic"),
            t("menu_advance"),
            Separator(),
            t("menu_save_exit"),
            t("menu_exit"),
        ]

        choice = inquirer.select(
            message=t("select_option_prompt"),
            choices=menu_choices,
            default=menu_choices[0],
        ).execute()

        if choice is menu_choices[0]:
            current_lang_name = LANGUAGE_NAMES.get(loop_config.get("language", "en"), "English")
            lang_choice = inquirer.select(
                message=t("select_language_prompt"),
                choices=LANGUAGE_CHOICES,
                default=current_lang_name,
            ).execute()
            changed_config["language"] = LANGUAGE_CODES[lang_choice]
            set_lang(changed_config["language"])
        elif choice is menu_choices[1]:
            changed_config |= prompt([weapon_question(config=loop_config)])
        elif choice is menu_choices[2]:
            changed_config |= prompt([table_question(config=loop_config)])
        elif choice is menu_choices[3]:
            changed_config |= prompt([flags_question(config=loop_config)])
        elif choice is menu_choices[5]:
            changed_config |= prompt(basic_questions(config=loop_config))
        elif choice is menu_choices[6]:
            changed_config |= prompt(advance_questions(config=loop_config))
        elif choice is menu_choices[8]:
            proceed=True
            break
        else:
            proceed = (not len(changed_config.keys()) > 0) or inquirer.confirm(
                message=t("save_config_prompt"), default=True
            ).execute()
            break

        os.system('cls')

    if proceed:
        config = default_config | user_config | changed_config
        with open("config.json", "w") as outfile:
            json.dump(config, outfile, indent=4)
    else:
        config = default_config | user_config

    return config
