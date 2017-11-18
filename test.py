import pygame
import sys

class game:
	def __init__(self,length,width):
		self.length = length
		self.width = width
		self.display = [ ['.']*length for i in range(width)]



	def add_car(self,car_data,count):
		#new_car = car(car_data[0],car_data[1],car_data[2],car_data[3])
		if car_data[0]=='v':
			for i in range(int(car_data[2]),int(car_data[2])+int(car_data[1])):
				self.display[i][int(car_data[3])]=count
		else:
			for i in range(int(car_data[3]),int(car_data[3])+int(car_data[1])):
				self.display[int(car_data[2])][i]=count

	def load_game(self):
		data=open(sys.argv[1],'r')
		lot = []
		line = data.readline()
		while len(line)>1:
			lot.append(line[:-1].split(','))
			line = data.readline()
		count = 0
		for cars in lot:
			self.add_car(cars,count)
			count+=1

	#def move_car(self):


	def update(self):
		for i in self.display:
			for j in i:
				if type(j)==int and j>=10:
					print(j,end='  ')
				else:
					print(j,end='   ')
			print()




class car:
	def __init__(self,orientation,size,row,col):
		self.orientation = orientation
		self.row = row
		self.col = col
		self.size = size

	#def move(self,command):
		


def main():
	rush =game(6,6)
	rush.load_game()
	rush.update()

main()