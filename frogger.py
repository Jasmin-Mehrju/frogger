import os
from typing import Any

import pygame


class Settings():
    WINDOW = pygame.rect.Rect((0, 0, 800, 800))
    FPS = 60
    DELTATIME = 1.0 / FPS
    DIRECTIONS = {"right": pygame.math.Vector2(5, 0), 
                  "left": pygame.math.Vector2(-5, 0), 
                  "up": pygame.math.Vector2(0, -5), 
                  "down": pygame.math.Vector2(0, 5)}
    TITLE = "Frogger"
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")
    start_pos = pygame.math.Vector2(WINDOW.width // 2, WINDOW.height - 40)

class Object(pygame.sprite.Sprite):
    def __init__(self, image_file, size, pos):
        super().__init__()
        self.pos = pos
        self.size = size
        self.image_file = image_file
        self.setImage()

    def setImage(self):
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, self.image_file)).convert()
        self.image = pygame.transform.scale(self.image, self.size)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self):
        self.setImage()


class Frog(Object):
    def __init__(self, image_file, size, pos):
        super().__init__(image_file, size, pos)
        self.pos = pygame.math.Vector2(pos)
        self.speed = 1
        self.direction = None

    def update(self):
        if self.direction:
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
    def __init__(self, image_file, size, pos, speedx, speedy, is_log = False):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, image_file)).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speedx = speedx
        self.speedy = speedy
        self.is_log = is_log

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
                
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

        self.ziel_image = pygame.image.load(os.path.join("images", "ziel.png")).convert()
        self.ziel_image = pygame.transform.scale(self.ziel_image, (100, 100))
        self.ziel_rect = self.ziel_image.get_rect()
        self.ziel_rect_left = self.ziel_image.get_rect(center=(50, 50))
        self.ziel_rect_center = self.ziel_image.get_rect(center=(Settings.WINDOW.width // 2, 50))
        self.ziel_rect_right = self.ziel_image.get_rect(center=(Settings.WINDOW.width - 50, 50))
    

        #autos
        self.obstacles = pygame.sprite.Group()
        self.car1 = Obstacle("car1.png", (100, 60), (Settings.WINDOW.width // 2, Settings.WINDOW.height - 200), speedx=2, speedy=0)
        self.obstacles.add(self.car1)

        self.car2 = Obstacle("car2.png", (100, 60), (Settings.WINDOW.width - 680, Settings.WINDOW.height - 200), speedx=2, speedy=0)
        self.obstacles.add(self.car2)

        self.car3 = Obstacle("car3.png", (100, 60), (Settings.WINDOW.width - 880, Settings.WINDOW.height - 200), speedx=2, speedy=0)
        self.obstacles.add(self.car3)

        self.car1L = Obstacle("car1L.png", (100, 60), (Settings.WINDOW.width // 2, Settings.WINDOW.height - 250), speedx=-2, speedy=0)
        self.obstacles.add(self.car1L)

        self.car2L = Obstacle("car2L.png", (100, 60), (Settings.WINDOW.width - 800, Settings.WINDOW.height - 250), speedx=-2, speedy=0)
        self.obstacles.add(self.car2L)

        self.car3L = Obstacle("car3L.png", (100, 60), (Settings.WINDOW.width - 600, Settings.WINDOW.height - 250), speedx=-2, speedy=0)
        self.obstacles.add(self.car3L)

        #trucks
        self.truck1 = Obstacle("truck1.png", (150, 60), (Settings.WINDOW.width - 900, Settings.WINDOW.height - 350), speedx= 4, speedy=0)
        self.obstacles.add(self.truck1)

        self.truck2 = Obstacle("truck2.png", (150, 60), (Settings.WINDOW.width - 450, Settings.WINDOW.height - 350), speedx= 4, speedy=0)
        self.obstacles.add(self.truck2)

        #Logs
        self.log1 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 300, Settings.WINDOW.height - 450), speedx= 2, speedy=0, is_log=True)
        self.obstacles.add(self.log1)

        self.log2 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 600, Settings.WINDOW.height - 450), speedx= 2, speedy=0, is_log=True)
        self.obstacles.add(self.log2)

        self.log25 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 900, Settings.WINDOW.height - 450), speedx= 2, speedy=0, is_log=True)
        self.obstacles.add(self.log25)

        # self.log3 = Obstacle("log2.png", (150, 60), (Settings.WINDOW.width - 600, Settings.WINDOW.height - 500), speedx= 3, speedy=0, is_log=True)
        # self.obstacles.add(self.log3)

        self.log4 = Obstacle("log2.png", (150, 60), (Settings.WINDOW.width - 350, Settings.WINDOW.height - 500), speedx= 3, speedy=0, is_log=True)
        self.obstacles.add(self.log4)

        self.log5 = Obstacle("log2.png", (150, 60), (Settings.WINDOW.width - 100, Settings.WINDOW.height - 500), speedx= 3, speedy=0, is_log=True)
        self.obstacles.add(self.log5)

        self.log8 = Obstacle("log2.png", (150, 60), (Settings.WINDOW.width - 600, Settings.WINDOW.height - 500), speedx= 3, speedy=0, is_log=True)
        self.obstacles.add(self.log8)

        self.log9 = Obstacle("log2.png", (150, 60), (Settings.WINDOW.width - 750, Settings.WINDOW.height - 500), speedx= 3, speedy=0, is_log=True)
        self.obstacles.add(self.log9)

        self.log10 = Obstacle("log2.png", (150, 60), (Settings.WINDOW.width - 900, Settings.WINDOW.height - 500), speedx= 3, speedy=0, is_log=True)
        self.obstacles.add(self.log10)

        self.log6 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 800, Settings.WINDOW.height - 550), speedx= -1, speedy=0, is_log=True)
        self.obstacles.add(self.log6)

        self.log7 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 420, Settings.WINDOW.height - 550), speedx= -1, speedy=0, is_log=True)
        self.obstacles.add(self.log7)

        self.log72 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 100, Settings.WINDOW.height - 550), speedx= -1, speedy=0, is_log=True)
        self.obstacles.add(self.log72)

        self.log11 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 900, Settings.WINDOW.height - 600), speedx= 3, speedy=0, is_log=True)
        self.obstacles.add(self.log11)

        self.log12 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 600, Settings.WINDOW.height - 600), speedx= 3, speedy=0, is_log=True)
        self.obstacles.add(self.log12)

        self.log122 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 900, Settings.WINDOW.height - 600), speedx= 3, speedy=0, is_log=True)
        self.obstacles.add(self.log122)

        self.log13 = Obstacle("log2.png", (150, 60), (Settings.WINDOW.width - 900, Settings.WINDOW.height - 650), speedx= 2, speedy=0, is_log=True)
        self.obstacles.add(self.log13)

        self.log14 = Obstacle("log2.png", (150, 60), (Settings.WINDOW.width - 700, Settings.WINDOW.height - 650), speedx= 2, speedy=0, is_log=True)
        self.obstacles.add(self.log14)

        self.log15 = Obstacle("log2.png", (150, 60), (Settings.WINDOW.width - 500, Settings.WINDOW.height - 650), speedx= 2, speedy=0, is_log=True)
        self.obstacles.add(self.log15)

        self.log152 = Obstacle("log2.png", (150, 60), (Settings.WINDOW.width - 300, Settings.WINDOW.height - 650), speedx= 2, speedy=0, is_log=True)
        self.obstacles.add(self.log152)

        self.log142 = Obstacle("log2.png", (150, 60), (Settings.WINDOW.width - 100, Settings.WINDOW.height - 650), speedx= 2, speedy=0, is_log=True)
        self.obstacles.add(self.log142)

        self.log16 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 900, Settings.WINDOW.height - 700), speedx= -1, speedy=0, is_log=True)
        self.obstacles.add(self.log16)

        self.log17 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 600, Settings.WINDOW.height - 700), speedx= -1, speedy=0, is_log=True)
        self.obstacles.add(self.log17)

        self.log172 = Obstacle("log1.png", (250, 60), (Settings.WINDOW.width - 300, Settings.WINDOW.height - 700), speedx= -1, speedy=0, is_log=True)
        self.obstacles.add(self.log172)


        self.background_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "bg.png")).convert()
        self.background_image = pygame.transform.scale(self.background_image, Settings.WINDOW.size)

   
        self.running = True

    def restart_round(self):
        self.frog.pos = pygame.math.Vector2(Settings.start_pos)
        self.frog.rect.topleft = self.frog.pos

        for obstacle in self.obstacles:
            if isinstance(obstacle, Obstacle):
                obstacle.speedx *= 1.1
                if obstacle.speedy != 0:
                    obstacle.speedy *= 1.1

    def run(self):
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.FPS)
        pygame.quit()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        pygame.draw.rect(self.screen, (25, 147, 41),(0, Settings.WINDOW.height - 90, Settings.WINDOW.width, 90))
        pygame.draw.rect(self.screen, (25, 147, 41),(0, Settings.WINDOW.height - 800, Settings.WINDOW.width, 100))
        pygame.draw.rect(self.screen, (25, 147, 41),(0, Settings.WINDOW.height - 390, Settings.WINDOW.width, 40))
        pygame.draw.rect(self.screen, (255, 255, 255),(0, Settings.WINDOW.height - 180, Settings.WINDOW.width, 10))
        pygame.draw.rect(self.screen, (255, 255, 255),(0, Settings.WINDOW.height - 220, Settings.WINDOW.width, 10))
        pygame.draw.rect(self.screen, (255, 255, 255),(0, Settings.WINDOW.height - 320, Settings.WINDOW.width, 10))

     

        self.obstacles.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.ziel_image, self.ziel_rect_left)
        self.screen.blit(self.ziel_image, self.ziel_rect_center)
        self.screen.blit(self.ziel_image, self.ziel_rect_right)
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
                    self.frog.pos.x -= 50
                elif event.key == pygame.K_RIGHT:
                    self.frog.image_file = "frog_right.png"
                    self.frog.direction = "right"
                    self.frog.pos.x += 50
                elif event.key == pygame.K_UP:
                    self.frog.image_file = "frog_up.png"
                    self.frog.direction = "up"
                    self.frog.pos.y -= 50
                elif event.key == pygame.K_DOWN:
                    self.frog.image_file = "frog_down.png"
                    self.frog.direction = "down"
                    self.frog.pos.y += 50
                self.frog.setImage()

            elif event.type == pygame.KEYUP:
                self.frog.direction = None


    def update(self):
        self.all_sprites.update()
        self.obstacles.update()

        collisions = pygame.sprite.groupcollide(self.all_sprites, self.obstacles, False, False)
        for sprite, obstacles in collisions.items():
                for obstacle in obstacles:
                    if not obstacle.is_log:
                        sprite.pos = pygame.math.Vector2(Settings.start_pos)
                        sprite.rect.topleft = sprite.pos

        log_collisions = pygame.sprite.spritecollide(self.frog, self.obstacles, False)
        on_log = False
        for log in log_collisions:
            if log.is_log:
                self.frog.pos.x += log.speedx * 0.5
                self.frog.rect.topleft = self.frog.pos
                on_log = True

        if not on_log and self.frog.rect.top < Settings.WINDOW.height - 450:
            self.frog.pos = pygame.math.Vector2(Settings.start_pos)
            self.frog.rect.topleft = self.frog.pos


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
