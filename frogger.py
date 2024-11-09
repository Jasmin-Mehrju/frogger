import os
from typing import Any

import pygame


class Settings():
    WINDOW = pygame.rect.Rect((0, 0, 800, 800))
    FPS = 60
    DELTATIME = 1.0 / FPS
    DIRECTIONS = {"right": pygame.math.Vector2(10, 0), 
                  "left": pygame.math.Vector2(-10, 0), 
                  "up": pygame.math.Vector2(0, -10), 
                  "down": pygame.math.Vector2(0, 10)}
    TITLE = "Frogger"
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")

class Object(pygame.sprite.Sprite):
    def __init__(self, image_file, size, pos):
        super().__init__()
        self.pos = pos
        self.size = size
        self.image_file = image_file
        self.setImage()

    def setImage(self):
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, self.image_file)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def update(self):
        self.setImage()


class Frog(Object):
    def __init__(self, image_file, size, pos):
        super().__init__(image_file, size, pos)
        self.speed = 1
        self.direction = None

    def update(self):
        if self.direction:
            movement = Settings.DIRECTIONS.get(self.direction)
            if movement:
                self.pos += movement
                self.rect.topleft = self.pos
        self.setImage()


class Game():
    def __init__(self):
        os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 50"
        pygame.init()

        self.screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("Frogger")
        self.clock = pygame.time.Clock()

        self.frog = Frog("frog_up.png", (40, 40), (Settings.WINDOW.width // 2, Settings.WINDOW.height - 40))
        self.all_sprites = pygame.sprite.Group(self.frog)

        self.background_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "bg.png")).convert()
        self.background_image = pygame.transform.scale(self.background_image, Settings.WINDOW.size)

   
        self.running = True

    def run(self):
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.FPS)
        pygame.quit()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:          
                if event.key == pygame.K_ESCAPE:  
                    self.running = False

                elif event.key == pygame.K_LEFT:
                    self.frog.image_file = "frog_left.png"
                    self.frog.direction = "left"
                    self.frog.setImage()
                elif event.key == pygame.K_RIGHT:
                    self.frog.image_file = "frog_right.png"
                    self.frog.direction = "right"
                    self.frog.setImage()
                elif event.key == pygame.K_UP:
                    self.frog.image_file = "frog_up.png"
                    self.frog.direction = "up"
                    self.frog.setImage()
                elif event.key == pygame.K_DOWN:
                    self.frog.image_file = "frog_down.png"
                    self.frog.direction = "down"
                    self.frog.setImage()

            elif event.type == pygame.KEYUP:
                self.frog.direction = None


    def update(self):
        self.all_sprites.update()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
