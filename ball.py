import sys, math, random, time, pygame
pygame.init()

size = width, height = 640, 480
speed = [1, 1]

screen = pygame.display.set_mode(size)
color = 0, 0, 0

ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
                a = math.floor((event.key - 97) * 10)
                color = a, (a + 85) % 255, (a - 85) % 255

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
        
    screen.fill(color)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    time.sleep(.005)