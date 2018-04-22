import time
import pygame
from data import Point, load_assets


class Camera:

    def __init__(self):
        self.screen_width = 600
        self.screen_height = 300
        self.window = None
        self.screen = None
        self._pygame_setup()
        self.assets = load_assets()
        self.block_size = 16
        self.focus = Point(0, 0)
        self.biome = "normal"
        self.fullscreen = False

        pygame.display.set_caption('Onward')
        pygame.display.set_icon(self.assets["other"]["icon"])

    def _pygame_setup(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen = pygame.Surface((self.screen_width, self.screen_height))

    def set_focus(self, x, y):
        self.focus = Point(x, y)

    def set_biome(self, biome):
        self.biome = biome

    def show_title_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.assets["other"]["title"], (250, 50))
        self.window.blit(self.screen, (0,0))
        pygame.display.update()
        time.sleep(3)

    def toggle_fullscreen(self):
        if not self.fullscreen:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),
                                              pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))


    def _get_screen_coordinates(self, world_x, world_y):
        spx = (world_x * self.block_size - (self.focus.x - (self.screen_width//2)))
        spy = (world_y * self.block_size - (self.focus.y - (self.screen_height//2)))
        return spx, spy

    def _draw_background(self):
        pass

    def _draw_map(self, heightmap):
        block_screen_width = self.screen_width // self.block_size
        for x in range(max(0, self.focus.x-block_screen_width//2),
                       min(len(heightmap), self.focus.x+block_screen_width//2)):
            spx, spy = self._get_screen_coordinates(x, heightmap[x])
            self.screen.blit(self.assets["tiles"][self.biome + '_grass'], (spx, spy))

            for y in range(spy, spy+10):
                self.screen.blit(self.assets["tiles"][self.biome + '_dirt'], (spx, y))

    def _draw_entities(self, entities):
        # Don't forget to draw damaged enemies
        pass

    def _draw_bullets(self, bullets):
        pass

    def _draw_hud(self, high_score, player):
        WHITE = (255,255,255)
        surface = pygame.Surface((self.screen_width, 40))

        # Draw avatar
        surface.blit(self.assets["other"]["avatar"], (3, 5))

        # Draw health and level
        myfont = pygame.font.SysFont("calibri", 15)
        label = myfont.render("HP", True, WHITE)
        surface.blit(label, (40, 5))
        label = myfont.render("Highscore:", True, WHITE)
        surface.blit(label, (40, 22))

        # Draw hp & lv bars
        myfont = pygame.font.SysFont("calibri", 14)

        pygame.draw.rect(surface, WHITE, (59, 4, 103, 15), 2)
        pygame.draw.rect(surface, (0, 255, 0), (61, 6, player.health, 12), 0)

        label = myfont.render(str(high_score), True, WHITE)
        surface.blit(label, (110, 24))

        # Draw weapon
        pygame.draw.rect(surface, WHITE, (170, 4, 32, 32), 2)
        if player.weapon == 1:
            surface.blit(self.assets["weapons"]["pistol"], (170, 4))
        elif player.weapon == 2:
            surface.blit(self.assets["weapons"]["shotgun"], (170, 4))
        elif player.weapon == 3:
            surface.blit(self.assets["weapons"]["machine_gun"], (170, 4))
        else:
            pass

        # Put HUD on screen
        self.screen.blit(surface, (0, self.screen_height - 40))

        # Draw mouse
        mx, my = pygame.mouse.get_pos()
        self.screen.blit(self.assets["other"]["cursor"], (mx, my))

    def render(self, game):
        self.screen.fill((0, 0, 0))

        self._draw_background()
        self._draw_map(game.height_map)
        self._draw_entities(game.creatures)
        self._draw_bullets(game.bullets)
        self._draw_hud(game.highscore, game.player)

        self.window.blit(self.screen, (0,0))
        pygame.display.update()

    def draw_cursor(self, x, y):
        self.screen.blit(self.assets['cursor'], (x, y))
    
    def draw_game_over(self, x, y):
        pygame.draw.rect(self.screen, (0, 0, 0), (self.screen_width / 2 - 115, self.screen_height / 2 - 100, 230, 44), 5)
        myfont = pygame.font.SysFont("calibri", 40, True)
        label = myfont.render("GAME OVER!", True, (0, 0, 0))
        self.window.blit(label, (self.screen_width / 2 - 110, self.screen_height / 2 - 95))
        self.window.blit(self.screen, (0, 0))
        pygame.display.update()
