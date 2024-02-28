import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("My Pygame Window")

clock = pygame.time.Clock()

light_mask = 'light_med.png'

runing = pygame.image.load("runing.png")
runing = pygame.transform.scale(runing, (65, 80))
runing = pygame.transform.flip(runing, True, False)
runing_rect = runing.get_rect()

start = pygame.image.load("start.png")
start = pygame.transform.scale(start, (210, 210))

fire_ball = pygame.image.load("fire_ball.png")
fire_ball = pygame.transform.scale(fire_ball, (100, 100))
fire_ball = pygame.transform.flip(fire_ball, False, True)

coin = pygame.image.load("coin.png")
coin = pygame.transform.scale(coin, (90, 90))

maze = pygame.image.load("maze1.png")
maze = pygame.transform.scale(maze, (860, 860)).convert_alpha()

transparency = 0
#maze.fill((255, 255, 255, transparency), special_flags=pygame.BLEND_RGBA_MULT)
fog = pygame.Surface((860, 860))
fog.fill(transparency)
light_mask = pygame.image.load(light_mask).convert_alpha()
light_mask = pygame.transform.scale(light_mask, (500, 500))
light_rect = light_mask.get_rect()

image = pygame.image.load("back.png")
image = pygame.transform.scale(image, (1920, 1150))


def render_fog(x_char, y_char):
    fog.fill(transparency)
    x_char = x_char - 750
    y_char = y_char - 300
    fog.blit(light_mask, (x_char, y_char))
    screen.blit(fog, (530, 110), special_flags=pygame.BLEND_MULT)


pygame.display.set_caption('Show Text')
font = pygame.font.Font('freesansbold.ttf', 40)

#font = pygame.font.Font('freesansbold.ttf', 40)
message = 'Game Over!!!'
done = False
running = True
x_char = 1220
y_char = 885
speed = 48
lettersSpeed = 10
letterCounter = 0
win = False
start_ticks = pygame.time.get_ticks() #starter tick
seconds = 0
limit = 120
hp = 1
discoverd = False
fire_x = 700


def better_text(msg, size, color, bg, pos):
    font = pygame.font.Font('freesansbold.ttf', size)
    snip = font.render(msg, True, color, bg)
    textRect = snip.get_rect()
    textRect.center = pos
    screen.blit(snip, textRect)

with open('coincount.txt', 'r') as f:
    coinCount = f.read()
    #coinCount = int(coinCount)
    print(coinCount)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            print(x_char, y_char)
            if screen.get_at((x_char + 100, y_char)) != (0, 0, 0, 255) and x_char < 1300:
                x_char += speed
        if keys[pygame.K_a]:
            print(x_char, y_char)
            #print(screen.get_at((x_char - 25, y_char)))
            if screen.get_at((x_char - 25, y_char)) != (0, 0, 0, 255) and x_char > 530:
                x_char -= speed
        if keys[pygame.K_w]:
            print(x_char, y_char)
            if screen.get_at((x_char, y_char - 20)) != (0, 0, 0, 255) and y_char > 117:
                y_char -= speed
        if keys[pygame.K_s]:
            print(x_char, y_char)
            if screen.get_at((x_char, y_char + 100)) != (0, 0, 0, 255) and y_char < 885:
                y_char += speed

    if x_char == 836 and y_char == 501:
        win = True

    seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
    if seconds > limit:  # if more than 10 seconds close the game
        print("reached time limit! ")
    #print(seconds)  # print how many seconds

    if limit - seconds < 0:
        exit()

    if x_char == 644 and y_char == 117 and discoverd == False:
        coinCount = int(coinCount)
        coinCount += 1
        discoverd = True

    if win == False:
        screen.blit(image, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (520, 100, 880, 880))
        screen.blit(maze, (530, 110))
        if discoverd == False:
            screen.blit(coin, (630, 117))
        if fire_x < 915 and fire_x > 680:
            screen.blit(fire_ball, (fire_x, 693))
            fire_x += 1
            print(fire_x)
        else:
            if fire_x < 915:
                fire_x += 1
                print(fire_x)
            else:
                fire_x = 600
        if fire_x + 17 == x_char and y_char == 693:
            print("got hit!")
            hp -= 1
        screen.blit(runing, (x_char, y_char))
        render_fog(x_char, y_char)
        screen.blit(start, (1240, 815))
        screen.blit(start, (745, 435))
        better_text(f'your hp is: {hp}', 40, 'white', 'black', (200, 170))
        better_text(f'BTC: {coinCount}', 40, 'white', 'black', (200, 220))
        better_text(f'{limit - int(seconds)} seconds left!', 40, 'white', 'black', (200, 120))
    else:
        if letterCounter < lettersSpeed * len(message):
            letterCounter += 1
        elif letterCounter >= lettersSpeed * len(message):
            done = True
        screen.fill('black')
        snip = font.render(message[0:letterCounter // lettersSpeed], True, 'green', 'blue')
        screen.blit(snip, (10, 310))
        #better_text('your reward is: Nahum\'s mom!', 40, 'white', 'blue', (1000, 540))
        with open('coincount.txt', 'w') as f:
            f.write(str(coinCount))

    pygame.display.flip()
    clock.tick(600)
pygame.quit()
