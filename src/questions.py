from InquirerPy.base.control import Choice
from src.constants import DEFAULT_CONFIG, WEAPONS
from src.i18n import t

TABLE_OPTS_KEYS = ["skin", "rr", "leaderboard", "peakrank", "headshot_percent", "winrate", "kd"]
FLAGS_OPTS_KEYS = ["last_played", "auto_hide_leaderboard", "pre_cls", "game_chat", "peak_rank_act", "discord_rpc"]


def table_opts():
    return {
        "skin": t("opt_skin"),
        "rr": t("opt_rr"),
        "leaderboard": t("opt_leaderboard"),
        "peakrank": t("opt_peakrank"),
        "headshot_percent": t("opt_headshot_percent"),
        "winrate": t("opt_winrate"),
        "kd": t("opt_kd"),
    }


def flags_opts():
    return {
        "last_played": t("flag_last_played"),
        "auto_hide_leaderboard": t("flag_auto_hide_leaderboard"),
        "pre_cls": t("flag_pre_cls"),
        "game_chat": t("flag_game_chat"),
        "peak_rank_act": t("flag_peak_rank_act"),
        "discord_rpc": t("flag_discord_rpc"),
    }


weapon_question = lambda config: {
        "type": "fuzzy",
        "name": "weapon",
        "message": t("weapon_question_message"),
        "default": config.get("weapon","Vandal"),
        "choices": WEAPONS,
    }

table_question = lambda config: {
        "type": "checkbox",
        "name": "table",
        "message": t("table_question_message"),
        "choices": [
            Choice(k, name=v, enabled=config.get("table",DEFAULT_CONFIG["table"]).get(k, DEFAULT_CONFIG["table"][k]))
            for k, v in table_opts().items()
        ],
        "filter": lambda table: {k: k in table for k in TABLE_OPTS_KEYS},
        "long_instruction": t("checkbox_long_instruction")
    }

port_question = lambda config: {
        "type": "number",
        "name": "port",
        "message": t("port_question_message"),
        "default": config.get("port", 1100),
        "min_allowed":0,
        "max_allowed": 65535,
        "filter": lambda ans: int(ans)
    }

flags_question = lambda config: {
        "type": "checkbox",
        "name": "flags",
        "message": t("flags_question_message"),
        "choices": [
            Choice(k, name=v, enabled=config.get("flags",DEFAULT_CONFIG["flags"]).get(k, DEFAULT_CONFIG["flags"][k]))
            for k, v in flags_opts().items()
        ],
        "filter": lambda flags: {k: k in flags for k in FLAGS_OPTS_KEYS},
        "long_instruction": t("checkbox_long_instruction")
    }

basic_questions = lambda config: [
    weapon_question(config=config),
    table_question(config=config)
]

advance_questions = lambda config: [
    port_question(config=config),
] + basic_questions(config=config)
