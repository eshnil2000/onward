import random
import time
from data import Point
import pygame
from entities import Creature


def update_game_logic(entities, items, player, game):

    if player.health < 100.0:
        player.health += 0.05

    if entity_collision(player, entities):
        player.health -= 1 / 60

    for entity in entities:
        # Leveling up
        if entity.experience > 50:
            entity.level += 1
            entity.experience = 0

        # Health and player death
        if entity.health <= 0:
            if entity == player:
                game.camera.draw_game_over()
                time.sleep(2)
                game.Set_Level(1)
                highscore = 0
                return
            else:
                highscore += npc.size
                game.npcs.remove(npc)
                deadnpcs.append(npc)

        # Entity death
        if entity.state == "dead":
            if entity.death_timer > 85:
                entity.y -= 3
            elif 0 < entity.death_timer <= 85:
                entity.y += 3
            elif entity.death_timer <= 0:
                pass
                # TODO deadnpcs.remove(npc)

            entity.death_timer -= 1

        # Weapon cooldown timer
        if entity.cooldown_period > 0:
            entity.cooldown_period -=1

    for item in items:
        if item.type == "experience" and entity_collision(player, item):
            player.experience += item.quantity

    # Day/night
    if not game.transition_period: game.period_countdown += 1

    if game.transition_period:
        if game.time_of_day == 'day': game.transition_counter += 1
        elif game.time_of_day == 'night': game.transition_counter += 1
        if game.transition_counter == 1500: timefase = False
    elif not game.transition_period:
        if game.time_of_day == 'day' and game.period_countdown == 3600:
            game.time_of_day = 'night'
            game.transition_period = True
            game.transition_counter = 0
            game.period_countdown = 0
        elif game.time_of_day == 'night' and game.period_countdown == 3600:
            game.time_of_day = 'day'
            game.transition_period = True
            game.transition_counter = 0
            game.period_countdown = 0

    # Level advancing
    if game.player.x >= (game.level * 100) * game.camera.block_size:
        game.level_transition = True
        for npc in game.creatures:
            if npc != game.player:
                npc.health = 0

    if game.level_transition:
        game.level_transition_countdown += 1
        if game.level_transition_countdown > 300:
            game.Set_Level(game.level + 1)
            game.level_transition_countdown = 0
            game.highscore += game.level * 100
            game.level_switch = False


def update_physics(creatures, bullets, height_map):
    for entity in creatures + bullets:
        # Implement gravity
        if not map_collision(entity, height_map) and not entity.type == "bullet":
            entity.y_velocity += 1

        # Update position and reduce velocity
        if not map_collision(entity, height_map):
            entity.x += entity.x_velocity
            entity.y += entity.y_velocity
            entity.x_velocity -= 1
            entity.y_velocity -= 1


def update_ai(entities, player):
    line_of_sight = 200
    danger_zone = 100

    for entity in entities:
        if entity == player:
            continue

        if entity.x-line_of_sight < player.x < entity.x+line_of_sight:
            action = "hunt"
        else:
            action = random.choice(["jump", "move", "wait"])

        if action is "hunt":
            if player.x > entity.x:
                entity.move("right")
            elif player.x < entity.x:
                entity.move("left")

            if entity.x-danger_zone < player.x < entity.x+danger_zone:
                entity.shoot(player.x, player.y)
        elif action is "jump":
            entity.jump()
        elif action is "move":
            direction = random.choice(["left", "right"])
            entity.move(direction)


def spawn_monsters(player_x, level_length, creatures):
    die = random.uniform(0,100)
    if die > 99:
        weight_64 = 0.1*(player_x / level_length)
        weight_32 = 1-((player_x/level_length)-weight_64)
        weight_16 = 1-weight_64-weight_32

        sizes = random.choices([16, 32, 64], [weight_16, weight_32, weight_64], k=100)
        size = random.choice(sizes)
        x = random.randint(player_x, level_length)
        creatures.append(Creature(x, 0, size))


def entity_collision(entity, entities):
    for other_entity in entities:
        if entity is other_entity:
            return False
        else:
            if (other_entity.x <= entity.x <= other_entity.x+other_entity.size) \
                    and (other_entity.y <= entity.y <= other_entity.y + other_entity.size):
                return True
            elif (entity.x <= other_entity.x <= entity.x+entity.size) \
                    and (entity.y <= other_entity.y <= entity.y + entity.size):
                return True


def collision_with_bullet(bullet, entities):
    return any(((entity.x <= bullet.x <= entity.x+entity.size) \
                    and (entity.y <= bullet.y <= entity.y + entity.size))for entity in entities)

def map_collision(entity, heightmap):
    if entity.y + entity.y_velocity < 0: return True

    # topleftcorner
    mapx = ((entity.x + entity.x_velocity) & ~15) // 16
    mapy = ((entity.y + entity.y_velocity) & ~15) // 16
    
    if mapx > len(heightmap)-1:
        return True
    if heightmap[mapx] > mapy: return True
    # toprightcorner
    mapx = ((entity.x + (entity.size - 1) + entity.x_velocity) & ~15) // 16
    if heightmap[mapx] > mapy: return True

    return False