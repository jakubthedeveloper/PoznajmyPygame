#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import pygame
from levels import level1
pygame.init()

CAPTION = "Kuba PyGame 1"
SCREEN_SIZE = (1024, 768)
FULLSCREEN = False

class Game(object):
    # todo: add level changing
    level = level1.Level1(pygame)

    PLAYER_TILE_IDLE_A1_LEFT = 0
    PLAYER_TILE_IDLE_A2_LEFT = 1
    PLAYER_TILE_IDLE_A1_RIGHT = 2
    PLAYER_TILE_IDLE_A2_RIGHT = 3

    PLAYER_SEQUENCE_LENGTH_IDLE = 2

    PLAYER_TILES_CHANGE_SPEED = 0.005

    player_textures = {
        PLAYER_TILE_IDLE_A1_LEFT: pygame.image.load('./images/character/idleA1.png'),
        PLAYER_TILE_IDLE_A2_LEFT: pygame.image.load('./images/character/idleA2.png'),
        PLAYER_TILE_IDLE_A1_RIGHT: pygame.transform.flip(pygame.image.load('./images/character/idleA1.png'), True, False),
        PLAYER_TILE_IDLE_A2_RIGHT: pygame.transform.flip(pygame.image.load('./images/character/idleA2.png'), True, False)
    }

    player_position = level.initial_player_position
    player_facing = level.initial_player_facing

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.done = False

    def getPlayerTile(self, dt):
        # FOR IDLE
        sequence_frame = int((math.floor(pygame.time.get_ticks() * self.PLAYER_TILES_CHANGE_SPEED) % self.PLAYER_SEQUENCE_LENGTH_IDLE))

        if self.player_facing >= 0 and sequence_frame == 0:
            tile_index = self.PLAYER_TILE_IDLE_A1_RIGHT
        elif self.player_facing >= 0 and sequence_frame == 1:
            tile_index = self.PLAYER_TILE_IDLE_A2_RIGHT
        elif self.player_facing < 0 and sequence_frame == 0:
            tile_index = self.PLAYER_TILE_IDLE_A1_LEFT
        else:
            tile_index = self.PLAYER_TILE_IDLE_A2_LEFT

        return self.player_textures[tile_index]

    def drawBackground(self):
        self.screen.blit(self.level.background_image, (0,0))

    def drawObjects(self, dt):
        for row in range(self.level.MAPHEIGHT):
            for column in range(self.level.MAPWIDTH):
                textureIndex = self.level.tilemap[row][column]
                if textureIndex != None:
                    self.screen.blit(self.level.textures[textureIndex], (column * self.level.TILESIZE, row * self.level.TILESIZE))

    def drawPlayer(self, dt):
        self.screen.blit(self.getPlayerTile(dt), self.player_position)

    def update(self, dt):
        if pygame.key.get_pressed()[pygame.K_LEFT] != 0:
            self.player_facing = -1;

        if pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
            self.player_facing = 1;

        if pygame.mouse.get_pressed()[0]:
            print(pygame.mouse.get_pos())

    def draw(self, dt):
        self.drawBackground()
        self.drawObjects(dt)
        self.drawPlayer(dt)
        pygame.display.flip()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return

    def main_loop(self):
        dt = 0
        while not self.done:
            self.event_loop()
            self.update(dt)
            self.draw(dt)
            dt = self.clock.tick(self.fps) / 1000.0

def main():
    Game().main_loop()

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.display.set_caption(CAPTION)
    pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN if FULLSCREEN else 0)
    Game().main_loop()
    pygame.quit()