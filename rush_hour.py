import pygame
import sys


class Game:
    def __init__(self,game_row,game_col):
        self.row = game_row
        self.col = game_col
        self.display = [['.']*game_row for i in range(game_col)]
        self.cars={}
        self.lot=[]

    def load_game(self):
        data = open(sys.argv[1],'r')
        line = data.readline()
        while len(line)>1:
            self.lot.append(line[:-1].split(', '))
            line = data.readline()
        license=0
        for car in self.lot:
            new_car = Car(car[0],int(car[1]),int(car[2]),int(car[3]))
            self.cars[str(license)]=new_car
            if new_car.orientation=='h':
                for i in range(new_car.size):
                    self.display[new_car.row][new_car.col+i]=str(license)
            else:
                for i in range(new_car.size):
                    self.display[new_car.row+i][new_car.col]=str(license)
            license+=1
        self.update()

    def update(self):                   
        for i in self.display:
            for j in i:
                if j.isdigit() and int(j)>=10:
                    print(j , end = ' ')
                else:
                    print(j, end ='  ')
            print()


    def play(self):
        while not self.game_end():
            command_car = str(input('enter which car to  move'))
            command_direction = str(input('enter the direction to move'))
            command_step = int(input('enter how far'))
           
            if self.check(self.cars[command_car],command_direction,command_step):
                self.move(self.cars[command_car],command_direction,command_step,command_car)
            self.update() 

    def game_end(self):
        if self.display[2][5]=='0':
            return True
        return False


    def move(self,car,direction,step,license):
        for i in range(step):
            if car.orientation=='v' and direction=='w':
                self.display[car.row-1][car.col]=str(license)
                self.display[car.row+car.size-1][car.col]='.'
                car.row-=1
            elif car.orientation=='v' and direction=='s':
                self.display[car.row+car.size][car.col]=str(license)
                self.display[car.row][car.col]='.'
                car.row+=1
            elif car.orientation=='h' and direction=='a':
                self.display[car.row][car.col-1]=str(license)
                self.display[car.row][car.col+car.size-1]='.'
                car.col-=1
            elif car.orientation=='h' and direction =='d':
                self.display[car.row][car.col+car.size]=str(license)
                self.display[car.row][car.col]='.'
                car.col+=1

    def check(self,car,direction,step):
        if car.orientation == 'v':
            for i in range(1,step+1):
                if direction == 'w':
                    if car.row-step<0:
                        print('out of bounds')
                        return False
                    if self.display[car.row-i][car.col]!='.':
                        print('collision 1')
                        return False
                elif direction =='s':
                    if car.row+car.size+step>self.row:
                        print('out of bounds')
                        return False
                    if self.display[car.row+car.size-1+i][car.col]!='.':
                        print('collision 2')
                        return False
            return True
        elif car.orientation == 'h':
            for i in range(1,step+1):
                if direction == 'a':
                    if car.col-step<0:
                        print('out of bounds')
                        return False
                    if self.display[car.row][car.col-i]!='.':
                        print('collision 3')
                        return False
                elif direction =='d':
                    if car.col+car.size+step>self.col:
                        print('out of bounds')
                        return False
                    if self.display[car.row][car.col+car.size-1+i]!='.':
                        print('collision 4')
                        return False
            return True

class Car(Game):
    def __init__(self,orientation,size,row,col):
        self.orientation = orientation
        self.size = size
        self.row = row
        self.col = col

def main():
    rush_hour = Game(6,6)
    rush_hour.load_game()
    rush_hour.play()

main()
