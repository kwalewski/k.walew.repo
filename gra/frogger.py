import pygame
from pygame.locals import *
from sys import exit

#---------------------------------------------------------------------------
#Inicjalizujemy program
#---------------------------------------------------------------------------
pygame.init()
pygame.font.init()
pygame.mixer.pre_init()

#wyświetlany tekst grupujemy wg wielkości liter(inaczej-gdzie będzie się znajdował)
font = pygame.font.get_default_font()
fontBig = pygame.font.SysFont(font, 70)
fontSmall = pygame.font.SysFont(font, 24)
fontMiddle = pygame.font.SysFont(font, 35)

screen = pygame.display.set_mode((448,546))
pygame.display.set_caption('Frogger')

#---------------------------------------------------------------------------
#Ładujemy obrazy i dżwięki
#---------------------------------------------------------------------------

background = pygame.image.load('images/bg.png').convert()
frogUp = pygame.image.load('images/frog_up.png').convert_alpha()
frogDown = pygame.image.load('images/frog_down.png').convert_alpha()
frogLeft = pygame.image.load('images/frog_left.png').convert_alpha()
frogRight = pygame.image.load('images/frog_right.png').convert_alpha()
car1 = pygame.image.load('images/car1.png').convert_alpha()
car2 = pygame.image.load('images/car2.png').convert_alpha()
car3 = pygame.image.load('images/car3.png').convert_alpha()
car4 = pygame.image.load('images/car4.png').convert_alpha()
car5 = pygame.image.load('images/car5.png').convert_alpha()
wood = pygame.image.load('images/kłoda.png').convert_alpha()


soundHit = pygame.mixer.Sound('sounds/hit.wav')
soundWater = pygame.mixer.Sound('sounds/water.wav')
soundSucces = pygame.mixer.Sound('sounds/success.wav')
soundtrack = pygame.mixer.Sound('sounds/soundtrack.wav')


#---------------------------------------------------------------------------
#Klasy obiektów
#---------------------------------------------------------------------------

#---------------------
#Klasa Object
#---------------------

#Główna klasa dla wszystkich obiektów
class Object():
    #inicjalizujemy wybrany obiekt w wybranym miejscu
    def __init__(self,position,sprite):
        self.sprite = sprite
        self.position = position

    #rysujemy go
    def draw(self):
        screen.blit(self.sprite,(self.position))

    #przechowujemy położenie sprite'a
    def rect(self):
        return Rect(self.position[0],self.position[1],self.sprite.get_width(),self.sprite.get_height())

#------------------
#Klasa Game
#------------------

#W tej klasie przechowujemy parametry gry, czyli
#prędkość, level, punkty i czas
class Game():
    def __init__(self):
        self.speed = 3
        self.level = 1
        self.points = 0
        self.time = 30
        
#----------------------
#Klasa Frog
#----------------------

class Frog(Object):
    def __init__(self,position,frogUp):
        #obrazek żaby
        self.sprite = frogUp
        #jej pozycja
        self.position = position
        #ustawiamy 3 "życia"
        self.lifes = 3
        #strona w którą jest zwrócona żaba
        self.way = "UP"
        #dycedujemy czy możemy daną żabą się przemieścić
        self.can_move = 1

    def updateFrogImage(self,key_pressed):
        #w zależności od wciśniętego przycisku decydujemy, w którą stronę
        #jest zwrócona żaba, aktualizujemy obrazek
        if self.way != key_pressed:
            self.way = key_pressed
            if self.way == "up":
                self.sprite = frogUp
            elif self.way == "down":
                self.sprite = frogDown
            elif self.way == "left":
                self.sprite = frogLeft
            elif self.way == "right":
                self.sprite = frogRight

    #prezesuwamy żabę
    def moveFrog(self,key_pressed):
        #aktualizujemy jej zwrot
        self.updateFrogImage(key_pressed)
        
        if key_pressed == "up":
            if self.position[1] > 39:
                self.position[1] = self.position[1]-39
        elif key_pressed == "down":
            if self.position[1] < 473:
                self.position[1] = self.position[1]+39
        if key_pressed == "left":
            if self.position[0] > 30:
                self.position[0] = self.position[0]-39
        elif key_pressed == "right":
            if self.position[0] < 401:
                self.position[0] = self.position[0]+39
                    
    
    #ustawiamy żabę w pozycji wyjściowej
    def FrogBackPosition(self):
        self.position = [207, 475]

    def frogDead(self,game):
        #gdy żaba umrze, ustawiamy ją na pozycję początkową
        self.FrogBackPosition()
        #zabieramy życie
        self.lifes = self.lifes - 1
        #resetujemy czas(mamy 30s na dojście)
        game.time = 30
        #resetujemy inne parametry żaby
        self.way = "UP"
        self.can_move = 1

    def draw(self):
        screen.blit(self.sprite,(self.position))

    def rect(self):
        return Rect(self.position[0],self.position[1],30,30)


#-------------------
#Klasa Car i Wood
#-------------------

class Car(Object):
    def __init__(self,position,car,way):
        #obrazek samochodu
        self.sprite = car
        self.position = position
        #strona w którą auto lub kłoda będą się poruszać
        self.way = way
       
    #w zależności od wybranej strony definiujemy, jak 
    #mają się poruszać auta
    def move(self,speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed 
        elif self.way == "left":
            self.position[0] = self.position[0] - speed 


class Wood(Object):
    def __init__(self,position,wood,way):
        self.sprite = wood
        self.position = position
        self.way = way

    def move(self,speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed
        elif self.way == "left":
            self.position[0] = self.position[0] - speed


#---------------------------------------------------------------------------
#Inne funkcje
#---------------------------------------------------------------------------

#kłody i auta będziemy przechowywać w listach, więc defiujemy fukcje pomocnicze,
#które wyświetlą nam wszystkie te obiekty w liście i je przesuną
def displayAll(list):
    for i in list:
        i.draw()

def moveAll(list,speed):
    for i in list:
        i.move(speed)

#----------------------------------------------------------------------------

#jeśli obiekty wyjdą poza plansze to je usuwamy z listy
def destroyCars(list):
    for i in list:
        if i.position[0] < -80:
            list.remove(i)
        elif i.position[0] > 516:
            list.remove(i)

def destroyWoods(list):
    for i in list:
        if i.position[0] < -100:
            list.remove(i)
        elif i.position[0] > 448:
            list.remove(i)

#----------------------------------------------------------------------------
#Definiujemy funkcje, która będzie tworzyć obiekty w odstępach czasowych
#Mamy np. liste[100,20,40,100,100].Każda wartość odpowiada kolejnym autom.
#Odejmujemy od każdej wartości po kolei jedynkę. Gdy dojdziemy z którąś do 
#zera to możemy stworzyć nowy sdamochód(drugi jest odpowiednio daleko).
#Resetujemy ponownie wartość do 100, aby móc stworzyć następny obiekt po tym
#samym czasie

def createCars(list,cars,game):
    for i in range(5):
        list[i] = list[i] - 1
        if list[i] <= 0:
            if i == 0:
                list[0] = 100
                car = Car([-55,436],car1,"right")
                cars.append(car)
            elif i == 1:
                list[1] = 100
                car = Car([506, 397],car2,"left")
                cars.append(car)
            elif i == 2:
                list[2] = 100
                car = Car([-80, 357],car3,"right")
                cars.append(car)
            elif i == 3:
                list[3] = 100
                car = Car([516, 318],car4,"left")
                cars.append(car)
            elif i == 4:
                list[4] = 100
                car = Car([-56, 280],car5,"right")
                cars.append(car)

def createWood(list,woods,game):
    for i in range(5):
        list[i] = list[i] - 1
        if list[i] <= 0:
            if i == 0:
                list[0] = 100
                log = Wood([-100,200],wood,"right")
                woods.append(log)
            elif i == 1:
                list[1] = 100
                log = Wood([448, 161],wood,"left")
                woods.append(log)
            elif i == 2:
                list[2] = 100
                log = Wood([-100, 122],wood,"right")
                woods.append(log)
            elif i == 3:
                list[3] = 100
                log = Wood([448, 83],wood,"left")
                woods.append(log)
            elif i == 4:
                list[4] = 100
                log = Wood([-100, 44],wood,"right")
                woods.append(log)
                
#-------------------------------------------------------------------------

def frogAndStreet(frog,cars,game):
    #jeśli wykryjemy kolizje z którymś z aut, to uśmiercamy żabę
    for i in cars:
        carRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(carRect):
            #dodajemy dźwięk uderzenia
            soundHit.play()
            frog.frogDead(game)

def frogAndLake(frog,woods,game):
    #Sprawdzamy, czy żaba jest w kolizji z jakąś kłodą
    colission = 0
    
    for i in woods:
        woodRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(woodRect):
            colission = 1
            woodWay = i.way

    #jeśli nie, to uśmiercamy żabę
    if colission == 0:
        soundWater.play()
        frog.frogDead(game)

    #jeśli tak, to porusza się z tą samą szybkością co kłoda, czyli płynie na niej
    elif colission == 1:
        #sprawdzamy jeszcze czy w lewo, czy w prawo
        if woodWay == "right":
            frog.position[0] = frog.position[0] + game.speed

        elif woodWay == "left":
            frog.position[0] = frog.position[0] - game.speed

#-----------------------------------------------------------------------
#Jeśli żaba dotrze do listka, to resetujemy jej położenie, a w miejsce listka
#wklejamy obraz żaby
def stayAtLeaf(frog,frogOnLeaves,game,position):
    #tworzymy obraz żaby na wybranyn listku
    frogOnLeaf = Object(position,frogDown)
    #dodajemy naszą żabę do listy
    frogOnLeaves.append(frogOnLeaf)
    #dadajemy dźwięk
    soundSucces.play()
    #resetujemy żabę, dodajemy punkty, resetujemy czas
    frog.FrogBackPosition()
    game.points += 15 + game.time
    game.time = 30
    frog.can_move = 1

#sprawdzamy czy żaba dotarła do listka
def setStayAtLeaf(frog,frogOnLeaves,game):
    if frog.position[0] > 33 and frog.position[0] < 53:
        stayAtLeaf(frog,frogOnLeaves,game,[43,7])

    elif frog.position[0] > 115 and frog.position[0] < 135:
        stayAtLeaf(frog,frogOnLeaves,game,[125,7])

    elif frog.position[0] > 197 and frog.position[0] < 217:
        stayAtLeaf(frog,frogOnLeaves,game,[207,7])

    elif frog.position[0] > 279 and frog.position[0] < 299:
        stayAtLeaf(frog,frogOnLeaves,game,[289,7])

    elif frog.position[0] > 361 and frog.position[0] < 381:
        stayAtLeaf(frog,frogOnLeaves,game,[371,7])

    #jeśli nie to wraca na kłode
    else:
        frog.position[1] = 46
        frog.can_move = 1

#--------------------------------------------------------------------------
#W zależności od tego, gdzie jest żaba, odpalamy odpowiednią funkcję

def frogAndWhat(frog,cars,woods,frogOnLeaves,game):
    if frog.position[1] > 240 :
        frogAndStreet(frog,cars,game)

    elif frog.position[1] < 240 and frog.position[1] > 40:
        frogAndLake(frog,woods,game)

    elif frog.position[1] < 40 :
        setStayAtLeaf(frog,frogOnLeaves,game)

#--------------------------------------------------------------------------

def nextLevel(frogOnLeaves,cars,woods,frog,game):
    #jeśli wszystkie listki są zapełnione, to zwiększamy
    #level i prędkość, dodajemy punkty, resetujemy liste,
    #umieszczamy żabę na początku
    if len(frogOnLeaves) == 5:
        frogOnLeaves[:] = []
        frog.FrogBackPosition()
        game.level += 1
        game.speed += 1
        game.points += 100
        game.time = 30

#---------------------------------------------------------------------------
#Menu
#---------------------------------------------------------------------------

def Menu():

    while True:
    
        screen.blit(background, (0, 0))

        #definiujemy kontener dla każdego z przycisku
        buttonStart = pygame.Rect(180,100,80,50)
        buttonRules = pygame.Rect(180,160,80,50)
        buttonHS = pygame.Rect(140,220,160,50)
        buttonAuthor = pygame.Rect(170,280,100,50)
        buttonEnd = pygame.Rect(195,340,50,50)


        #W kontenerach umieszczamy napisy
        text_start = fontMiddle.render(('Start'),1,(127,0,255))
        screen.blit(text_start,(190,115))

        text_rules = fontMiddle.render(('Rules'),1,(127,0,255))
        screen.blit(text_rules,(185,175))

        text_hs = fontMiddle.render(('High scores'),1,(127,0,255))
        screen.blit(text_hs,(150,235))

        text_author = fontMiddle.render(('Author'),1,(127,0,255))
        screen.blit(text_author,(180,290))

        text_end = fontMiddle.render(('End'),1,(127,0,255))
        screen.blit(text_end,(195,355))

        #Bierzemy wsp. kursora
        mx, my = pygame.mouse.get_pos()
        
        #jeśli klikniemy w odpowiedni kontener to zostajemy 
        #przekierowani do tego miejsca uruchamiając funkcje
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if buttonStart.collidepoint((mx,my)):
                        gra()
                if buttonRules.collidepoint((mx,my)):
                        rules()
                if buttonHS.collidepoint((mx,my)):
                        HS()
                if buttonAuthor.collidepoint((mx,my)):
                        author()
                if buttonEnd.collidepoint((mx,my)):
                        exit()

        
        pygame.display.update()

#-------------------------------------------------------------------

def rules():
    while True:
        
        screen.blit(background, (0, 0))

        text_titleRules = fontMiddle.render(('Rules:'),1,(0,0,0))
        screen.blit(text_titleRules,(185,50))

        text_rules1 = fontSmall.render(('Move your frog using arrows. Go safely to another side'),1,(0,0,0))
        screen.blit(text_rules1,(10,100))

        text_rules2 = fontSmall.render(('of road and river. Avoid cars and swimming. Use the'),1,(0,0,0))
        screen.blit(text_rules2,(10,120))

        text_rules3 = fontSmall.render(('logs to get through the river. Collect points for every'),1,(0,0,0))
        screen.blit(text_rules3,(10,140))

        text_rules4 = fontSmall.render(('arrival and try to do it the fastest you can(time matters!)'),1,(0,0,0))
        screen.blit(text_rules4,(10,160))

        #przycisk powrotu do menu
        buttonBack = pygame.Rect(175,475,80,30)
        text_Back = fontMiddle.render(('Back'),1,(127,0,255))
        screen.blit(text_Back,(185,480))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if buttonBack.collidepoint((mx,my)):
                        Menu()

        pygame.display.update()

#-------------------------------------------------------------------

def HS():
    while True:
        
        screen.blit(background, (0, 0))

        #otwieramy plik w którym zapisane są high scores
        file = open("HS.txt", 'r')
        Lines = file.readlines()
        
        #tworzymy litę z tymi wartościami
        scores = []
        for line in Lines:
            scores.append(line[0:-1])

        #wyświetlamy te wyniki
        text_titleHS = fontMiddle.render(('High scores:'),1,(0,0,0))
        screen.blit(text_titleHS,(150,50))

        text_HS1 = fontMiddle.render(('- %s')%(scores[0]),1,(0,0,0))
        screen.blit(text_HS1,(180,80))

        text_HS2 = fontMiddle.render(('- %s')%(scores[1]),1,(0,0,0))
        screen.blit(text_HS2,(180,110))

        text_HS3 = fontMiddle.render(('- %s')%(scores[2]),1,(0,0,0))
        screen.blit(text_HS3,(180,140))

        text_HS4 = fontMiddle.render(('- %s')%(scores[3]),1,(0,0,0))
        screen.blit(text_HS4,(180,170))

        text_HS5 = fontMiddle.render(('- %s')%(scores[4]),1,(0,0,0))
        screen.blit(text_HS5,(180,200))

        buttonBack = pygame.Rect(175,475,80,30)
        text_Back = fontMiddle.render(('Back'),1,(127,0,255))
        screen.blit(text_Back,(185,480))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if buttonBack.collidepoint((mx,my)):
                        Menu()

        pygame.display.update()

#----------------------------------------------------------------------

def author():
    while True:
        
        screen.blit(background, (0, 0))

        text_titleAuthor = fontMiddle.render(('Author:'),1,(0,0,0))
        screen.blit(text_titleAuthor,(180,50))

        text_Author = fontSmall.render(('Krystian Walewski-student of applied mathematics'),1,(0,0,0))
        screen.blit(text_Author,(20,150))

        buttonBack = pygame.Rect(175,475,80,30)
        text_Back = fontMiddle.render(('Back'),1,(127,0,255))
        screen.blit(text_Back,(185,480))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if buttonBack.collidepoint((mx,my)):
                        Menu()

        pygame.display.update()


#-------------------------------------------------------------------

def setHS(game):
    
    #pobieramy liste najwyzszych wyników z pliku
    file1 = open("HS.txt", 'r')
    Lines = file1.readlines()
    file1.close()
        
    scores = []
    for line in Lines:
        scores.append(int(line[0:-1]))

    #dodajemy do niej nasz wynik z gry, sortujemy i 
    #zapisujemy 5 najwyższych
    scores.append(game.points)
    scores.sort()
    scores.reverse()
    
        
    file2 = open("HS.txt", 'w')
    for i in range(5):
        file2.write("%s\n"%(scores[i]))
    file2.close()


def gra():
    checkHS = 1
    while True:
        
        game = Game()
    
        #klawisz nie jest wciśnięty
        key_up = 1
        
        #tworzymy żabę
        frog = Frog([207,475],frogUp)

        #listy z obiektami
        cars = []
        woods = []
        frogOnLeaves = []
        
        #w jakich odstępach zainicjalizujemy obiekty
        carsInit = [30, 10, 20, 0, 60]
        woodsInit = [10, 0, 30, 20, 50]
        
        key_pressed = 0

        while frog.lifes > 0:

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYUP:
                    key_up = 1
                if event.type == KEYDOWN:
                    #żabą możemy się poruszyć tylko jeśli przycisk
                    #zostanie ponownie wciśnięty(trzymanie cały czas nic nie da)
                    if key_up == 1 and frog.can_move == 1 :
                        #sprawdzamy jaki przycisk został wciśnięty
                        key_pressed = pygame.key.name(event.key)
                        #ruszamy żabę
                        frog.moveFrog(key_pressed)
                        #blokujemy dalszy ruch
                        frog.can_move = 0
        
            #ustawiamy szybkość gry(klatki)
            time_passed = clock.tick(30)

            #ustawiamy licznik czasu
            frames = 30

            #W sekunde wyswietlamy 30 klatek, czyli wywołujemy program 30 ruszamy
            #Po każdych 30 klatkach odejmujemy sekunde z licznika
            if frames <= 0:
                frames = 30
                game.time -= 1
            else:
                frames -= 1

            #uśmiercamy żabę, gdy skończy się czas
            if game.time == 0:
                frog.frogDead(game)

            #odblokowujemy żabę
            frog.can_move = 1
           
            #tworzymy auta i kłody 
            createCars(carsInit,cars,game)
            createWood(woodsInit,woods,game)

            #przesuwamy auta i kłody
            moveAll(cars,game.speed)
            moveAll(woods,game.speed)
            
            #sprawdzamy gdzie jest żaba i co się z nią dzieje
            frogAndWhat(frog,cars,woods,frogOnLeaves,game)
            
            #sprawdzamy czy nie przejść na następny level
            nextLevel(frogOnLeaves,cars,woods,frog,game)

            #ustawiamy na ekranie licznik żyć, punktów, czasu i levelu
            text_Level = fontSmall.render(('Level: %s'%(game.level)),1,(255,255,255))
            text_Points = fontSmall.render(('Points: %s'%(game.points)),1,(255,255,255))
            text_Time = fontSmall.render(('Time: %s'%(game.time)),1,(255,255,255))
            text_Lifes = fontSmall.render(('Lifes: %s'%(frog.lifes)),1,(255,255,255))
            screen.blit(background, (0, 0))
            screen.blit(text_Level,(10,520))
            screen.blit(text_Points,(110,520))
            screen.blit(text_Time,(210,520))
            screen.blit(text_Lifes,(310,520))


            #wyświetlamy na ekran wszystkie obiekty
            displayAll(cars)
            displayAll(woods)
            displayAll(frogOnLeaves)
            frog.draw()

            #usuwamy niepotrzebne obiekty
            destroyCars(cars)
            destroyWoods(woods)

            pygame.display.update()

        #Ekran przegranej
        while frog.lifes == 0:
            
            #odpalamy funkcje do sprawdzenia high scores
            if checkHS == 1:
                setHS(game)
                checkHS = 0
           
            screen.blit(background, (0, 0))
            
            #wyświetlamy informacje i wynik
            text_GameOver = fontBig.render(('GAME OVER'),1,(255,0,0))
            screen.blit(text_GameOver, (70,100))

            text_YourScore = fontMiddle.render(('Your score: %s')%(game.points),1,(255,0,0))
            screen.blit(text_YourScore, (150,200))

            #wstawiamy przyciski try again i end
            buttonGame = pygame.Rect(100,475,120,30)
            text_Try = fontMiddle.render(('Try Again'),1,(127,0,255))
            screen.blit(text_Try,(100,480))

            buttonEnd = pygame.Rect(270,475,55,30)
            text_End = fontMiddle.render(('End'),1,(127,0,255))
            screen.blit(text_End,(270,480))

            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if buttonGame.collidepoint((mx,my)):
                            gra()
                    if buttonEnd.collidepoint((mx,my)):
                            exit()
            
            pygame.display.update()


#---------------------------------------------------------------------------
#Rozpoczynamy program
#---------------------------------------------------------------------------

#uruchamiamy zegar
clock = pygame.time.Clock()
#włączamy muzykę
soundtrack.play()

Menu()
