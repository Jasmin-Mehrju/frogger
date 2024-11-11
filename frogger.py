import os
from typing import Any

import pygame


class Settings():
    WINDOW = pygame.rect.Rect((0, 0, 800, 800))
    FPS = 60
    DELTATIME = 1.0 / FPS
    DIRECTIONS = {"right": pygame.math.Vector2(8, 0), 
                  "left": pygame.math.Vector2(-8, 0), 
                  "up": pygame.math.Vector2(0, -8), 
                  "down": pygame.math.Vector2(0, 8)}
    TITLE = "Frogger"
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")
    start_pos = (WINDOW.width // 2, WINDOW.height - 40)

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
            if self.pos.x < 0:
                self.pos.x = 0
            elif self.pos.x + self.rect.width > Settings.WINDOW.width:
                self.pos.x = Settings.WINDOW.width - self.rect.width
            if self.pos.y < 0:
                self.pos.y = 0
            elif self.pos.y + self.rect.height > Settings.WINDOW.height:
                self.pos.y = Settings.WINDOW.height - self.rect.height

            self.rect.topleft = self.pos
        self.setImage()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image_file, size, pos, speedx, speedy):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, image_file)).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect = self.rect.move(self.speedx, self.speedy)
        if self.rect.right < 0:
            self.rect.left = Settings.WINDOW.width
        elif self.rect.left > Settings.WINDOW.width:
            self.rect.right = 0



class Game():
    def __init__(self):
        os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 50"
        pygame.init()

        self.screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("Frogger")
        self.clock = pygame.time.Clock()

        self.frog = Frog("frog_up.png", (40, 40), (Settings.start_pos))
        self.all_sprites = pygame.sprite.Group(self.frog)

        self.obstacles = pygame.sprite.Group()
        self.car1 = Obstacle("car1.png", (100, 60), (Settings.WINDOW.width // 2, Settings.WINDOW.height - 150), speedx=2, speedy=0)
        self.obstacles.add(self.car1)

        self.car2 = Obstacle("car2.png", (100, 60), (Settings.WINDOW.width - 680, Settings.WINDOW.height - 150), speedx=2, speedy=0)
        self.obstacles.add(self.car2)

        self.car3 = Obstacle("car3.png", (100, 60), (Settings.WINDOW.width - 880, Settings.WINDOW.height - 150), speedx=2, speedy=0)
        self.obstacles.add(self.car3)

        self.car1L = Obstacle("car1L.png", (100, 60), (Settings.WINDOW.width // 2, Settings.WINDOW.height - 200), speedx=-3, speedy=0)
        self.obstacles.add(self.car1L)

        self.car2L = Obstacle("car2L.png", (100, 60), (Settings.WINDOW.width - 800, Settings.WINDOW.height - 200), speedx=-3, speedy=0)
        self.obstacles.add(self.car2L)

        self.car3L = Obstacle("car3L.png", (100, 60), (Settings.WINDOW.width - 600, Settings.WINDOW.height - 200), speedx=-3, speedy=0)
        self.obstacles.add(self.car3L)
        

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
        self.obstacles.draw(self.screen)
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
        self.obstacles.update()

        collisions = pygame.sprite.groupcollide(self.all_sprites, self.obstacles, False, False)
        for sprite, obstacles in collisions.items():
            if isinstance(sprite, Frog):
                sprite.pos = Settings.start_pos
                sprite.rect.topleft = sprite.pos

        self.all_sprites.update()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
