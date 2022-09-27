import pygame as pg
pg.init()

W=1280
H=768
FPS=10
screen=pg.display.set_mode((W,H))
pg.display.set_caption("Gold collector")
clock=pg.time.Clock()

SKY=(200,205,255)
SPEED=W//64
rotate=1
gravity=2
g=10
Jump=False
jumpCount=0
isGameRunning=True
gamemode=0
#UI
Terrain1=pg.transform.scale(pg.image.load("Terrain1.png"), (W//20,H//12))
Terrain2=pg.transform.scale(pg.image.load("Terrain2.png"), (W//20,H//12))
PlayImg=pg.transform.scale(pg.image.load("Button1.png"), (W//5,H//6))
QuitImg=pg.transform.scale(pg.image.load("Button2.png"), (W//5,H//6))
LevelImg=pg.transform.scale(pg.image.load("Button3.png"), (W//5,H//6))
button1=pg.Rect(W//5, H//2, W//6,H//6)
button2=pg.Rect(W//1.6, H//2, W//6,H//6)
button3=pg.Rect(W//2.5, H//3, W//6,H//6)
font1=pg.font.SysFont("comic sans ms", H//6)
font2=pg.font.SysFont("courier new", H//12)
you_won_text=font1.render("You won", 1, (238,221,130))

level_text=font2.render("level1", 1, (255,255,255))
level_number=1
level1=[]
level2=[]
level3=[]
levels=[level1,level2,level3]
level=levels[0]
for x in open("level1.txt","r"):level1.append(x)
for x in open("level2.txt","r"):level2.append(x)
for x in open("level3.txt","r"):level3.append(x)

#объекты
Objects={"Tree":{"Scale":(W//7,H//4), "Anim":[4], "AnimCount":1},\
		"Coin":{"Scale":(W//40,H//24), "Anim":[4], "AnimCount":1},\
 		"Chest":{"Scale":(W//10,H//11), "Anim":[9], "AnimCount":5},\
 		"Cloud":{"Scale":(W//9,H//16), "Anim":[1], "AnimCount":1},\
 		"Crab":{"Scale":(W//12,H//14), "Anim":[6], "AnimCount":1}}

#создание игры
def new_game():
	global Chest, coins, pick, colliders
	Chest=[]
	colliders=[]
	coins=[]
	pick=0
	PlayerRect.x=W//60
	PlayerRect.y=H-H//5
	y=0
	for row in level:
		x=0
		y+=H//12
		for num in row:
			if   str(num)=="1":colliders.append(pg.Rect(x,y, W//20,1))
			elif str(num)=="3":Chest.append(pg.Rect(x+W//20,y+H//20, W//64,H//38))
			elif str(num)=="6":coins.append(pg.Rect(x,y, W//20,W//20))
			x+=W//20

#загрузка изображений
def imageLoad(spisok):
	for i in spisok.keys():
		for j in range(1, spisok[i]["Anim"][0]+1):
			link=i+str(j)+".png"
			img=pg.transform.scale(pg.image.load(link), spisok[i]["Scale"])
			spisok[i]["Anim"].append(img)

#поворот персонажа
def flip(Person):
	global rotate, SPEED
	rotate=rotate*(-1); SPEED=SPEED*(-1)
	for i in range(1,len(Person)):
		Person[i]=pg.transform.flip(Person[i],1,0)

#отрисовка
def draw():
	global game
	screen.fill(SKY)
	y=0
	for row in level:
		x=0
		y+=H//12
		for num in row:
			if   str(num)=="1":screen.blit(Terrain1, (x,y))
			elif str(num)=="2":screen.blit(Terrain2, (x,y))
			elif str(num)=="3":screen.blit(Objects["Chest"]["Anim"][Objects["Chest"]["AnimCount"]], (x,y-2))
			elif str(num)=="4": screen.blit(Objects["Tree"]["Anim"][Objects["Tree"]["AnimCount"]], (x-(Objects["Tree"]["Scale"][0]//2),y))
			elif str(num)=="5": screen.blit(Objects["Cloud"]["Anim"][Objects["Cloud"]["AnimCount"]], (x,y))
			x+=W//20
		for coin in coins:
			screen.blit(Objects["Coin"]["Anim"][Objects["Coin"]["AnimCount"]], (coin.left, coin.top))
	screen.blit(Objects["Crab"]["Anim"][Objects["Crab"]["AnimCount"]], (PlayerRect.left, PlayerRect.top))
	if gamemode==0:
		screen.blit(PlayImg, (button1.left, button1.top))
		screen.blit(QuitImg, (button2.left, button2.top))
		screen.blit(LevelImg, (button3.left, button3.top))
		screen.blit(level_text, (button3.x+7, button3.y+10))
	if pick>=4 and PlayerRect.colliderect(Chest[0]) and gamemode!=0:screen.blit(you_won_text, (W//3, H//4)); game=False
	pg.display.update()

imageLoad(Objects)
Player=Objects["Crab"]["Anim"]
PlayerRect=Objects["Crab"]["Anim"][1].get_rect()
for i in range(1,len(Player)): Player[i]=pg.transform.flip(Player[i],True,False)
new_game()
while isGameRunning:
	pressed=pg.Rect(pg.mouse.get_pos(), (10,10))
	clock.tick(FPS)
	draw()

	#МЕНЮ
	if gamemode==0:
		for i in pg.event.get():
			if i.type==pg.QUIT:
				isGameRunning=False
			if i.type==pg.MOUSEBUTTONDOWN:
				if i.button==1:
					if pressed.colliderect(button1):
						gamemode=1
						game=True
						new_game()
					if pressed.colliderect(button2):
						isGameRunning=False
					if pressed.colliderect(button3):
						level_number+=1
						if level_number==4:level_number=1
						level_text=font2.render("level"+str(level_number), 1, (255,255,255))
						level=levels[level_number-1]
						new_game()
	if gamemode==1:
		if game:
			#АНИМАЦИЯ
		    for i in Objects.keys():
		    	if i=="Chest":
		    		if Objects[i]["AnimCount"]<9 and pick<4:
		    			Objects[i]["AnimCount"]+=1
		    		elif pick==4:pick+=1; Objects[i]["AnimCount"]=1
		    		elif Objects[i]["AnimCount"]<6 and pick>4:
		    				Objects[i]["AnimCount"]+=1
		    	else:
			    	if Objects[i]["AnimCount"]<Objects[i]["Anim"][0]:Objects[i]["AnimCount"]+=1
			    	else: Objects[i]["AnimCount"]=1
		    #ПЕРЕДВИЖЕНИЕ
		    PlayerRect.x+=SPEED
		    if PlayerRect.x<-PlayerRect.width//2 :flip(Player)
		    if PlayerRect.x>W-PlayerRect.width//2 :flip(Player)
		    for coin in coins:
		    	if PlayerRect.colliderect(coin):
		    		pick+=1
		    		coins.remove(coin)
		    #ПРЫЖОК И ГРАВИТАЦИЯ
		    if Jump and jumpCount<5:
		    	jumpCount+=1
		    	PlayerRect.y-=H//25
		    	if jumpCount>=5: Jump=False; g=10
		    else:
		    	g+=gravity
		    	PlayerRect.y+=g
		    for col in colliders:
		    	screen.fill((100,100,100), col)
		    	if ((PlayerRect.colliderect(col) and PlayerRect.y<col.y-col.height)) and (Jump==False):
		    		PlayerRect.y-=g
		    		g=0

		    #обработка нажатий клавиш
		    for i in pg.event.get():
		        if i.type==pg.QUIT:
		            isGameRunning=False
		        if i.type==pg.KEYDOWN:
		        	if i.key==pg.K_LEFT:
		        		if rotate==1:flip(Player)
		        	if i.key==pg.K_RIGHT:
		        		if rotate==-1: flip(Player)
		        	if i.key==pg.K_SPACE and Jump==False and g==0:
		        		Jump=True
		        		jumpCount=0

		#обработка нажатий мыши
		for i in pg.event.get():
			if i.type==pg.QUIT:
				isGameRunning=False
			if i.type==pg.MOUSEBUTTONDOWN:
				gamemode=0

pg.quit()