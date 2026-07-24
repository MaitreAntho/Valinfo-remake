import time
from src.i18n import t


class Coregame:
    def __init__(self, Requests, log):
        self.log = log

        self.Requests = Requests

        self.response = ""

    def get_coregame_match_id(self):
        try:
            self.response = self.Requests.fetch(url_type="glz", endpoint=f"/core-game/v1/players/{self.Requests.puuid}", method="get")
            if self.response.get("errorCode") == "RESOURCE_NOT_FOUND":
                return 0
            match_id = self.response['MatchID']
            self.log(f"retrieved coregame match id: '{match_id}'")
            return match_id
        except (KeyError, TypeError):
            self.log(f"cannot find coregame match id: ")
            time.sleep(5)
            try:
                self.response = self.Requests.fetch(url_type="glz", endpoint=f"/core-game/v1/players/{self.Requests.puuid}", method="get")
                match_id = self.response['MatchID']
                self.log(f"retrieved coregame match id: '{match_id}'")
                return match_id
            except (KeyError, TypeError):
                self.log(f"cannot find coregame match id: ")
                print(t("no_match_id_found", response=self.response))
            return 0

    def get_coregame_stats(self):
        self.match_id = self.get_coregame_match_id()
        if self.match_id != 0:
            return self.Requests.fetch(url_type="glz", endpoint=f"/core-game/v1/matches/{self.match_id}", method="get")
        else:
            return None
