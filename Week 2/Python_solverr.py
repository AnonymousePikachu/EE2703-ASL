from cmath import cos,sin
from sys import argv,exit
import numpy as np

CIRCUIT=".circuit"              #Variables for identifying different lines in netlist file
END=".end"
AC=".ac"
freq_index = -1             #Variable to check if the circuit is AC/DC         

if len(argv) != 2:              #Error message for wrong input
    print('more than 1 argument')
    exit()

try:                    
    with open(argv[1]) as f:                #Reading file contents and storing important indices
        lines = f.readlines()  
        start = -1; end = -2
        for line in lines:                
            if CIRCUIT == line[:len(CIRCUIT)]:
                start = lines.index(line)
            elif END == line[:len(END)]:
                end = lines.index(line)
            elif AC == line[:len(AC)]:
                freq_index = lines.index(line)

        if start >= end:                      
            print('Invalid circuit definition')
            exit(0)

except IOError:             #Error message for invalid file
    print('Invalid file')
    exit()

nodes = [0]                 #Array of nodes, 0 indicates ground node
num_nodes = 0               #number of nodes
num_VSs = 0                 #number of voltage sources
node_voltages = []          #Lists containing different types of components
branch_currents = []
Resistors = []
Capacitors = []
Inductors = []
DCVSs = []
ACVSs = []
DCCSs = []
ACCSs = []

for line in lines[start+1:end]:             #Adding all the nodes to nodes array
    if line.split()[1]!="GND":
        if int(line.split()[1]) not in nodes:
            nodes.append(int(line.split()[1]))
    if line.split()[2]!="GND":
        if int(line.split()[2]) not in nodes:
            nodes.append(int(line.split()[2]))

num_nodes=len(nodes)                #length of nodes array gives number of nodes

class Resistor:             #Class for all resistor components             

    def __init__(self,name,nA,nB,value):
        self.name = name
        self.nA = nA
        self.nB = nB
        self.value = value

    def Reqn(self):             #Function to return conductance/admittance
        return 1/self.value


class Capacitor:                #Class for all capacitor components                

    def __init__(self,name,nA,nB,value):
        self.name = name
        self.nA = nA
        self.nB = nB
        self.value = value

    def Ceqn(self):             #Function to return admittance
        return (w*self.value)*1j

class Inductor:                 #Class for all inductor components  

    def __init__(self,name,nA,nB,value):
        self.name = name
        self.nA = nA
        self.nB = nB
        self.value = value

    def Leqn(self):             #Function to return admittance
        return (-1/(w*self.value))*1j

class DCVoltageSource:              #Class for all dc voltage sources

    def __init__(self,name,nA,nB,value):
        self.name = name
        self.nA = nA
        self.nB = nB
        self.value = value

class ACVoltageSource:              #Class for all ac voltage sources   

    def __init__(self,name,nA,nB,value,phase):
        self.name = name
        self.nA = nA
        self.nB = nB
        self.value = value
        self.phase = phase

    def ACVSeqn(self):              #Function to return Voltage phasor
        return (self.value/2)*((cos(self.phase))+(sin(self.phase)*1j))

class DCCurrentSource:              #Class for all dc current sources

    def __init__(self,name,nA,nB,value):
        self.name = name
        self.nA = nA
        self.nB = nB
        self.value = value

class ACCurrentSource:              #Class for all ac current sources

    def __init__(self,name,nA,nB,value,phase):
        self.name = name
        self.nA = nA
        self.nB = nB
        self.value = value
        self.phase = phase

    def ACCSeqn(self):              #Function to return current phasor
        return (self.value/2)*((cos(self.phase))+(sin(self.phase)*1j))

if freq_index!=-1:              #To take the frequency of the ac circuit
    w = float(lines[freq_index].split()[2])

for line in lines[start+1:end]:             #Parsing all the file tokens and adding it to respective lists accordingly
    words=line.split()
    if words[1]=="GND":             #Converting GND to 0th node
        words[1]="0"
    if words[2]=="GND":
        words[2]="0"
    if line[0]=="R":
        Resistors.append(Resistor(words[0],int(words[1]),int(words[2]),float(words[3])))
    if line[0]=="C":
        Capacitors.append(Capacitor(words[0],int(words[1]),int(words[2]),float(words[3])))
    if line[0]=="L":
        Inductors.append(Inductor(words[0],int(words[1]),int(words[2]),float(words[3])))
    if line[0]=="V":
        if words[3]=="dc":
            DCVSs.append(DCVoltageSource(words[0],int(words[1]),int(words[2]),float(words[4])))
        elif words[3]=="ac":
            ACVSs.append(ACVoltageSource(words[0],int(words[1]),int(words[2]),float(words[4]),float(words[5])))
    if line[0]=="I":
        if words[3]=="dc":
            DCCSs.append(DCCurrentSource(words[0],int(words[1]),int(words[2]),float(words[4])))
        elif words[3]=="ac":
            ACCSs.append(ACCurrentSource(words[0],int(words[1]),int(words[2]),float(words[4]),float(words[5])))

num_VSs = len(DCVSs) + len(ACVSs)               
neq = num_nodes+num_VSs             #Number of nodal analysis equations

M=np.zeros((neq,neq),dtype=complex)             #M and B matrices for nodal analysis matrix equation MX=B
B=np.zeros(neq,dtype=complex)

for r in Resistors:                             #Modifying M and B matrices for various components according to the algorithm
    M[r.nA,r.nA] = M[r.nA,r.nA] + r.Reqn()
    M[r.nA,r.nB] = M[r.nA,r.nB] - r.Reqn()
    M[r.nB,r.nA] = M[r.nB,r.nA] - r.Reqn()
    M[r.nB,r.nB] = M[r.nB,r.nB] + r.Reqn()

for c in Capacitors:
    M[c.nA,c.nA] = M[c.nA,c.nA] + c.Ceqn()
    M[c.nA,c.nB] = M[c.nA,c.nB] - c.Ceqn()
    M[c.nB,c.nA] = M[c.nB,c.nA] - c.Ceqn()
    M[c.nB,c.nB] = M[c.nB,c.nB] + c.Ceqn()

for l in Inductors:
    M[l.nA,l.nA] = M[l.nA,l.nA] + l.Leqn()
    M[l.nA,l.nB] = M[l.nA,l.nB] - l.Leqn()
    M[l.nB,l.nA] = M[l.nB,l.nA] - l.Leqn()
    M[l.nB,l.nB] = M[l.nB,l.nB] + l.Leqn()

for dcv in DCVSs:
    M[dcv.nA,num_nodes+int(dcv.name[1])-1] = M[dcv.nA,num_nodes+int(dcv.name[1])-1] + 1
    M[dcv.nB,num_nodes+int(dcv.name[1])-1] = M[dcv.nB,num_nodes+int(dcv.name[1])-1] - 1
    M[num_nodes+int(dcv.name[1])-1,dcv.nA] = 1
    M[num_nodes+int(dcv.name[1])-1,dcv.nB] = -1
    B[num_nodes+int(dcv.name[1])-1] = dcv.value

for dci in DCCSs:
    B[dci.nA] = -dci.value
    B[dci.nB] = dci.value

for acv in ACVSs:
    M[acv.nA,num_nodes+int(acv.name[1])-1] = M[acv.nA,num_nodes+int(acv.name[1])-1] + 1
    M[acv.nB,num_nodes+int(acv.name[1])-1] = M[acv.nB,num_nodes+int(acv.name[1])-1] - 1
    M[num_nodes+int(acv.name[1])-1,acv.nA] = 1
    M[num_nodes+int(acv.name[1])-1,acv.nB] = -1
    B[num_nodes+int(acv.name[1])-1] = acv.ACVSeqn()

for aci in DCCSs:
    B[aci.nA] = -aci.ACCSeqn()
    B[aci.nB] = aci.ACCSeqn()

X = np.linalg.solve(M,B)                #Using numpy solver to invert and solve for the X matrix
temp=X[0]
for i in range(num_nodes):              #Making the ground voltage 0, so that all other node voltages are in relation to the ground node
    X[i]=X[i]-temp

for k in range(num_nodes):
    print("V%d=({0.real:0.10f})+({0.imag:0.10f})j".format(X[k])%k)              #Printing node voltages 

for l in range(num_VSs):
    print("Iv%d=({0.real:0.10f})+({0.imag:0.10f})j".format(X[num_nodes+l])%(l+1))               #Printing current through voltage sources

