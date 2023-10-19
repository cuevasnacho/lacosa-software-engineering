
from pony.orm import db_session, commit
from db.database import Player,Card
from definitions import cards_subtypes
from fastapi.responses import JSONResponse
import random

from abc import ABC, abstractmethod

#chequa que el jugador sea alguno del costado
def adjacent_players(player_cause_id,target_id):
    cause = Player.get(player_id = player_cause_id)
    target = Player.get(player_id = target_id)
    match_id = cause.player_current_match_id.match_id
    if cause == None or target== None:
        return False
    player_counter = cause.player_lobby.lobby_pcount

    cause_position = cause.player_position
    target_position = target.player_position
    if (target.player_dead == True):
        return False
    
    left = (cause_position - 1) % player_counter 
    right = (cause_position + 1) % player_counter
    player_left = Player.select (lambda p: p.player_current_match_id.match_id == match_id and p.player_position == left).first()
    player_right = Player.select (lambda p: p.player_current_match_id.match_id == match_id and p.player_position == right).first()
    while player_left.player_dead == True:
        left = (left - 1) % player_counter
    while player_right.player_dead == True:
        right = (right + 1) % player_counter

    return left == target_position   or right == target_position  

class card_template(ABC):
    def __init__(self,isPanic,alejate_type,effect,name) -> None:
        self.type = isPanic
        self.alejate_type = alejate_type
        self.effect = effect
        self.name = name
    @abstractmethod
    def valid_play(objective_id,player_cause_id): #si no hya condiciones necesarias para jugar la carta, devuelve false o true
        pass

    @abstractmethod
    def aplicar_efecto(objective_id,player_cause_id): #se añade pĺayer_id para indicar el jugador que causo la jugada
        pass

lanz_Effdect = "Eliminar el jugador objetivo"

class lanzallamas_T(card_template):
    def __init__(self):
        super().__init__(False, cards_subtypes.ACTION.value,lanz_Effdect,"lanzallamas")
    def valid_play(objective_id, player_cause_id):
        pass

    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id):
        objective_player = Player.get(player_id = objective_id)
        objective_player.player_dead = True
        commit()
        return []
        
cosa_Effect = "something"

class laCosa_T(card_template):

    def __init__(self):
        super().__init__(False, cards_subtypes.INFECTION.value,cosa_Effect,"lacosa")
    def valid_play(objective_id, player_cause_id):
        pass

    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id):
        return []


nada_de_barbacoas_effect = "Anula carta Lanzallamas"

class NadaDeBarbacoa(card_template):
    def __init__(self):
        super().__init__(False,cards_subtypes.DEFENSE.value,nada_de_barbacoas_effect,"nada_de_barbacoas")

    def valid_play(objective_id, player_cause_id):
        pass
    
    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id):
        objective_player = Player.get(player_id = objective_id)
        objective_player.player_dead = False
        commit()
        return []

sospecha_effect = "Muestra carta aleatoria de un jugador adyacente"

class Sospecha(card_template):
    def __init__(self):
        super().__init__(False,cards_subtypes.ACTION.value,sospecha_effect,"sospecha")
    
    @db_session
    def valid_play(self,player_cause_id,target_id):
        return adjacent_players(player_cause_id,target_id)
    
    @db_session
    def aplicar_efecto(self,target_id,player_cause_id):
        player_target = Player.get(player_id = target_id)
        deck_cards = Card.select(lambda c : c.card_player.player_id == target_id).random(1)[0]
        return [deck_cards.card_cardT.cardT_name]
    
analisis_effect = "Muestra todas las cartas del jugador adyacente"

class Analisis(card_template):
    def __init__(self):
        super().__init__(False,cards_subtypes.ACTION.value,sospecha_effect,"analisis")
    
    def valid_play(objective_id, player_cause_id):
        return adjacent_players(player_cause_id,target_id)
    @db_session
    def aplicar_efecto(self,target_id,player_cause_id):
        list_of_cards = []
        player_target = Player.get(player_id = target_id)
        deck_cards = Card.select(lambda c : c.card_player.player_id == target_id)
        for cards in deck_cards:
            list_of_cards.append(deck_cards.card_cardT.cardT_name)
        return list_of_cards



