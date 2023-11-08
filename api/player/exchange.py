from pony.orm import db_session
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.database import Player, Card
from pony.orm import db_session, commit
from api.card.alejate import adjacent_players
from definitions import player_roles

router = APIRouter()

#POSIBLE ERROR ES QUE NO ESTEN CON LOS MISMOS NOMBRES
@db_session
def valid_card(card_id,role):
    if role == player_roles.THE_THING.value:
        not_valid_cards = ["lacosa"]
    elif role == player_roles.HUMAN.value:
        not_valid_cards = ["infectado"] 
    elif role == player_roles.INFECTED.value:
        not_valid_cards = []

    card = Card[card_id]
    if card.card_cardT.cardT_name in not_valid_cards: 
        return False 
    return True

@db_session
def valid_oponent(player_id,oponent_id,role,oponent_at_left,oponent_at_right,card_id,motive):
    oponent = Player[oponent_id]    
    card = Card[card_id]
    oponent = Player[oponent_id]
    oponent_role = oponent.player_role
    valid = True

    if role != player_roles.THE_THING.value:
        player_hand = Card.select(lambda card : card.card_player.player_id == player_id and 
                                    card.card_cardT.cardT_name == "infectado") 
        infect_card = 0
        for card in player_hand:
            infect_card += 1

        #no tengo mas de una carta infectado o no se la doy a la cosa
        if card.card_cardT.cardT_name == "infectado":
            if role == player_roles.INFECTED.value:
                if infect_card <= 1 or oponent_role != player_roles.THE_THING.value:
                    valid = valid and False 

        #no se da el intercambio si tengo todas cartas de infectado -> superinfeccion
        if role == player_roles.HUMAN.value:
            if infect_card == 6:
                valid = valid and False 
    
    #carta no es seducion -> derecha o izq
    if motive != "seduccion":
        if not (oponent_at_left or oponent_at_right): #el jugador no es adyecente
            valid = valid and False 

    #caso puerta atrancada
    if ((not oponent.player_exchangeL) and oponent_at_left) or ((not oponent.player_exchangeR) and oponent_at_right):
        valid = valid and False    

    return valid

@db_session
def have_defense_card(oponent_id):
    defense_cards = ["aterrador","no_gracias","fallaste"]  
    cards = Card.select(lambda card : card.card_player.player_id == oponent_id)
    for card in cards : 
        if card.card_cardT.cardT_name in defense_cards:
            return True 
    return False

#encargado de ver si se cumplen todas las condiciones para poder intercambiar
#motive : motivo del intercambio, si es una carta es su nombre si es por intercambio normal es "intercambio"
@router.get("/intercambio/valido/{player_id}/{oponent_id}/{player_card_id}/{motive}")
async def exchange_valid(player_id : int, oponent_id : int, player_card_id : int, motive : str):
    with db_session:
        try: 
            player = Player[player_id]
        except:
            content = "El objeto no existe"
            return JSONResponse(content = content, status_code = 404)
        
        oponent_position = adjacent_players(player_id,oponent_id) 
        is_card_valid = valid_card(player_card_id,player.player_role)
        is_oponent_valid = valid_oponent(player_id,oponent_id,player.player_role,oponent_position[0],oponent_position[1],player_card_id,motive)
        #mandar mensaje por soccket
        exchange = is_card_valid and is_oponent_valid
        return JSONResponse(content = exchange, status_code = 200)

#encargado solamente de chequear si se puede defender
@router.get("/intercambio/defensa/{player_defense_id}")
async def exchange_defense(player_defense_id : int): 
    defense = have_defense_card(player_defense_id)
    return JSONResponse(content = defense, status_code = 200)

#swap de cartas 
@router.put("/intercambio/cartas/{player_id}/{card1_id}/{oponent_id}/{card2_id}")
async def swap_cards(player_id : int, card1_id : int, oponent_id : int, card2_id : int):
    with db_session :
        try: 
            player = Player[player_id]
            oponent = Player[oponent_id]
            player_card = Card.get(card_id = card1_id)
            oponent_card = Card.get(card_id = card2_id)
        except:
            content = "El objeto no existe"
            return JSONResponse(content = content, status_code = 404)

        player_card.card_player = oponent_id
        oponent_card.card_player = player_id
        commit()

        if player.player_quarentine_count > 0 :
            #MANDAR MENSAJE POR SOQUET DE LA NUEVA CARTA
            pass
        if oponent.player_quarentine_count > 0:
            #MANDAR MENSAJE POR SOQUET DE LA NUEVA CARTA
            pass
        content = "Cambio realizado"
        return JSONResponse(content = content, status_code = 200)
