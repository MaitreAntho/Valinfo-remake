import traceback
import requests
import urllib3
import os
import sys
import time
import asyncio
import threading
from InquirerPy import inquirer
from src.constants import *
from src.requestsV import Requests
from src.logs import Logging
from src.config import Config
from src.colors import Colors
from src.rank import Rank
from src.content import Content
from src.names import Names
from src.presences import Presences
from src.Loadouts import Loadouts
from src.websocket import Ws
from src.states.menu import Menu
from src.states.pregame import Pregame
from src.states.coregame import Coregame
from src.table import Table
from src.server import Server
from src.errors import Error
from src.stats import Stats
from src.configurator import configure
from src.player_stats import PlayerStats
from src.chatlogs import ChatLogging
from src.rpc import Rpc
from src.os import get_os
from src.i18n import t, set_lang, bootstrap_lang_from_config
from colr import color as colr
from rich.console import Console as RichConsole

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bootstrap_lang_from_config()

os.system(f"title VALINFO API STATUS v{version}")

server = ""


def program_exit(status: int):
    log(f"exited program with error code {status}")
    raise sys.exit(status)


def watch_round_score(stop_event, presences_obj, initial_score, log):
    last_score = initial_score
    while not stop_event.is_set():
        try:
            presence = presences_obj.get_presence()
            own_presence = presences_obj.get_private_presence(presence)
            if own_presence is not None and own_presence.get("sessionLoopState") == "INGAME" and own_presence.get("partyOwnerMatchScoreAllyTeam") is not None:
                score = (own_presence["partyOwnerMatchScoreAllyTeam"], own_presence["partyOwnerMatchScoreEnemyTeam"])
                if score != last_score:
                    last_score = score
                    print(color(t("round_score_live", ally=score[0], enemy=score[1]), fore=(200, 200, 200)))
                    log(f"live round score update: {score[0]} - {score[1]}")
        except Exception:
            pass
        stop_event.wait(3)



try:
    Logging = Logging()
    log = Logging.log

    
    if get_os()[1] == False:
        print(t("unsupported_os", os=get_os()[0]) + "\n")
        log(f"Unsupported operating system: {get_os()[0]}\n")
        program_exit(0)
    else:
        log(f"Operating system: {get_os()[0]}\n")

    ChatLogging = ChatLogging()
    chatlog = ChatLogging.chatLog

    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--config":
            configure()
            run_app = inquirer.confirm(
                message=t("configurator_run_prompt"), default=True
            ).execute()
            if run_app:
                os.system('mode 150,35')
                os.system('cls')
            else:
                os._exit(0)
        else:
            os.system('mode 150,35')
            os.system('cls')
    except Exception as e:
        print(t("configurator_error"))
        log(f"configurator encountered an error")
        log(str(traceback.format_exc()))
        input(t("exit_press_enter"))
        os._exit(1)


    ErrorSRC = Error(log)

    Requests = Requests(version, log, ErrorSRC)
    Requests.check_version()
    Requests.check_status()

    cfg = Config(log)
    set_lang(cfg.language)

    content = Content(Requests, log)

    rank = Rank(Requests, log, content, before_ascendant_seasons)
    pstats = PlayerStats(Requests, log, cfg)

    namesClass = Names(Requests, log)

    presences = Presences(Requests, log)


    menu = Menu(Requests, log, presences)
    pregame = Pregame(Requests, log)
    coregame = Coregame(Requests, log)

    Server = Server(log, ErrorSRC)
    Server.start_server()

    agent_dict = content.get_all_agents()
    map_dict = content.get_maps()

    colors = Colors(hide_names, agent_dict, AGENTCOLORLIST)

    loadoutsClass = Loadouts(Requests, log, colors, Server)
    table = Table(cfg, chatlog, log)

    stats = Stats()

    if cfg.get_feature_flag("discord_rpc"):
        rpc = Rpc(map_dict, gamemodes, colors, log)
    else:
        rpc = None

    Wss = Ws(Requests.lockfile, Requests, cfg, colors, hide_names, chatlog, rpc)

    log(f"VALINFO API STATUS v{version}")




    valoApiSkins = requests.get("https://valorant-api.com/v1/weapons/skins")
    gameContent = content.get_content()
    seasonID = content.get_latest_season_id(gameContent)
    lastGameState = ""
    print(color("""
██    ██  █████  ██      ██ ███    ██ ███████  ██████  
██    ██ ██   ██ ██      ██ ████   ██ ██      ██    ██ 
██    ██ ███████ ██      ██ ██ ██  ██ █████   ██    ██ 
 ██  ██  ██   ██ ██      ██ ██  ██ ██ ██      ██    ██ 
  ████   ██   ██ ███████ ██ ██   ████ ██       ██████  
                                                       
                                                       
""", fore=(182, 44, 54)))
    print(color(t("banner_intro"), fore=(255, 253, 205)))
    chatlog(color(t("banner_welcome"), fore=(255, 253, 205)))


    richConsole = RichConsole()

    firstTime = True
    firstPrint = True
    score_thread = None
    score_stop_event = None
    while True:
        table.clear()
        table.set_default_field_names()
        table.reset_runtime_col_flags()

        if score_stop_event is not None:
            score_stop_event.set()
            score_thread.join(timeout=2)
            score_stop_event = None
            score_thread = None

        try:


            if firstTime:
                run = True
                while run:
                    while True:
                        presence = presences.get_presence()
                        if presences.get_private_presence(presence) != None:
                            break
                        time.sleep(5)
                    if cfg.get_feature_flag("discord_rpc"):
                        rpc.set_rpc(presences.get_private_presence(presence))
                    game_state = presences.get_game_state(presence)
                    if game_state != None:
                        run = False
                    time.sleep(2)
                log(f"game state: {game_state}")
            else:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                game_state = loop.run_until_complete(Wss.recconect_to_websocket(game_state))
                log(f"new game state: {game_state}")
                loop.close()
            firstTime = False

        except TypeError:
            raise Exception("Game has not started yet!")

        if True:
            log(f"getting new {game_state} scoreboard")
            lastGameState = game_state
            game_state_dict = {
                "INGAME": color(t("game_state_ingame"), fore=(241, 39, 39)),
                "PREGAME": color(t("game_state_pregame"), fore=(103, 237, 76)),
                "MENUS": color(t("game_state_menus"), fore=(238, 241, 54)),
            }

            if (not firstPrint) and cfg.get_feature_flag("pre_cls"):
                    os.system('cls')

            is_leaderboard_needed = False
            roundScore = ""

            if game_state == "INGAME":
                coregame_stats = coregame.get_coregame_stats()
                if coregame_stats == None:
                    continue
                Players = coregame_stats["Players"]
                presence = presences.get_presence()
                partyMembers = menu.get_party_members(Requests.puuid, presence)
                partyMembersList = [a["Subject"] for a in partyMembers]

                own_presence = presences.get_private_presence(presence)
                if own_presence is not None and own_presence.get("partyOwnerMatchScoreAllyTeam") is not None:
                    roundScore = f" | {own_presence['partyOwnerMatchScoreAllyTeam']} - {own_presence['partyOwnerMatchScoreEnemyTeam']}"
                else:
                    roundScore = ""

                players_data = {}
                players_data.update({"ignore": partyMembersList})
                for player in Players:
                    if player["Subject"] == Requests.puuid:
                        if cfg.get_feature_flag("discord_rpc"):
                            rpc.set_data({"agent": player["CharacterID"]})
                    players_data.update({player["Subject"]: {"team": player["TeamID"], "agent": player["CharacterID"], "streamer_mode": player["PlayerIdentity"]["Incognito"]}})
                Wss.set_player_data(players_data)

                try:
                    server = GAMEPODS[coregame_stats["GamePodID"]]
                except KeyError:
                    server = t("new_server")
                presences.wait_for_presence(namesClass.get_players_puuid(Players))
                names = namesClass.get_names_from_puuids(Players)
                loadouts = loadoutsClass.get_match_loadouts(coregame.get_coregame_match_id(), Players, cfg.weapon, valoApiSkins, names, state="game")
                isRange = False
                playersLoaded = 1
                with richConsole.status(t("loading_players")) as status:
                    partyOBJ = menu.get_party_json(namesClass.get_players_puuid(Players), presence)
                    Players.sort(key=lambda Players: Players["PlayerIdentity"].get("AccountLevel"), reverse=True)
                    Players.sort(key=lambda Players: Players["TeamID"], reverse=True)
                    partyCount = 0
                    partyIcons = {}
                    lastTeamBoolean = False
                    lastTeam = "Red"


                    already_played_with = []
                    stats_data = stats.read_data()

                    for p in Players:
                        if p["Subject"] == Requests.puuid:
                            allyTeam = p["TeamID"]
                    for player in Players:
                        status.update(t("loading_status", loaded=playersLoaded, total=len(Players)))
                        playersLoaded += 1

                        if player["Subject"] in stats_data.keys():
                            if player["Subject"] != Requests.puuid and player["Subject"] not in partyMembersList:
                                curr_player_stat = stats_data[player["Subject"]][-1]
                                i = 1
                                while curr_player_stat["match_id"] == coregame.match_id and len(stats_data[player["Subject"]]) > i:
                                    i+=1
                                    curr_player_stat = stats_data[player["Subject"]][-i]
                                if curr_player_stat["match_id"] != coregame.match_id:
                                    times = 0
                                    m_set = ()
                                    for m in stats_data[player["Subject"]]:
                                        if m["match_id"] != coregame.match_id and m["match_id"] not in m_set:
                                            times += 1
                                            m_set += (m["match_id"],)
                                    if player["PlayerIdentity"]["Incognito"] == False:
                                        already_played_with.append(
                                                {
                                                    "times": times,
                                                    "name": curr_player_stat["name"],
                                                    "agent": curr_player_stat["agent"],
                                                    "time_diff": time.time() - curr_player_stat["epoch"]
                                                })
                                    else:
                                        if player["TeamID"] == allyTeam:
                                            team_string = t("team_yours")
                                        else:
                                            team_string = t("team_enemy")
                                        already_played_with.append(
                                                {
                                                    "times": times,
                                                    "name": t("agent_on_team", agent=agent_dict[player["CharacterID"].lower()], team=team_string),
                                                    "agent": curr_player_stat["agent"],
                                                    "time_diff": time.time() - curr_player_stat["epoch"]
                                                })

                        party_icon = ''

                        for party in partyOBJ:
                            if player["Subject"] in partyOBJ[party]:
                                if party not in partyIcons:
                                    partyIcons.update({party: PARTYICONLIST[partyCount]})
                                    party_icon = PARTYICONLIST[partyCount]
                                    partyCount += 1
                                else:
                                    party_icon = partyIcons[party]
                        playerRank = rank.get_rank(player["Subject"], seasonID)
                        if player["Subject"] == Requests.puuid:
                            if cfg.get_feature_flag("discord_rpc"):
                                rpc.set_data({"rank": playerRank["rank"], "rank_name": colors.escape_ansi(NUMBERTORANKS[playerRank["rank"]]) + " | " + str(playerRank["rr"]) + "rr"})

                        ppstats = pstats.get_stats(player["Subject"])
                        hs = ppstats["hs"]
                        kd = ppstats["kd"]

                        player_level = player["PlayerIdentity"].get("AccountLevel")



                        if player["PlayerIdentity"]["Incognito"]:
                            Namecolor = colors.get_color_from_team(player["TeamID"],
                                                            names[player["Subject"]],
                                                            player["Subject"], Requests.puuid, agent=player["CharacterID"], party_members=partyMembersList)
                        else:
                            Namecolor = colors.get_color_from_team(player["TeamID"],
                                                            names[player["Subject"]],
                                                            player["Subject"], Requests.puuid, party_members=partyMembersList)
                        if lastTeam != player["TeamID"]:
                            if lastTeamBoolean:
                                table.add_empty_row()
                        lastTeam = player['TeamID']
                        lastTeamBoolean = True
                        if player["PlayerIdentity"]["HideAccountLevel"]:
                            if player["Subject"] == Requests.puuid or player["Subject"] in partyMembersList or hide_levels == False:
                                PLcolor = colors.level_to_color(player_level)
                            else:
                                PLcolor = ""
                        else:
                            PLcolor = colors.level_to_color(player_level)
                        agent = colors.get_agent_from_uuid(player["CharacterID"].lower())
                        if agent == "" and len(Players) == 1:
                            isRange = True

                        name = Namecolor

                        skin = loadouts[player["Subject"]]

                        rankName = NUMBERTORANKS[playerRank["rank"]]

                        rr = playerRank["rr"]
                        
                        peakRankAct = f" (e{playerRank['peakrankep']}a{playerRank['peakrankact']})"
                        if not cfg.get_feature_flag("peak_rank_act"):
                            peakRankAct = ""

                        peakRank = NUMBERTORANKS[playerRank["peakrank"]] + peakRankAct

                        leaderboard = playerRank["leaderboard"]

                        hs = colors.get_hs_gradient(hs)
                        wr = colors.get_wr_gradient(playerRank["wr"]) + f" ({playerRank['numberofgames']})"

                        if(int(leaderboard)>0):
                            is_leaderboard_needed = True
                            
                        level = PLcolor
                        table.add_row_table([party_icon,
                                              agent,
                                              name,
                                              skin,
                                              rankName,
                                              rr,
                                              peakRank,
                                              leaderboard,
                                              hs,
                                              wr,
                                              kd,
                                              level
                                              ])
                        stats.save_data(
                            {
                                player["Subject"]: {
                                    "name": names[player["Subject"]],
                                    "agent": agent_dict[player["CharacterID"].lower()],
                                    "map": map_dict.get(coregame_stats["MapID"].lower()),
                                    "rank": playerRank["rank"],
                                    "rr": rr,
                                    "match_id": coregame.match_id,
                                    "epoch": time.time(),
                                }
                            }
                        )
                        
            elif game_state == "PREGAME":
                already_played_with = []
                pregame_stats = pregame.get_pregame_stats()
                if pregame_stats == None:
                    continue
                try:
                    server = GAMEPODS[pregame_stats["GamePodID"]]
                except KeyError:
                    server = t("new_server")
                Players = pregame_stats["AllyTeam"]["Players"]
                presences.wait_for_presence(namesClass.get_players_puuid(Players))
                names = namesClass.get_names_from_puuids(Players)
                playersLoaded = 1
                with richConsole.status(t("loading_players")) as status:
                    presence = presences.get_presence()
                    partyOBJ = menu.get_party_json(namesClass.get_players_puuid(Players), presence)
                    partyMembers = menu.get_party_members(Requests.puuid, presence)
                    partyMembersList = [a["Subject"] for a in partyMembers]
                    Players.sort(key=lambda Players: Players["PlayerIdentity"].get("AccountLevel"), reverse=True)
                    partyCount = 0
                    partyIcons = {}
                    for player in Players:
                        status.update(t("loading_status", loaded=playersLoaded, total=len(Players)))
                        playersLoaded += 1
                        party_icon = ''

                        for party in partyOBJ:
                            if player["Subject"] in partyOBJ[party]:
                                if party not in partyIcons:
                                    partyIcons.update({party: PARTYICONLIST[partyCount]})
                                    party_icon = PARTYICONLIST[partyCount]
                                    partyCount += 1
                                else:
                                    party_icon = partyIcons[party]
                        playerRank = rank.get_rank(player["Subject"], seasonID)

                        if player["Subject"] == Requests.puuid:
                            if cfg.get_feature_flag("discord_rpc"):
                                rpc.set_data({"rank": playerRank["rank"], "rank_name": colors.escape_ansi(NUMBERTORANKS[playerRank["rank"]]) + " | " + str(playerRank["rr"]) + "rr"})

                        ppstats = pstats.get_stats(player["Subject"])
                        hs = ppstats["hs"]
                        kd = ppstats["kd"]

                        player_level = player["PlayerIdentity"].get("AccountLevel")
                        if player["PlayerIdentity"]["Incognito"]:
                            NameColor = colors.get_color_from_team(pregame_stats['Teams'][0]['TeamID'],
                                                            names[player["Subject"]],
                                                            player["Subject"], Requests.puuid, agent=player["CharacterID"], party_members=partyMembersList)
                        else:
                            NameColor = colors.get_color_from_team(pregame_stats['Teams'][0]['TeamID'],
                                                            names[player["Subject"]],
                                                            player["Subject"], Requests.puuid, party_members=partyMembersList)

                        if player["PlayerIdentity"]["HideAccountLevel"]:
                            if player["Subject"] == Requests.puuid or player["Subject"] in partyMembersList or hide_levels == False:
                                PLcolor = colors.level_to_color(player_level)
                            else:
                                PLcolor = ""
                        else:
                            PLcolor = colors.level_to_color(player_level)
                        if player["CharacterSelectionState"] == "locked":
                            agent_color = color(str(agent_dict.get(player["CharacterID"].lower())),
                                                fore=(255, 255, 255))
                        elif player["CharacterSelectionState"] == "selected":
                            agent_color = color(str(agent_dict.get(player["CharacterID"].lower())),
                                                fore=(128, 128, 128))
                        else:
                            agent_color = color(str(agent_dict.get(player["CharacterID"].lower())), fore=(54, 53, 51))

                        agent = agent_color

                        name = NameColor

                        rankName = NUMBERTORANKS[playerRank["rank"]]

                        rr = playerRank["rr"]

                        peakRankAct = f" (e{playerRank['peakrankep']}a{playerRank['peakrankact']})"
                        if not cfg.get_feature_flag("peak_rank_act"):
                            peakRankAct = ""
                        peakRank = NUMBERTORANKS[playerRank["peakrank"]] + peakRankAct

                        leaderboard = playerRank["leaderboard"]

                        hs = colors.get_hs_gradient(hs)
                        wr = colors.get_wr_gradient(playerRank["wr"]) + f" ({playerRank['numberofgames']})"

                        if(int(leaderboard)>0):
                            is_leaderboard_needed = True

                        level = PLcolor

                        table.add_row_table([party_icon,
                                              agent,
                                              name,
                                              "",
                                              rankName,
                                              rr,
                                              peakRank,
                                              leaderboard,
                                              hs,
                                              wr,
                                              kd,
                                              level,
                                              ])
            if game_state == "MENUS":
                already_played_with = []
                Players = menu.get_party_members(Requests.puuid, presence)
                names = namesClass.get_names_from_puuids(Players)
                playersLoaded = 1
                with richConsole.status(t("loading_players")) as status:
                    Players.sort(key=lambda Players: Players["PlayerIdentity"].get("AccountLevel"), reverse=True)
                    seen = []
                    for player in Players:

                        if player not in seen:
                            status.update(t("loading_status", loaded=playersLoaded, total=len(Players)))
                            playersLoaded += 1
                            party_icon = PARTYICONLIST[0]
                            playerRank = rank.get_rank(player["Subject"], seasonID)

                            if player["Subject"] == Requests.puuid:
                                if cfg.get_feature_flag("discord_rpc"):
                                    rpc.set_data({"rank": playerRank["rank"], "rank_name": colors.escape_ansi(NUMBERTORANKS[playerRank["rank"]]) + " | " + str(playerRank["rr"]) + "rr"})

                            ppstats = pstats.get_stats(player["Subject"])
                            hs = ppstats["hs"]
                            kd = ppstats["kd"]

                            player_level = player["PlayerIdentity"].get("AccountLevel")
                            PLcolor = colors.level_to_color(player_level)

                            agent = ""

                            name = color(names[player["Subject"]], fore=(76, 151, 237))

                            rankName = NUMBERTORANKS[playerRank["rank"]]

                            rr = playerRank["rr"]

                            peakRankAct = f" (e{playerRank['peakrankep']}a{playerRank['peakrankact']})"
                            if not cfg.get_feature_flag("peak_rank_act"):
                                peakRankAct = ""

                            peakRank = NUMBERTORANKS[playerRank["peakrank"]] + peakRankAct

                            leaderboard = playerRank["leaderboard"]

                            hs = colors.get_hs_gradient(hs)
                            wr = colors.get_wr_gradient(playerRank["wr"]) + f" ({playerRank['numberofgames']})"

                            if(int(leaderboard)>0):
                                is_leaderboard_needed = True

                            level = PLcolor

                            table.add_row_table([party_icon,
                                                agent,
                                                name,
                                                "",
                                                rankName,
                                                rr,
                                                peakRank,
                                                leaderboard,
                                                hs,
                                                wr,
                                                kd,
                                                level
                                                ])
                    seen.append(player["Subject"])
            if (title := game_state_dict.get(game_state)) is None:
                time.sleep(9)
            if server != "":
                table.set_title(f"{t('title_valorant_status', title=title, score=roundScore)} {colr('- ' + server, fore=(200, 200, 200))}")
            else:
                table.set_title(t("title_valorant_status", title=title, score=roundScore))
            server = ""
            if title is not None:
                if cfg.get_feature_flag("auto_hide_leaderboard") and (not is_leaderboard_needed):
                    table.set_runtime_col_flag('pos', False)

                if game_state == "MENUS":
                    table.set_runtime_col_flag('party', False)
                    table.set_runtime_col_flag('agent',False)
                    table.set_runtime_col_flag('skin',False)

                if game_state == "INGAME":
                    if isRange:
                        table.set_runtime_col_flag('party', False)
                        table.set_runtime_col_flag('agent',False)

                table.set_caption(f"VALINFO API STATUS v{version}")
                table.display()
                firstPrint = False

                if game_state == "INGAME" and own_presence is not None and own_presence.get("partyOwnerMatchScoreAllyTeam") is not None:
                    initial_score = (own_presence["partyOwnerMatchScoreAllyTeam"], own_presence["partyOwnerMatchScoreEnemyTeam"])
                    score_stop_event = threading.Event()
                    score_thread = threading.Thread(
                        target=watch_round_score,
                        args=(score_stop_event, presences, initial_score, log),
                        daemon=True
                    )
                    score_thread.start()

                if cfg.get_feature_flag("last_played"):
                    if len(already_played_with) > 0:
                        print("\n")
                        for played in already_played_with:
                            msg = t("already_played_with", name=played['name'], agent=played['agent'], time=stats.convert_time(played['time_diff']), times=played['times'])
                            print(msg)
                            chatlog(msg)
                already_played_with = []
        if cfg.cooldown == 0:
            input(t("cooldown_press_enter"))
        else:
        
            pass
except KeyboardInterrupt:
    os._exit(0)
except:
    log(traceback.format_exc())
    fatal_msg = t("fatal_error", path=os.getcwd())
    print(color(fatal_msg, fore=(255, 0, 0)))
    chatlog(color(fatal_msg, fore=(255, 0, 0)))
    input(t("exit_press_enter"))
    os._exit(1)
