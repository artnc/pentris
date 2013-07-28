import os
import time

import pygame as pg

window = pg.display.set_mode((250,450))
net = pg.image.load("pentris\\gscreen.png").subsurface((360,39,242,402))
squ = net.subsurface((0,0,22,22))
print(time.time())
for x in range(24000):
    window.blit(squ,(0,0))
print(time.time())
pg.display.flip()
input()