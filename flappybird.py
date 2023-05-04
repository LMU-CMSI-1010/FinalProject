import pygame
import random

# Define game constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
GRAVITY = 0.3
BIRD_SPEED = -7
PIPE_SPEED = -5
PIPE_GAP = 200
BASE_HEIGHT = 100

# Bird class, bird image and scale
class Bird:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.velocity = 0
        self.image = pygame.image.load('Assets/bird.png')
        self.image = pygame.transform.scale(self.image, (42, 42))

#update call for game loop (bird falling)
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
#jump func
    def jump(self):
        self.velocity = BIRD_SPEED
#draws bird
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
#pipe class
class Pipe:
    #initializes pipe (sets starting position and attributes)
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.gap_y = random.randint(BASE_HEIGHT + PIPE_GAP, SCREEN_HEIGHT - PIPE_GAP)
        self.top_pipe_height = self.gap_y - PIPE_GAP/2
        self.bottom_pipe_height = SCREEN_HEIGHT - self.gap_y - PIPE_GAP/2
        self.image_top = pygame.image.load('Assets/pipe_top.png')
        self.image_bottom = pygame.image.load('Assets/pipe_bottom.png')
        
#pipe moving
    def update(self):
        self.x += PIPE_SPEED

#draws pipe
    def draw(self, screen):
        screen.blit(self.image_top, (self.x, self.top_pipe_height - 1000))
        screen.blit(self.image_bottom, (self.x, self.gap_y + 120))

#handles collision for bird and pipe
    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, bird.image.get_width(), bird.image.get_height())
        top_pipe_rect = pygame.Rect(self.x, self.top_pipe_height - 1000, self.image_top.get_width(), self.image_top.get_height() - 50)
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + 120, self.image_bottom.get_width(), self.image_bottom.get_height() - 50)

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            return True

        return False
       

#score class
class Score:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.font = pygame.font.SysFont('comicsans', 30)

#increment score by pipe 
    def update(self, pipes):
        for pipe in pipes:
            if pipe.x == 50:
                self.score += 1

        if self.score > self.high_score:
            self.high_score = self.score

#display text for score
    def draw(self, screen):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))

#background helper class
class Background(pygame.sprite.Sprite):
        def __init__(self, image_file, location):
            pygame.sprite.Sprite.__init__(self)  
            self.image = pygame.image.load(image_file)
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = location

#game class (core game loop and event handling)
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.bird = Bird()
        self.pipes = [Pipe()]
        self.score = Score()
        self.game_over = False
        self.background = pygame.image.load('Assets/download.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        

 #game over screen   
    def draw_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Game Over', True, (255, 255, 255))
        restart_button = font.render('R - Restart', True, (255, 255, 255))
        quit_button = font.render('Q - Quit', True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/3))
        self.screen.blit(restart_button, (SCREEN_WIDTH/2 - restart_button.get_width()/2, SCREEN_HEIGHT/1.9 + restart_button.get_height()))
        self.screen.blit(quit_button, (SCREEN_WIDTH/2 - quit_button.get_width()/2, SCREEN_HEIGHT/2 + quit_button.get_height()/2))
        pygame.display.update()
        
#core game loop
    def run(self):
        i = 0
        while True:
            if not self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:#event.type == pygame.K_q:
                        self.game_over = True
                    elif event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                        self.bird.jump()
                        
                # Update objects
                self.bird.update()
                for pipe in self.pipes:
                    pipe.update()

                # Remove off-screen pipes
                if self.pipes and self.pipes[0].x < -200:
                    self.pipes.pop(0)

                # Check for collision
                if self.check_collision():
                    self.game_over = True

                # Add new pipe
                if self.pipes[-1].x < SCREEN_WIDTH - 200:
                    self.pipes.append(Pipe())

                # Update score
                self.score.update(self.pipes)
                self.screen.fill((0,0,0))
                
                #background movement
                self.screen.blit(self.background, (i,0))
                self.screen.blit(self.background,(SCREEN_WIDTH + i, 0))
                if (i == -SCREEN_WIDTH):
                        self.screen.blit(self.background,(SCREEN_WIDTH + i, 0))
                        i = 0
                i -= 1

            

                # Draw objects
                for pipe in self.pipes:
                    pipe.draw(self.screen)
                self.bird.draw(self.screen)
                self.score.draw(self.screen)
                pygame.display.update()

                

                # Set game FPS
                self.clock.tick(60)
            else:
                self.draw_game_over_screen()
                keys = pygame.key.get_pressed()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.bird.y = SCREEN_HEIGHT/2
                        self.pipes = [Pipe()]
                        self.score.score = 0
                        self.game_over = False
                        self.background = pygame.image.load('Assets/download.png')
                        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                        


        # Quit the game
        pygame.quit()


    def check_collision(self):
        for pipe in self.pipes:
            if pipe.collide(self.bird):
                return True

        if self.bird.y >= SCREEN_HEIGHT - BASE_HEIGHT:
            return True

        return False

# Create and run the game
game = Game()
game.run()

