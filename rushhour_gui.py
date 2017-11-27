import pygame
import sys


'''Game of rush hour with a GUI. Users navigate the red car from its starting position to 
the winning square which is the very right block on the third row. Users click and drag the cars to move them along their orientations.
However, no cars can move sideways, have any collision or leave the grid at any time.'''


#Game class contains elements of the rush hour game. Contains class variables and methods for the GUI.
class Game:

	def __init__(self,x,y,res):
		pygame.init() #initializes pygame
		self.block_size = res
		self.screen_x=x*self.block_size
		self.screen_y=y*self.block_size
		self.display = pygame.display.set_mode((self.screen_x,self.screen_y)) #sets up display
		pygame.display.set_caption('Rush Hour')
		self.cars=[]	#list of car objects
		self.winning_block = pygame.rect.Rect(5*self.block_size,2*self.block_size,self.block_size,self.block_size) #assigns the winning block
		self.clock = pygame.time.Clock() #for timing control
		self.fps = 60
		self.load_game() #loads the map from data file

	#loads the game from a data file. First entry in the file is the Red_car with subsequent entries being the other cars.
	#A new object is made for each entry and added to self.cars
	def load_game(self):
		lot = []
		data = open(sys.argv[1],'r') #opens the file
		line = data.readline()
		while len(line)>1: #get the lines from file
			lot.append(line[:-1].split(', '))
			line = data.readline()
		red_car = Red_car(lot[0][0],int(lot[0][1]),int(lot[0][2]),int(lot[0][3]),self.block_size) #First entry is Red_car
		self.cars.append(red_car)
		del lot[0]
		for car in lot: #all other entries are Other_car
			new_car = Other_car(car[0],int(car[1]),int(car[2]),int(car[3]),self.block_size)
			self.cars.append(new_car)

	#Function for displaying some text on the GUI screen. 
	#@param display - surface that the text is to be displayed on
	#@param message - text string to be displayed
	#@param dest - location on surface where the text will appear
	#Referenced from https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
	def display_text(self,display,message,dest):
		font = pygame.font.SysFont(None,35)
		text_color = (255,255,0)
		text_to_screen = font.render(message,True,text_color)
		display.blit(text_to_screen,dest)


	#Blit all the cars onto the display surface
	def draw_state(self):
		for car in self.cars:
			self.display.blit(car.image,car.rect)

	#Checks if the Red_car is in the winning block
	def win(self,car):
		car_block = pygame.rect.Rect(car.rect.x+self.block_size,car.rect.y,self.block_size,self.block_size)
		if car_block == self.winning_block:
			return True
		return False

	#Checks if a drag move on a car is legal or not. Returns True if legal and False if not.
	def check(self,car,orig_x,orig_y,direction):
		#checks if the car moves or not. If not,then return False
		if orig_x==car.rect.x and orig_y==car.rect.y:
			#print('in place')
			return False
		#Based on the orientation and the direction of the drag, makes a traj rectangle and a boundary boolean.
		#The traj rectangle represents the total space occupied by a drag move./
		#For example, for a car moving from the very left to the very right in a row,/
		#a traj would be a rectangle which takes up that entire row.
		#Boundary is a boolean which checks if the car is still entirely in the screen
		if direction=='h':
			if orig_x>car.rect.x:
				traj = pygame.rect.Rect(car.rect.x,car.rect.y,orig_x+car.size-car.rect.x,self.block_size)
				boundary = 0<=car.rect.x<=self.screen_x
			else:
				traj = pygame.rect.Rect(orig_x,orig_y,car.rect.x+car.size-orig_x,self.block_size)
				boundary = 0<=car.rect.x+car.size<=self.screen_x
		else:
			if orig_y<car.rect.y:
				traj = pygame.rect.Rect(orig_x,orig_y,self.block_size,car.rect.y+car.size-orig_y)
				boundary = 0<=car.rect.y+car.size<=self.screen_y
			else:
				traj = pygame.rect.Rect(car.rect.x,car.rect.y,self.block_size,orig_y+car.size-car.rect.y)
				boundary = 0<=car.rect.y<=self.screen_y

		for i in self.cars:
			if not boundary: #checks if the car is out of bounds
				#print('boundary')
				return False
			if i!=car: #checks for collisions. If traj collides with any other car, there is a collision
				if traj.colliderect(i.rect):
					#print('collide')
					return False
		return True

	#Draws grid lines to show each block.
	def draw_grid(self):
		black = (0,0,0)
		for i in range(0,self.screen_x+1,self.block_size):
			pygame.draw.line(self.display,black,(i,0),(i,self.screen_y),10)
		for j in range(0,self.screen_y+1,self.block_size):
			pygame.draw.line(self.display,black,(0,j),(self.screen_x,j),10)

	#Mainloop function which handles user input and makes changes to car instances based on the commands. 
	def play(self):
		self.clock.tick(self.fps) #set refresh rate
		drag=False	#True if user is dragging a car for a move
		running= True #True if user has not clicked the quit button
		turn = 0 #counter for number of moves

		#Drag and drop referenced from https://stackoverflow.com/questions/41332861/click-and-drag-a-rectangle-with-pygame
		while running:

			if not self.win(self.cars[0]): #if self.win, then no longer updates the screen
				bg_color = (50,192,182)
				self.display.fill(bg_color) #fill out the screen
				self.draw_grid()	#then draw the grid
				self.draw_state()	#then draw the cars
			else:
				self.display.fill(bg_color)
				self.draw_grid()
				self.draw_state()
				self.display_text(self.display,'You Won in '+str(turn)+' Moves',[self.screen_x/2-100,self.screen_y/2])
			
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					running=False

				elif self.win(self.cars[0]): #stops inputs once won
					continue

				elif event.type==pygame.MOUSEBUTTONDOWN: #handles left and right mouse button clicks
					for i in self.cars:
						if i.rect.collidepoint(event.pos): #finds which car is clicked
							car = i
							drag=True 
							orig_x=car.rect.x
							orig_y=car.rect.y
							x,y = event.pos
							off_x = car.rect.x-x
							off_y = car.rect.y-y
				elif event.type==pygame.MOUSEBUTTONUP: #handles left and right mouse button release
					drag = False
					car.rect.x = round(car.rect.x/self.block_size)*self.block_size #"snaps" the car into grid
					car.rect.y = round(car.rect.y/self.block_size)*self.block_size
					if car.orientation=='h': 
						if car.rect.y == orig_y and self.check(car,orig_x,orig_y,'h'):#if car is horizontal, its final y should equal its initial y
								turn+=1 												#then checks if the move is legal.
						else: #if moved sideways or not legal, car goes back to its original location
							car.rect.x = orig_x
							car.rect.y = orig_y
					else:	#if car is vertical, its final and initial x should be the same, then checks if move is legal.
						if car.rect.x == orig_x and self.check(car,orig_x,orig_y,'v'):
								turn+=1
						else: #moves car back to original location 
							car.rect.x = orig_x
							car.rect.y = orig_y

				elif event.type==pygame.MOUSEMOTION: #handles mouse movenements
					if drag:	#if a car has been clicked and is being dragged
						x,y = event.pos
						car.rect.x = x+off_x
						car.rect.y = y+off_y
						
			self.display_text(self.display,'Moves: '+str(turn),[270,20]) #displays the number of legal moves user has made.
			pygame.display.update() #updates the display surface


#Car sprite super class. Contains class variables that all cars should have: orientation, size, and position
#Block size determines how big each square grid block is 
class Car(pygame.sprite.Sprite,Game):
	def __init__(self,orientation,size,row,col,block_size):
		super(Car,self).__init__()
		self.orientation = orientation
		self.block_size = block_size
		self.size = size*self.block_size
		self.x = col*self.block_size
		self.y = row*self.block_size

#Child class Red_car defines the car which users must move to the target destination in order to win. 
#sprite image obtained from https://openclipart.org/detail/61201/red-racing-car-top-view
class Red_car(Car):
	def __init__(self,orientation,size,row,col,block_size):
		Car.__init__(self,orientation,size,row,col,block_size) #calls superclass init
		self.image = pygame.image.load('red_car.png')# assigns an image to the instance
		self.rect = pygame.rect.Rect(self.x,self.y,self.size,self.block_size) #assigns a rectangle the size of red car

#Child class Other_cars define the other vehicles obstructing the red car's path. They can either be of length 2 or 3 
# with either a vertical or horizontal orientation.
class Other_car(Car):
	def __init__(self,orientation,size,row,col,block_size):
		Car.__init__(self,orientation,size,row,col,block_size)
		if orientation=='h': #assigns images and rectangles for horizontal cars
				self.rect = pygame.rect.Rect(self.x,self.y,self.size,self.block_size)
				if size ==2:
					self.image = pygame.image.load('2_h.png')
				elif size ==3:
					self.image = pygame.image.load('3_h.png')
		else: #assigns images and rectangles for vertical cars
			self.rect = pygame.rect.Rect(self.x,self.y,self.block_size,self.size)
			if size ==2:
				self.image = pygame.image.load('2_v.png')
			elif size ==3:
				self.image = pygame.image.load('3_v.png')


def main():
	game_grid_length=6
	game_grid_width=6
	game_resolution=100
	rush_hour = Game(game_grid_length,game_grid_width,game_resolution)
	rush_hour.play()
main()