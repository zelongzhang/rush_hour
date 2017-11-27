import pygame
import sys


'''Game of Rush Hour. The object of the game is to move the red car, in this case, car 0 from the its starting location to the very right of row 3. 
    Other cars will obstruct the path and the player needs to move them along their orientation to maneuver the red car to the destination.
    Cars cannot pass through one another and the entirety of any cars must be inside the boundaries at all times.'''
class Game:
    def __init__(self,game_row,game_col):
        self.row = game_row
        self.col = game_col
        self.display = [['.']*game_row for i in range(game_col)]
        self.cars={}
        self.lot=[]

    #read the data fil and convert it into the display which will be the text based grid and a 
    # dictionary of car objects which can be called by their reference #/license
    def load_game(self):
        data = open(sys.argv[1],'r')
        line = data.readline()
        
        while len(line)>1: #get lines from file
            self.lot.append(line[:-1].split(', '))
            line = data.readline()
        
        license=0 #car identifier
        
        for car in self.lot: #makes a Car object for each line and puts them into self.cars then generates the initial state of the display
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

    #Updates the game state. Prints the entire display list.
    def update(self):                   
        for i in self.display:
            for j in i:
                if j.isdigit() and int(j)>=10:
                    print(j , end = ' ')
                else:
                    print(j, end ='  ')
            print()

    #Mainloop function. Takes commands from user and if it's a valid move, make the move on the board.
    def play(self):
        while not self.game_end():
            command_car = self.get_input(1,[i for i in range(0,len(self.cars))],'enter which car to move ')
            command_direction = self.get_input('s','wasd','enter the direction to move (wasd) ')
            command_step = self.get_input(1,[i for i in range(0,self.row+1)],'enter how far to move ')
           
            if self.check(self.cars[str(command_car)],command_direction,command_step):
                print('hey')
                self.move(self.cars[str(command_car)],command_direction,command_step,command_car)
            else:
                print('invalid move')
            self.update() 

    #sets up winning condition and end. True if condition is met. False if it's not
    def game_end(self):
        if self.display[2][5]=='0':
            print('you won')
            return True
        return False

    #moves a car accoding to user instructions by updating the board and car objects
    #@param car - Car to be moved
    #@param direction,step - direction and step instructions from user
    #@param license - Identifier of car to be moved
    def move(self,car,direction,step,license):
        for i in range(step):
            if car.orientation=='v' and direction=='w':#if the car is vertical and user wants to move up
                self.display[car.row-1][car.col]=str(license) #the block above becomes the license of the car
                self.display[car.row+car.size-1][car.col]='.' #the block below becomes .
                car.row-=1  #Car instance variable is updated to reflect the change
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

    #checks if the user designated move is legal for the car.
    def check(self,car,direction,step):
        #checks vertical cars
        if car.orientation == 'v':
            for i in range(1,step+1):
                #checks for moving up
                if direction == 'w':
                    #checks if car goes out of bounds
                    if car.row-step<0:
                        print('out of bounds')
                        return False
                    #checks if car collides with another car
                    if self.display[car.row-i][car.col]!='.':
                        print('collision')
                        return False

                elif direction =='s':
                    if car.row+car.size+step>self.row:
                        print('out of bounds')
                        return False
                    if self.display[car.row+car.size-1+i][car.col]!='.':
                        print('collision')
                        return False
                else:
                    print('that car doesn''t go that way')
                    return False
            return True
        #check horizontal cars
        elif car.orientation == 'h':
            for i in range(1,step+1):
                if direction == 'a':
                    if car.col-step<0:
                        print('out of bounds')
                        return False
                    if self.display[car.row][car.col-i]!='.':
                        print('collision')
                        return False

                elif direction =='d':
                    if car.col+car.size+step>self.col:
                        print('out of bounds')
                        return False
                    if self.display[car.row][car.col+car.size-1+i]!='.':
                        print('collision')
                        return False
                else:
                    print('that car doesn''t go that way')
                    return False
            return True
    
    def get_input(self,sample,range,prompt):
        while True:
            if type(sample) == int:
                try:
                    i=int(input(prompt))
                    if i not in range:
                        print('Please enter an integet between ',range[0],' and ',range[-1])
                    else:
                        return i
                except ValueError:
                    print('Please enter an integer')
            if type(sample) == str:
                try:
                    s=str(input(prompt))
                    if s not in range:
                        print('Please enter a direction (wasd)')
                    else:
                        return s
                except ValueError:
                    print('Please enter an str')


#Car class used to store each individual car's orientation, size, and position
class Car:
    def __init__(self,orientation,size,row,col):
        self.orientation = orientation
        self.size = size
        self.row = row
        self.col = col


def main():
    game_row=6
    game_col=6
    rush_hour = Game(game_row,game_col)
    rush_hour.load_game()
    rush_hour.play()

main()