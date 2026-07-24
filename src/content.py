import requests

ROMAN_NUMERALS = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}

class Content():
    def __init__(self, Requests, log):
        self.Requests = Requests
        self.log = log
        self.content = {}

    def get_content(self):
        self.content = self.Requests.fetch("custom", f"https://shared.{self.Requests.region}.a.pvp.net/content-service/v3/content", "get")
        return self.content

    def get_latest_season_id(self, content):
        for season in content["Seasons"]:
            if season["IsActive"] and season["Type"] == "act":
                self.log(f"retrieved season id: {season['ID']}")
                return season["ID"]

    def get_all_agents(self):
        rAgents = requests.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true").json()
        agent_dict = {}
        agent_dict.update({None: None})
        agent_dict.update({"": ""})
        for agent in rAgents["data"]:
            agent_dict.update({agent['uuid'].lower(): agent['displayName']})
        self.log(f"retrieved agent dict: {agent_dict}")
        return agent_dict

    def get_maps(self):
        rMaps = requests.get("https://valorant-api.com/v1/maps").json()
        map_dict = {}
        map_dict.update({None: None})
        for Vmap in rMaps["data"]:
            map_dict.update({Vmap['mapUrl'].lower(): Vmap['displayName']})
        self.log(f"retrieved map dict: {map_dict}")
        return map_dict

    def get_act_episode_from_act_id(self, act_id):
        final = {
            "act": None,
            "episode": None
        }
        act_found = False
        for season in self.content["Seasons"]:
            if season["ID"].lower() == act_id.lower():
                act_name = season["Name"].strip().split()[-1]
                final["act"] = ROMAN_NUMERALS.get(act_name)
                act_found = True
            if act_found and season["Type"] == "episode":
                episode_digits = "".join(ch for ch in season["Name"] if ch.isdigit())
                final["episode"] = int(episode_digits) if episode_digits else None
                break
        return final
