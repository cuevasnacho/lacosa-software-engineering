
from pydantic import *
from enum import Enum
from typing import Optional, List, Any
from api.models.user import PlayerIn , get_jugador
from fastapi import FastAPI, HTTPException, APIRouter, Query, status
from fastapi.responses import JSONResponse
from pony.orm import db_session, ObjectNotFound
from db.database import Lobby as db_lobby
from db.database import Player as db_player
#from pony.orm import Set, select
#from definitions import match_status

# debo hacer un endpoint para ingresar a una partida
#verificar que la partida no este llena
#verificar que el estado del usuario permita unirse a la partida
#verificar que el usuario no este ya en la partida
#si todo esta ok, se agrega el usuario a la partida
#deberia usar 2 db session, una para player y una para lobby
#hacer un lobby_pcount + 1
#hacer un player_ingame = True
#obtener el id del match al que se unio
#hacer un match_currentP + 1
#primero debo verificar si la partida existe
#PONER QUE EL JUGADOR NO SEA HOST, PONER IS_HOST DE TRUE A FALSE
#para modificar una instancia de player

router = APIRouter()

class PlayersLobbyList(BaseModel):
    player_name: str
    player_isHost: bool

def player_in_lobby(player_id : int):
    player_info = db_player[player_id]
    return {"player_name": player_info.player_name, "player_isHost": player_info.player_isHost}

#verifico si la partida existe:

@db_session()
def get_lobby(lobby_id):
    try:
        lobby = db_lobby[lobby_id]
        return lobby
    except ObjectNotFound:
        message = "El lobby no existe"
        status_code = 404 # not found
        return JSONResponse(content = message, status_code = status_code)

@router.put("/lobbys/{lobby_id}")
async def Unirse_Lobby(lobby_id : int, player_id : int) -> List[PlayersLobbyList]:
    players_list = []
    lobby = get_lobby(lobby_id)
    player = get_jugador(player_id)
    if lobby.lobby_pcount + 1 == lobby.lobby_max:
        message = "El lobby esta lleno"
        status_code = 406
        return JSONResponse(content=message, status_code=status_code)
    with db_session:
        player_get = db_player[player_id]
        lobby_get = db_lobby[lobby_id]

        player_get.player_ingame = True
        player_get.player_isHost = False
        lobby_get.lobby_pcount = lobby_get.lobby_pcount + 1
       #player_get.player_lobby.add(lobby_get) #agrego el jugador al lobby
        lobby_get.lobby_player.add(player_get)
        listed_players = list(db_player.select(lambda p: p.player_lobby))

        for i in listed_players:
            player_info = player_in_lobby(i.player_id)
            players_list.append(player_info)

        print(lobby_get.lobby_player.copy())
        print(listed_players)
        print(players_list)
        return players_list

#en db_session, vez de hacer un db_player, tomo el id del jugador y modifico los campos que quiero
