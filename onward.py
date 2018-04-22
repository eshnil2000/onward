import pygame
import random

import logic
import graphics
import entities
import data


class Game:

    def __init__(self):
        self.seed = 0
        self.player = None
        self.running = True
        self.level = 0
        self.height_map = []
        self.creatures = []
        self.items = []
        self.bullets = []  # List of lists indicating positions
        self.clock = pygame.time.Clock()
        self.highscore = 0
        self.camera = graphics.Camera()

        self.transition_period = False
        self.transition_counter = 0
        self.time_of_day = "day"
        self.period_countdown = 0

        self.level_transition = False
        self.level_transition_countdown = 0

    def handle_input(self):

        # Handle mouse presses and exit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    bullets = self.player.shoot(x, y)
                    self.bullets.append(bullets)
                if event.button == 4:
                    self.player.change_weapon("prev")
                elif event.button == 5:
                    self.player.change_weapon("next")

        # Handle continuous keyboard input
        kb_input = pygame.key.get_pressed()

        if kb_input[pygame.K_UP]:
            self.player.jump()
        if kb_input[pygame.K_LEFT]:
            self.player.move(-2, 0)
        if kb_input[pygame.K_RIGHT]:
            self.player.move(2, 0)
        if kb_input[pygame.K_f]:
            self.camera.toggle_fullscreen()

    def update(self):
        logic.spawn_monsters(self.player.x, self.level*100, self.creatures)
        logic.update_physics(self.creatures, self.bullets, self.height_map)
        logic.update_ai(self.creatures, self.player)
        logic.update_game_logic(self.creatures, self.items, self.player, self)

    def draw(self):
        self.camera.set_focus(self.player.x, self.player.y)
        self.camera.render(self)

    def next_level(self):
        self.level += 1
        self.height_map = self.generate_height_map(100*self.level+100)
        self.camera.set_biome(random.choice(["normal", "jungle", "desert"]))
        self.player = entities.Creature(10, 0, 16)
        self.creatures = [self.player]
        self.bullets = []

    def generate_height_map(self, width, seed=0):
        height_map = [0]
        for x in range(1, width):
            new_point = height_map[x-1] + random.randint(-2, 2)
            height_map.append(new_point)
        return height_map

    def run(self):
        self.next_level()
        self.camera.show_title_screen()
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick_busy_loop()
        pygame.quit()
        exit(0)


Game().run()
