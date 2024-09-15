import pygame
import random

# cores
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 100)
dark_green = (0, 200, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)

# dimensoes e congif iniciais
width, height = 1800, 1200
cell_size = 40
grid_width = width // cell_size
grid_height = height // cell_size

# Direções
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(grid_width // 2, grid_height // 2)]
        self.direction = RIGHT

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        if 0 <= new_head[0] < grid_width and 0 <= new_head[1] < grid_height:
            self.body.insert(0, new_head)
            self.body.pop()
            return True
        return False

    def grow(self):
        tail = self.body[-1]
        new_tail = (tail[0] - self.direction[0], tail[1] - self.direction[1])
        self.body.append(new_tail)

    def shrink(self):
        half_size = len(self.body) // 2
        self.body = self.body[:half_size + 1 if len(self.body) % 2 != 0 else half_size]

    def draw(self, surface):
        for index, segment in enumerate(self.body):
            color = dark_green if index == 0 else green
            pygame.draw.rect(surface, color, (segment[0] * cell_size, segment[1] * cell_size, cell_size, cell_size))

class Game:
    def __init__(self):
        pygame.init()  # Inicializa modulos
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('jogo snake AleB')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = self.generate_food()
        self.poison = self.generate_poison()
        self.font = pygame.font.SysFont(None, 60)  # Cria uma fonte do sistema, None usa a fonte padrão

    def generate_food(self):
        while True:
            food_pos = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
            if food_pos not in self.snake.body:
                return food_pos

    def generate_poison(self):
        while True:
            poison_pos = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
            if poison_pos not in self.snake.body:
                return poison_pos

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.direction = UP
                    elif event.key == pygame.K_DOWN:
                        self.snake.direction = DOWN
                    elif event.key == pygame.K_LEFT:
                        self.snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT:
                        self.snake.direction = RIGHT

            if not self.snake.move():
                running = False

            if self.snake.body[0] == self.food:
                self.snake.grow()
                self.food = self.generate_food()
                self.poison = self.generate_poison()

            if self.snake.body[0] == self.poison:
                if len(self.snake.body) == 1:
                    running = False
                else:
                    self.snake.shrink()
                self.poison = self.generate_poison()

            self.screen.fill(black)
            self.snake.draw(self.screen)
            pygame.draw.rect(self.screen, yellow, (self.food[0] * cell_size, self.food[1] * cell_size, cell_size, cell_size))
            pygame.draw.rect(self.screen, red, (self.poison[0] * cell_size, self.poison[1] * cell_size, cell_size, cell_size))
            self.draw_score()  # desenha placar
            pygame.display.update()
            self.clock.tick(15)

        pygame.quit()

    def draw_score(self):
        score_text = self.font.render(f'Size: {len(self.snake.body)}', True, white)
        self.screen.blit(score_text, (10, 10))

if __name__ == "__main__":
    game = Game()
    game.run()
