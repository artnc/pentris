#!/usr/bin/env python

"""
Pentris v1.0
Art Chaidarun
Released under MIT license

Python 2.7

"""

from __future__ import division

import copy
import json
import math
import os
import random
import sys
import threading
import time

import pygame as pg

def num_blit(surf, num, rect):
  """Print a number using its digits' sprites"""
  surf.fill(black, rect)
  r = 1 + int(math.log(num, 10)) if num else 1
  for x in range(r):
    d = int(((num - (num % (10 ** x))) / (10 ** x)) % 10)
    surf.blit(n[d], (rect[0] + rect[2] - 18 * (x + 1), rect[1]))

def setcolor(file):
  """Define image sprites per piece"""
  global color
  sheet = pg.image.load(file)
  color = [0] * 19
  for x in range(19):
    tmp = pg.surface.Surface((22, 22))
    tmp.blit(sheet, (0, 0), (22 * x, 0, 22, 22))
    color[x] = tmp

def shiftpiece(x, y, hard=0):
  """Move the active piece left, right, or down"""
  global axis, square, piece, curr, landed, timeup
  backup = copy.deepcopy(square)
  # Remove piece from square
  for j in range(5):
    for i in range(5):
      if piece[i][j]:
        square[i + axis[0] - 1][j + axis[1] - 1] = 0
  axis[0] += x
  axis[1] += y
  overlap = 0
  for j in range(5):
    for i in range(5):
      if piece[i][j] and square[i + axis[0] - 1][j + axis[1] - 1]:
        overlap = 1
        break
    if overlap:
      break
  # Move piece if ok, else undo changes to square
  if not overlap:
    for j in range(5):
      for i in range(5):
        if piece[i][j]:
          square[i + axis[0] - 1][j + axis[1] - 1] = curr
  else:
    # If timeout() causes overlap, means piece has landed
    if timeup:
      landed = 1
    square = copy.deepcopy(backup)
    axis[0] -= x
    axis[1] -= y

def rotpiece():
  """Rotate the active piece clockwise"""
  global axis, square, piece, curr
  overlap = 0
  # Check overlaps
  for j in range(5):
    for i in range(5):
      if piece[i][j]:
        continue
      tmp = square[i + axis[0] - 1][j + axis[1] - 1]
      if tmp and piece[4 - j][i]:
        overlap += 1
  if not overlap:
    # Remove piece from square
    for j in range(5):
      for i in range(5):
        if piece[i][j]:
          square[i + axis[0] - 1][j + axis[1] - 1] = 0
    backup = copy.deepcopy(piece)
    # Rotate, then draw to square
    for j in range(5):
      for i in range(5):
        tmp = backup[i][j]
        piece[j][4 - i] = tmp
        if tmp:
          square[j + axis[0] - 1][4 - i + axis[1] - 1] = curr

def rotpiece_original():
  """Rotate the active piece clockwise"""
  a = time.time()
  global axis, square, piece
  backup = copy.deepcopy(piece)
  # Remove piece from square
  for j in range(5):
    for i in range(5):
      if piece[i][j]:
        square[i + axis[0] - 1][j + axis[1] - 1] = 0
  overlap = 0
  # Copy rotated backup to piece, check overlaps
  for j in range(5):
    for i in range(5):
      piece[i][j] = backup[4 - j][i]
      if piece[i][j] and square[i + axis[0] - 1][j + axis[1] - 1]:
        overlap = 1
        break
    if overlap:
      break
  if overlap:
    for j in range(5):
      for i in range(5):
        tmp = backup[i][j]
        if tmp:
          square[i + axis[0] - 1][j + axis[1] - 1] = tmp
  else:
    for j in range(5):
      for i in range(5):
        tmp = backup[4 - j][i]
        piece[i][j] = tmp
        if tmp:
          square[i + axis[0] - 1][j + axis[1] - 1] = tmp
  print(time.time() - a)

def timeout():
  """Keep the active piece falling"""
  global timeup
  timeup = 1
  pg.event.post(pg.event.Event(pg.KEYDOWN, {'key': pg.K_DOWN}))
  pg.event.post(pg.event.Event(pg.KEYUP, {'key': pg.K_UP}))

pg.init()

# Nonzeros form pentomino shapes, rotated 90deg clockwise
pent = [0] * 19

pent[1] = [[0, 0, 1, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 1, 0, 0]]

pent[2] = [[0, 0, 0, 0, 0],
           [0, 2, 2, 0, 0],
           [0, 2, 2, 0, 0],
           [0, 0, 2, 0, 0],
           [0, 0, 0, 0, 0]]

pent[3] = [[0, 0, 0, 0, 0],
           [0, 0, 3, 0, 0],
           [0, 3, 3, 0, 0],
           [0, 3, 3, 0, 0],
           [0, 0, 0, 0, 0]]

pent[4] = [[0, 0, 0, 0, 0],
           [0, 4, 4, 0, 0],
           [0, 0, 4, 0, 0],
           [0, 0, 4, 0, 0],
           [0, 0, 4, 0, 0]]

pent[5] = [[0, 0, 5, 0, 0],
           [0, 0, 5, 0, 0],
           [0, 0, 5, 0, 0],
           [0, 5, 5, 0, 0],
           [0, 0, 0, 0, 0]]

pent[6] = [[0, 0, 6, 0, 0],
           [0, 0, 6, 0, 0],
           [0, 6, 6, 0, 0],
           [0, 6, 0, 0, 0],
           [0, 0, 0, 0, 0]]

pent[7] = [[0, 0, 0, 0, 0],
           [0, 7, 0, 0, 0],
           [0, 7, 7, 0, 0],
           [0, 0, 7, 0, 0],
           [0, 0, 7, 0, 0]]

pent[8] = [[0, 0, 0, 0, 0],
           [0, 8, 8, 0, 0],
           [0, 0, 8, 0, 0],
           [0, 8, 8, 0, 0],
           [0, 0, 0, 0, 0]]

pent[9] = [[0, 0, 9, 0, 0],
           [0, 0, 9, 0, 0],
           [0, 9, 9, 0, 0],
           [0, 0, 9, 0, 0],
           [0, 0, 0, 0, 0]]

pent[10]= [[0, 0, 0, 0, 0],
           [0, 0,10, 0, 0],
           [0,10,10, 0, 0],
           [0, 0,10, 0, 0],
           [0, 0,10, 0, 0]]

pent[11]= [[0, 0, 0, 0, 0],
           [0, 0, 0,11, 0],
           [0,11,11,11, 0],
           [0, 0, 0,11, 0],
           [0, 0, 0,0, 0]]

pent[12]= [[0, 0, 0, 0, 0],
           [0,12,12,12, 0],
           [0, 0, 0,12, 0],
           [0, 0, 0,12, 0],
           [0, 0, 0, 0, 0]]

pent[13]= [[0, 0, 0, 0, 0],
           [0, 0,13,13, 0],
           [0,13,13, 0, 0],
           [0, 0,13, 0, 0],
           [0, 0, 0, 0, 0]]

pent[14]= [[0, 0, 0, 0, 0],
           [0, 0,14, 0, 0],
           [0,14,14, 0, 0],
           [0, 0,14,14, 0],
           [0, 0, 0, 0, 0]]

pent[15]= [[0, 0, 0, 0, 0],
           [0, 0, 0,15, 0],
           [0, 0,15,15, 0],
           [0,15,15, 0, 0],
           [0, 0, 0, 0, 0]]

pent[16]= [[0, 0, 0, 0, 0],
           [0, 0,16, 0, 0],
           [0,16,16,16, 0],
           [0, 0,16, 0, 0],
           [0, 0, 0, 0, 0]]

pent[17]= [[0, 0, 0, 0, 0],
           [0,17,17, 0, 0],
           [0, 0,17, 0, 0],
           [0, 0,17,17, 0],
           [0, 0, 0, 0, 0]]

pent[18]= [[0, 0, 0, 0, 0],
           [0, 0,18,18, 0],
           [0, 0,18, 0, 0],
           [0,18,18, 0, 0],
           [0, 0, 0, 0, 0]]

# Nextbox piece offset
offset = [(  0,  0),
          (  0,  0),
          (  0,-10),
          (  0,-10),
          (-10,-10),
          ( 10,-10),
          ( 10,-10),
          (-10,-10),
          (  0,-10),
          ( 10,-10),
          (-10,-10),
          (  0,  0),
          (  0,  0),
          (  0,  0),
          (  0,  0),
          (  0,  0),
          (  0,  0),
          (  0,  0),
          (  0,  0),]

setcolor("img/colors.png")

black = 0, 0, 0

# Title screen
title = pg.image.load("img/welcome.png")
logo = title.subsurface((27, 0, 586, 228))
lpieces = title.subsurface((90, 249, 114, 106))
rpieces = title.subsurface((436, 249, 114, 106))

# Game screen
game = pg.image.load("img/gscreen.png")
grid = game.subsurface((322, 0, 318, 480))
net = grid.subsurface((38, 39, 242, 402))

# Numerical digits
num = pg.image.load("img/nums.png")
n = [0] * 10
for x in range(10):
  n[x] = num.subsurface((x*18, 0, 18, 33))

# Create game window
os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.display.set_icon(pg.image.load("img/icon2.png"))
pg.display.set_caption("Pentris v1.0")
window = pg.display.set_mode((640, 480))
window.fill(black)

# Fade in title screen
for a in range(5, 260, 5):
  title.set_alpha(a)
  window.blit(title, (0, 0))
  pg.display.flip()

# Wait for user input
lv = 1
score = 0
lines = 0

narea = 322, 292, 36, 33
while 1:
  event = pg.event.wait()
  if event.type == pg.QUIT:
    sys.exit()
  if event.type == pg.KEYDOWN:
    key = pg.key.name(event.key)
    if key == "return":
      break
    elif key == "left":
      if lv == 1: lv = 21
      lv -= 1
    elif key == "right":
      if lv == 20: lv = 0
      lv += 1
    num_blit(title, lv, narea)
    window.blit(title, (0, 0))
    pg.display.update(narea)

# Fade out title screen
level = title.subsurface((261, 292, 118, 33))
grass = title.subsurface((0, 392, 640, 88))
for x in range(1, 55):
  window.fill(black)

  window.blit(lpieces, (90 + x * 11, 249))
  window.blit(rpieces, (436 - x * 11, 249))

  w = int(586 - x * 257 / 54)
  h = int(228 - x * 100 / 54)
  window.blit(pg.transform.smoothscale(logo, (w, h)), (27 - int(x / 2), 0))

  a = int(255 * (1 - x / 54))
  level.set_alpha(a)
  window.blit(level, (261, 292))
  grass.set_alpha(a)
  window.blit(grass, (0, 392 + 2 * x))

  pg.display.flip()

# Fade in game screen

num_blit(game, lv, (229, 157, 36, 33))
num_blit(game, score, (139, 205, 126, 33))
num_blit(game, lines, (211, 253, 54, 33))
for a in range(0, 260, 5):
  game.set_alpha(a)
  window.blit(game, (0, 0))
  pg.display.update([(0, 128, 322, 352), (322, 0, 318, 480)])

# Set up game
square = [0] * 15
for x in range(15):
  square[x] = [0] * 23
  square[x][0] = 1
for x in range(23):
  square[0][x] = 1
  square[13][x] = 1
  square[14][x] = 1

# Per game
next = random.randint(1, 18)

# Per piece
while 1:
  kode = 0
  curr = next
  piece = copy.deepcopy(pent[curr])
  # Choose and display next piece
  next = random.randint(1, 18)
  window.fill(black, (74, 351, 170, 90))
  for c in range(5):
    for r in range(5):
      if pent[next][c][r]:
        x = 108 + 20 * c + offset[next][0]
        y = 425 - 20 * r + offset[next][1]
        window.blit(color[next], (x, y))
  pg.display.update((74, 350, 170, 90))
  # Show current piece at top of grid
  axis = [5, 19 if curr < 11 else 18]
  for j in range(5):
    for i in range(5):
      if piece[i][j]:
        square[i + axis[0] - 1][j + axis[1] - 1] = piece[i][j]
  # Per fall interval
  while 1:
    t = threading.Timer(.8 - .03 * lv, timeout)
    t.start()
    landed = 0
    # Receive (possibly simulated) keyboard input
    freetime = 1
    while freetime:
      timeup = 0
      while 1:
        event = pg.event.wait()
        if event.type == pg.QUIT:
          t.cancel()
          sys.exit()
        if event.type == pg.KEYDOWN:
          break
      key = pg.key.name(event.key)
      if key == "left":
        kode += 1 if kode == 4 or kode == 6 else -kode
        shiftpiece(-1, 0)
      elif key == "right":
        kode += 1 if kode == 5 or kode == 7 else -kode
        shiftpiece(1, 0)
      elif key == "up":
        kode += 1 if kode < 3 else -kode
        rotpiece()
      elif key == "down":
        shiftpiece(0, -1)
        if timeup < 1:
          kode += 1 if kode == 2 or kode == 3 else -kode
      elif key == "space":
        shiftpiece(0, -1, 1)
      elif key == "b":
        kode = 9 if kode == 8 else 0
      elif key == "a":
        if kode == 9:
          setcolor("img/colorsinv.png")
        else:
          kode = 0
      # Redraw playing field
      window.blit(net, (360, 39))
      for c in range(1, 13):
        for r in range(1, 21):
          if square[c][r]:
            window.blit(color[square[c][r]], (360 + 20*c - 20, 39 + 400 - 20*r))
      pg.display.update((360, 39, 242, 402))
      # If "down" was simulated
      if timeup:
        t.cancel()
        break
    if landed:
      break
  # Process completed lines
  streak = [0] * 5
  completed = []
  for j in range(1 if axis[1] < 2 else axis[1] - 1, axis[1] + 4):
    complete = 1
    for i in range(1, 13):
      if square[i][j] == 0:
        complete = 0
        break
    if complete:
      completed.append(j)
  for j in reversed(completed):
    for i in range(1, 13):
      square[i].pop(j)
      square[i].append(0)
  lines += len(completed)
  score += 4 + 10 * len(completed)
  lv = 1 + score // 100
  num_blit(game, lv, (229, 157, 36, 33))
  num_blit(game, score, (139, 205, 126, 33))
  num_blit(game, lines, (211, 253, 54, 33))
  window.blit(game, (0, 0))
  pg.display.update((0, 128, 322, 352))

# Wait for user input
print("done")
while 1:
  event = pg.event.wait()
  if event.type == pg.KEYDOWN:
    break
