#			SIDHARTH S KUMAR 
# 				EE21B130

# To use this program type in the following command in the terminal while in the same directory as the netlist and the python file
# `python netlist_solver.py ckt1.netlist`
# ckt1 can be replaced with any other file name


# Importing the necessary modules.
from numpy import *
from sys import argv, exit

#Gaussian Solver funstion from the previous question
def Linear_solver(A,b):
    A = array(A,dtype=float)
    b = array(b,dtype=float)
    size = len(b) - 1
    
    # Exception for wrong format of matrix passed
    if A.shape[0] != b.shape[0]:
        raise Exception("The number of rows in A and b must be the same.")
        
    if linalg.det(A) == 0:
            raise Exception("The matrix A is singular, and cannot be inverted.")

    #Pivoting the matrix to avoid zero errors
    for j in range(size):
        Max = j
        for k in range(j,size):
            if abs(A[k][j]) > abs(A[Max][j]) :
                Max = k
        A[[j, Max]] = A[[Max, j]]

        for i in range(size-j):
            fact = A[j][j]/A[i+j+1][j]
            A[i+j+1] = fact*A[i+j+1] - A[j]
            b[i+j+1] = fact*b[i+j+1] - b[j]

    #Finding the diagonal matrix
    for j in range(size,0,-1):
        for i in range(size):
            fact = A[j-i-1][j]/A[j][j]
            A[j-i-1] = A[j-i-1] - fact*A[j]
            b[j-i-1] = b[j-i-1] - fact*b[j]
            
    for i in range(size):
        b[i] = b[i]/A[i][i]    
    return b

# Class declared for components.
class Component:
	def __init__(self,name,nA,nB,value):
		self.name = name
		self.nA = nB
		self.nB = nA
		self.value = value

# The program will throw in an error if there isn't exactly 2 arguments in the commandline.
if len(argv)!=2:
	print("Please provide the correct 2 arguments in the commandline.")
	exit()

# Assigning constants variables to .circuit and .end 
CIRCUIT = ".circuit"
END = ".end"
AC = ".ac"

# Global exception for invalid file type
try:

	# Opening the file mentioned in the commandline.
	with open(argv[1]) as f:
		lines = f.readlines()

	# These are parameters to check the errors in the file format. 		
		start = -1; start_check = -1; end = -2; end_check = -1; ac = -1 ; ac_check = -1

	# The program will traverse through the file and take out only the required part.
		for line in lines:
			if CIRCUIT == line[:len(CIRCUIT)]:
				start = lines.index(line)
				start_check = 0

			elif END == line[:len(END)]:
				end = lines.index(line)
				end_check = 0
	#This part is to check if the circuit has an AC or a DC source. 	
			elif AC == line[:len(AC)]:
				ac = lines.index(line)
				ac_check = 1

	# The program will throw in an error if the circuit definition format is not proper.		
		if start >= end or start_check == -1 or end_check == -1:
			print("Invalid circuit definition.")
			exit()

	# Creating a list and storing the necessary information into it.			
		l = [] ; k=0
	# In case of an AC circuit, the required information is collected.		
		try:
			if ac_check ==1:
				_,ac_name,freq = lines[ac].split("#")[0].split()
				freq = 2*pi*float(freq)

			for line in (lines[start+1:end]):
				name,nA,nB,*value = line.split("#")[0].split()

				if name[0] == 'R' or name[0] == 'C' or name[0] == 'L' or name[0] == 'I':
					element = Component(name,nA,nB,value)
					
				elif name[0] == 'V':
					element = Component(name,nA,nB,value)
					k = k+1

		# Converting the values of the components into real numbers 
				if len(element.value) == 1:
						element.value = float(element.value[0])	

		# In case of an AC source, the voltage and phase are assigned properly.
				elif value[0] == "ac":
					element.value = (float(element.value[1])/2)*complex(cos(float(element.value[2])),sin(float(element.value[2])))

				else:
					element.value = float(element.value[1])
							

				l.append(element)

	# The program will throw an error if the netlist is not written properly.
		except IndexError:
			print("Please make sure the netlist is written properly.")	
			exit()

	# Nodes are creating using a dictionary.
	node ={}
	for element in l:
		if element.nA not in node:
			if element.nA == 'GND':
				node['n0'] = 'GND'
			else:	
				name = "n" + element.nA
				node[name] = int(element.nA[-1])

		if element.nB not in node:
			if element.nB == 'GND': 
				node['n0'] = 'GND'
			else:	
				name = "n" + element.nB 	
				node[name] = int(element.nB[-1])

	node['n0'] = 0			
	n = len(node)

	# Creating the N and b matrices for solving the equations.
	N = zeros(((n+k-1),(n+k-1)),dtype="complex_")
	b = zeros(((n+k-1),1),dtype="complex_")
	p=0

	# This part of code will fill the matrices N and b taking into consideration if it is an AC or a DC source.
	for element in l:

	# In case of a resistor, the matrix N is filled in a certain way as shown below.		
		if element.name[0] == 'R':
			if element.nB == 'GND': 
				N[int(element.nA[-1])-1][int(element.nA[-1])-1] += 1/element.value

			elif element.nA == 'GND':
				N[int(element.nB[-1])-1][int(element.nB[-1])-1] += 1/element.value
					
			else:	
				N[int(element.nA[-1])-1][int(element.nA[-1])-1] += 1/element.value
				N[int(element.nB[-1])-1][int(element.nB[-1])-1] += 1/element.value
				N[int(element.nA[-1])-1][int(element.nB[-1])-1] += -1/element.value
				N[int(element.nB[-1])-1][int(element.nA[-1])-1] += -1/element.value

	# In case of a capacitor, the impedance is calculated first and then the matrix N is filled.
		elif element.name[0] == 'C':
			if ac_check ==1:
				Xc = -1/(float(element.value)*freq)
				element.value = complex(0,Xc)

			if element.nB == 'GND': 
				N[int(element.nA[-1])-1][int(element.nA[-1])-1] += 1/element.value
			elif element.nA == 'GND':
				N[int(element.nB[-1])-1][int(element.nB[-1])-1] += 1/element.value
					
			else:	
				N[int(element.nA[-1])-1][int(element.nA[-1])-1] += 1/element.value
				N[int(element.nB[-1])-1][int(element.nB[-1])-1] += 1/element.value
				N[int(element.nA[-1])-1][int(element.nB[-1])-1] += -1/element.value
				N[int(element.nB[-1])-1][int(element.nA[-1])-1] += -1/element.value

	# In case of an inductor, the impedance is calculated first and then the matrix N is filled.
		elif element.name[0] == 'L':
			if ac_check ==1:
				Xl = (float(element.value)*freq)
				element.value = complex(0,Xl)

			if element.nB == 'GND': 
				N[int(element.nA[-1])-1][int(element.nA[-1])-1] += 1/element.value
			elif element.nA == 'GND':
				N[int(element.nB[-1])-1][int(element.nB[-1])-1] += 1/element.value
					
			else:	
				N[int(element.nA[-1])-1][int(element.nA[-1])-1] += 1/element.value
				N[int(element.nB[-1])-1][int(element.nB[-1])-1] += 1/element.value
				N[int(element.nA[-1])-1][int(element.nB[-1])-1] += -1/element.value
				N[int(element.nB[-1])-1][int(element.nA[-1])-1] += -1/element.value

	# In case of a current source, the matrix b is filled as shown.
		elif element.name[0] == 'I':
			if element.nB == 'GND':
				b[int(element.nA[-1])-1][0] += element.value

			elif element.nA == 'GND':
				b[int(element.nB[-1])-1][0] += -element.value

			else:
				b[int(element.nA[-1])-1][0] += element.value
				b[int(element.nB[-1])-1][0] += -element.value

	# In case of a voltage source, the matrices N and b are filled as shown.
		elif element.name[0] == 'V':
			if element.nB == 'GND':
				N[int(element.nA[-1])-1][n-1+p] += 1
				N[n-1+p][int(element.nA[-1])-1] += 1
				b[n-1+p] += element.value
				p = p+1			
			elif element.nA == 'GND':
				N[int(element.nB[-1])-1][n-1+p] += -1
				N[n-1+p][int(element.nB[-1])-1] += -1
				b[n-1+p] += element.value
				p = p+1			
			else:	
				N[int(element.nA[-1])-1][n-1+p] += 1
				N[int(element.nB[-1])-1][n-1+p] += -1
				N[n-1+p][int(element.nA[-1])-1] += 1
				N[n-1+p][int(element.nB[-1])-1] += -1
				b[n-1+p] += element.value
				p = p+1

	# I tried using both linalg.solve() and my function Linear_solver(), 
	# but due to some issue the Linear_solver funciton is not working from this particular case
	V = linalg.solve(N,b)
	# V = Linear_solver(N,b)
	print(V,"\n")			

	for i in range(n-1):
		print("V",i+1,"=",V[i],"\n")
	for j in range(k):
		print("I",j+1,"=",V[j+n-1],"\n")

# The program will throw in this error if the name of the netlist file is not proper 
# or if the netlist file is not found in the same directory as the program.

except FileNotFoundError:
	print("Invalid File.")
	exit()