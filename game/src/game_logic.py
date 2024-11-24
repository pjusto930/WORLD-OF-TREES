# game_logic.py
import pygame
import random
from entities import Tire, WaterDrop

def create_tires(tires_group, level):
    tire_count = 5 if level == 'easy' else 10
    for _ in range(tire_count):
        tire = Tire()
        tires_group.add(tire)

def handle_collisions(player, tires, water_drops):
    tire_hits = pygame.sprite.spritecollide(player, tires, False)
    if tire_hits:
        player.health -= 10
        for tire in tire_hits:
            tire.reset_position()
    
    if player.health <= 0:
        return "game_over"
    
    water_hits = pygame.sprite.spritecollide(player, water_drops, True)
    if water_hits:
        player.health = min(player.health + 5, 100)
    return "continue"
