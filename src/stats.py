import os
import time
import json
from src.i18n import t

class Stats:
    def __init__(self):
        pass

    def save_data(self, data):
        try:
            os.mkdir(os.path.join(os.getenv('APPDATA'), "valinfo"))
        except FileExistsError:
            pass
        try:
            with open(os.path.join(os.getenv('APPDATA'), "valinfo/stats.json"), "r") as f:
                original_data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            original_data = {}

        updated_data = original_data.copy()
        for puuid in data.keys():
            if original_data.get(puuid) is None:
                updated_data.update({puuid: [data[puuid]]})
            else:
                updated_data[puuid].append(data[puuid])
        

        with open(os.path.join(os.getenv('APPDATA'), "valinfo/stats.json"), "w") as f:
            json.dump(updated_data, f)
    
    def read_data(self):
        try:
            with open(os.path.join(os.getenv('APPDATA'), "valinfo/stats.json"), "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return {}

    def convert_time(self, s):
        s = int(s)
        if s < 60:
            return t("time_second" if s == 1 else "time_seconds", n=s)
        elif s < 3600:
            minutes = s // 60
            return t("time_minute" if minutes == 1 else "time_minutes", n=minutes)
        elif s < 86400:
            hours = s // 3600
            return t("time_hour" if hours == 1 else "time_hours", n=hours)
        else:
            days = s // 86400
            return t("time_day" if days == 1 else "time_days", n=days)
