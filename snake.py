import math
import random
import pygame
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('bubble.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1.0)

difficulty = int(input("난이도를 입력해주세요.(Easy : 1, Normal : 2, Hard : 3) : "))

if (difficulty == 1):
    fail_row_col = 20
if (difficulty == 2):
    fail_row_col = 16
if (difficulty == 3):
    fail_row_col = 12

width = (6 - difficulty) * 100 #500=1 400=2 300=3
height = (6 - difficulty) * 100 #500=1 400=2 300=3

cols = (6 - difficulty) * 4 #20=1 16=2 12=3
rows = (6 - difficulty) * 4 #20=1 16=2 12=3


class cube():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
            

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        


class snake():
	body = []
	turns = {}
    
	def __init__(self, color, pos):
		#pos is given as coordinates on the grid ex (1,5)
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 1
    
	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			keys = pygame.key.get_pressed()

			for key in keys:
				if keys[pygame.K_LEFT]:
					self.dirnx = -1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
				elif keys[pygame.K_RIGHT]:
					self.dirnx = 1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
				elif keys[pygame.K_UP]:
					self.dirny = -1
					self.dirnx = 0
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
				elif keys[pygame.K_DOWN]:
					self.dirny = 1
					self.dirnx = 0
					self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        
		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)
			else:
				c.move(c.dirnx,c.dirny)
        
        
	def reset(self,pos):
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1

	def addCube(self):
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny

		if dx == 1 and dy == 0:
			self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
		elif dx == -1 and dy == 0:
			self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
		elif dx == 0 and dy == 1:
			self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
		elif dx == 0 and dy == -1:
			self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy
    

	def draw(self, surface):
		for i,c in enumerate(self.body):
			if i == 0:
				c.draw(surface, True)
			else:
				c.draw(surface)



def redrawWindow():
    global win
    win.fill((0,0,0))
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()
    pass



def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y +sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x, 0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0, y),(w,y))
    


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
               continue
        else:
               break

    return (x,y)



def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
	global s, snack, win
	win = pygame.display.set_mode((width,height))
	s = snake((255,0,0),(10,10))
	if difficulty == 1:
		snack = cube(randomSnack(rows,s), color=(0,255,0))
	elif difficulty == 2:
		snack = cube(randomSnack(rows,s), color=(255,0,255))
	elif difficulty == 3:
		snack = cube(randomSnack(rows,s), color=(255,128,0))
	flag = True
	clock = pygame.time.Clock()
    
	while flag:
		pygame.time.delay(50)
		clock.tick(difficulty*5)
		s.move()
		headPos = s.head.pos
		if headPos[0] >= fail_row_col or headPos[0] < 0 or headPos[1] >= fail_row_col or headPos[1] < 0:
			print("Score:", len(s.body))
			message_box('You Lost!', 'Play again')
			s.reset((10, 10))

		if s.body[0].pos == snack.pos:
			s.addCube()
			if difficulty == 1:
				snack = cube(randomSnack(rows,s), color=(0,255,0))
			elif difficulty == 2:
				snack = cube(randomSnack(rows,s), color=(255,0,255))
			elif difficulty == 3:
				snack = cube(randomSnack(rows,s), color=(255,128,0))
            
		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
				print("Score:", len(s.body))
				message_box('You Lost!', 'Play again')
				s.reset((10,10))
				break
                    
		redrawWindow()

main()
    

    
