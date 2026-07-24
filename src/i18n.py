import json
import os

DEFAULT_LANG = "en"
_current_lang = DEFAULT_LANG

STRINGS = {
    "en": {
        "unsupported_os": "Unsupported operating system: {os}",
        "configurator_run_prompt": "Do you want to run valinfo?",
        "configurator_error": "Something went wrong while running configurator!",
        "banner_intro": "\nThis tool usings the API of Valorant \nNot ban able as it just uses the local client api\n",
        "banner_welcome": "\nWelcome to my world \nDont forget to follow me on instagram @eii3\n",
        "game_state_ingame": "In-Game",
        "game_state_pregame": "Agent Select",
        "game_state_menus": "In-Menus",
        "new_server": "New server",
        "loading_players": "Loading Players...",
        "loading_status": "Loading status of players... [{loaded}/{total}]",
        "team_yours": "your team",
        "team_enemy": "enemy team",
        "agent_on_team": "{agent} on {team}",
        "round_score_live": "Live round score: {ally} - {enemy}",
        "title_valorant_status": "VALORANT status: {title}{score}",
        "already_played_with": "Already played with {name} (last {agent}) {time} ago. (Total played {times} times)",
        "cooldown_press_enter": "Press enter to fetch again...",
        "fatal_error": "Make sure valorant it work, The program has encountered an error. with the logs found in {path}\\logs",
        "exit_press_enter": "press enter to exit...\n",

        "col_party": "Party",
        "col_agent": "Agent",
        "col_name": "Name",
        "col_skin": "Skin",
        "col_rank": "Rank",
        "col_rr": "RR",
        "col_peak_rank": "Peak Rank",
        "col_pos": "Pos.",
        "col_hs": "HS",
        "col_wr": "WR",
        "col_kd": "KD",
        "col_level": "Level",

        "firewall_blocked": """Valinfo is being blocked by the firewall!!
            - Check your firewall settings and whitelist the program / disable firewall
            - Try Restarting vRY and/or VALORANT, if non works try restarting your computer
            - If you have a slower internet connection, changing the value of cooldown located in config.json to 0 or any number greater than 1 may help.
            - If that doesn't work then changing the port number located in config.json file may work.
            - If all the above mentioned steps does not work, please join the support server!.
            """,
        "valorant_not_open": "\nVALORANT is not open that is mean valinfo wont work. Please open valorant\n",

        "new_version_available": "New version available! {link}",
        "update_now_prompt": "Do you want to update now? (Y/n): ",
        "invalid_update_input": 'Invalid input please response with "yes" or "no" ("y", "n") or press enter to update',
        "connection_error_retry": "Connection error, retrying in 5 seconds",

        "no_match_id_found": "No match id found. {response}",

        "generating_default_config": "Generating default configuration",
        "config_broken": "config file maybe broken, using default instead",
        "menu_language": "Language",
        "menu_weapon": "Weapon Selection",
        "menu_table": "Table Customization",
        "menu_flags": "Optional Feature Flags",
        "menu_basic": "Full Basic Config (Suitable for most users)",
        "menu_advance": "Full Advance Config (I know what i am doing!)",
        "menu_save_exit": "Save and Exit Configurator",
        "menu_exit": "Exit Configurator",
        "select_option_prompt": "Please select an option:",
        "save_config_prompt": "Do you want to save new config?",
        "select_language_prompt": "Please select a language:",

        "opt_skin": "Skin",
        "opt_rr": "Ranked Rating",
        "opt_leaderboard": "Leaderboard Position",
        "opt_peakrank": "Peak Rank",
        "opt_headshot_percent": "Headshot Percentage",
        "opt_winrate": "WinRate",
        "opt_kd": "K/D Ratio <!> Last Game Only <!>",

        "flag_last_played": "Last Played Stats",
        "flag_auto_hide_leaderboard": "Auto Hide Leaderboard Column",
        "flag_pre_cls": "Pre-Clear Screen",
        "flag_game_chat": "Print Game Chat",
        "flag_peak_rank_act": "Peak Rank Act",
        "flag_discord_rpc": "Discord Rich Presence",

        "weapon_question_message": "Please select a weapon to show skin for:",
        "table_question_message": "Please select table columns to display:",
        "checkbox_long_instruction": "Press 'space' to toggle selection and 'enter' to submit",
        "port_question_message": "Please enter port for server to run:",
        "flags_question_message": "Please select optional features:",

        "time_second": "{n} second",
        "time_seconds": "{n} seconds",
        "time_minute": "{n} minute",
        "time_minutes": "{n} minutes",
        "time_hour": "{n} hour",
        "time_hours": "{n} hours",
        "time_day": "{n} day",
        "time_days": "{n} days",
    },
    "fr": {
        "unsupported_os": "Système d'exploitation non supporté : {os}",
        "configurator_run_prompt": "Voulez-vous lancer valinfo ?",
        "configurator_error": "Une erreur est survenue lors du lancement du configurateur !",
        "banner_intro": "\nCet outil utilise l'API de Valorant \nAucun risque de ban car il utilise uniquement l'API du client local\n",
        "banner_welcome": "\nBienvenue dans mon monde \nN'oublie pas de me suivre sur instagram @eii3\n",
        "game_state_ingame": "En Partie",
        "game_state_pregame": "Sélection d'Agent",
        "game_state_menus": "Dans les Menus",
        "new_server": "Nouveau serveur",
        "loading_players": "Chargement des joueurs...",
        "loading_status": "Chargement du statut des joueurs... [{loaded}/{total}]",
        "team_yours": "votre équipe",
        "team_enemy": "l'équipe ennemie",
        "agent_on_team": "{agent} dans {team}",
        "round_score_live": "Score en direct : {ally} - {enemy}",
        "title_valorant_status": "Statut VALORANT : {title}{score}",
        "already_played_with": "Déjà joué avec {name} (dernier agent : {agent}) il y a {time}. (Joué {times} fois au total)",
        "cooldown_press_enter": "Appuyez sur Entrée pour actualiser...",
        "fatal_error": "Vérifie que Valorant est bien ouvert. Le programme a rencontré une erreur, les logs se trouvent dans {path}\\logs",
        "exit_press_enter": "Appuyez sur Entrée pour quitter...\n",

        "col_party": "Groupe",
        "col_agent": "Agent",
        "col_name": "Nom",
        "col_skin": "Skin",
        "col_rank": "Rang",
        "col_rr": "RR",
        "col_peak_rank": "Rang Max",
        "col_pos": "Pos.",
        "col_hs": "HS",
        "col_wr": "WR",
        "col_kd": "KD",
        "col_level": "Niveau",

        "firewall_blocked": """Valinfo est bloqué par le pare-feu !!
            - Vérifiez les paramètres de votre pare-feu et autorisez le programme / désactivez le pare-feu
            - Essayez de redémarrer vRY et/ou VALORANT, si rien ne fonctionne essayez de redémarrer votre ordinateur
            - Si votre connexion internet est lente, changer la valeur de cooldown dans config.json à 0 ou un nombre supérieur à 1 peut aider.
            - Si cela ne fonctionne pas, changer le numéro de port dans le fichier config.json peut résoudre le problème.
            - Si aucune des étapes ci-dessus ne fonctionne, rejoignez le serveur de support !
            """,
        "valorant_not_open": "\nVALORANT n'est pas ouvert, valinfo ne fonctionnera donc pas. Veuillez ouvrir valorant\n",

        "new_version_available": "Nouvelle version disponible ! {link}",
        "update_now_prompt": "Voulez-vous mettre à jour maintenant ? (O/n) : ",
        "invalid_update_input": 'Réponse invalide, répondez par "oui" ou "non" ("o", "n") ou appuyez sur Entrée pour mettre à jour',
        "connection_error_retry": "Erreur de connexion, nouvelle tentative dans 5 secondes",

        "no_match_id_found": "Aucun ID de match trouvé. {response}",

        "generating_default_config": "Génération de la configuration par défaut",
        "config_broken": "Le fichier de configuration est peut-être corrompu, utilisation de la configuration par défaut",
        "menu_language": "Langue",
        "menu_weapon": "Sélection de l'arme",
        "menu_table": "Personnalisation du tableau",
        "menu_flags": "Options facultatives",
        "menu_basic": "Configuration Basique Complète (Convient à la plupart des utilisateurs)",
        "menu_advance": "Configuration Avancée Complète (Je sais ce que je fais !)",
        "menu_save_exit": "Sauvegarder et Quitter le Configurateur",
        "menu_exit": "Quitter le Configurateur",
        "select_option_prompt": "Veuillez sélectionner une option :",
        "save_config_prompt": "Voulez-vous sauvegarder la nouvelle configuration ?",
        "select_language_prompt": "Veuillez sélectionner une langue :",

        "opt_skin": "Skin",
        "opt_rr": "Rank Rating",
        "opt_leaderboard": "Position au Classement",
        "opt_peakrank": "Rang Max",
        "opt_headshot_percent": "Pourcentage de Headshot",
        "opt_winrate": "Taux de Victoire",
        "opt_kd": "Ratio K/D <!> Dernière Partie Seulement <!>",

        "flag_last_played": "Statistiques Dernière Partie",
        "flag_auto_hide_leaderboard": "Masquer Auto. la Colonne Classement",
        "flag_pre_cls": "Effacer l'écran avant Affichage",
        "flag_game_chat": "Afficher le Chat en Jeu",
        "flag_peak_rank_act": "Acte du Rang Max",
        "flag_discord_rpc": "Discord Rich Presence",

        "weapon_question_message": "Veuillez sélectionner une arme pour laquelle afficher le skin :",
        "table_question_message": "Veuillez sélectionner les colonnes du tableau à afficher :",
        "checkbox_long_instruction": "Appuyez sur 'espace' pour cocher/décocher et 'entrée' pour valider",
        "port_question_message": "Veuillez entrer le port sur lequel le serveur doit tourner :",
        "flags_question_message": "Veuillez sélectionner les options facultatives :",

        "time_second": "{n} seconde",
        "time_seconds": "{n} secondes",
        "time_minute": "{n} minute",
        "time_minutes": "{n} minutes",
        "time_hour": "{n} heure",
        "time_hours": "{n} heures",
        "time_day": "{n} jour",
        "time_days": "{n} jours",
    },
}


def set_lang(lang):
    global _current_lang
    _current_lang = lang if lang in STRINGS else DEFAULT_LANG


def get_lang():
    return _current_lang


def t(key, **kwargs):
    template = STRINGS.get(_current_lang, {}).get(key)
    if template is None:
        template = STRINGS[DEFAULT_LANG].get(key, key)
    return template.format(**kwargs) if kwargs else template


def bootstrap_lang_from_config(path="config.json"):
    try:
        with open(path, "r") as f:
            lang = json.load(f).get("language", DEFAULT_LANG)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        lang = DEFAULT_LANG
    set_lang(lang)
