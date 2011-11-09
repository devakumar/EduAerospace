import math 
import numpy 
import schemes 
from matplotlib.pylab import * 
gamma=1.4
e=0.00000001

minfsq=0.0   # For AUSM plus , AUSM up
ku=.75   # For AUSM plus , AUSM up
kp=0.25   # For AUSM plus , AUSM up
sigma=1.0   # For AUSM plus , AUSM up
beta=1.0/8.0   # For AUSM plus , AUSM up
alpha=3.0/16.0   # For AUSM plus , AUSM up

length=1.0
numCells=100
tf=.25
cfl=1.0
diphrmPostn=0.5
itrf = 10
rho_l = 1.0
u_l =  0.0             
p_l = 1

rho_r = 0.125        
u_r = 0.0              
p_r = 0.1

Info['length']=length
Info['numCells']=numCells
Info['tf']=tf
Info['cfl']=cfl
Info['diphrmPostn']=diphrmPostn
Info['itrf']=itrf

Info['rho_l']=rho_l
Info['u_l']=u_l
Info['p_l']=p_l
Info['rho_r']=rho_r
Info['u_r']=u_r
Info['p_r']=p_r

class cfdSolver(object):
	netflux=numpy.zeros((self.numCells+2,3))
	U   =  numpy.zeros((self.numCells+2,3))
	fi   =  numpy.zeros((self.numCells+2,3))
	x= numpy.zeros((self.numCells+2))
	dx = self.length/self.numCells
	dt=1.0
	t=0.0
	def __init__(self, statesInfo= Info):
		self.statesInfo = statesInfo
		self.length=statesInfo['length']
		self.numCells=statesInfo['numCells']
		self.tf=statesInfo['tf']
		self.cfl=statesInfo['cfl']
		self.diphrmPostn=statesInfo['diphrmPostn']
		self.itrf = statesInfo['itrf']

		self.rho_l = statesInfo['rho_l']
		self.u_l =  statesInfo['u_l']
		self.p_l = statesInfo['p_l']
		self.rho_r = statesInfo['rho_r']
		self.u_r = statesInfo['u_r']
		self.p_r = statesInfo['p_r']
		
		self.netflux=numpy.zeros((self.numCells+2,3))
		self.U   =  numpy.zeros((self.numCells+2,3))
		self.fi   =  numpy.zeros((self.numCells+2,3))
		self.x= numpy.zeros((self.numCells+2))
		self.dx = self.length/self.numCells
		self.dt=1.0
		self.t=0.0
		pass

	def grid(self):

		dx = self.length/self.numCells
		i=0
		while i<= (self.numCells +1):
			x[i] =(   (i*dx)-( dx/2.0)   )
			#print i,"  "
			i=i+1


	def initialisation(self):
		i = 1
		while i<=self.numCells :
			elif self.length >= self.diphrmPostn :
				if self.x[i]<= self.diphrmPostn :
					rho_initial = self.rho_l
					u_initial =  self.u_l      
					p_initial = self.p_l       
				elif self.x[i]<=self.length:                         
					rho_initial = self.rho_r   
					u_initial = self.u_r       
					p_initial = self.p_r       
			elif self.length <= self.diphrmPostn :
				print "Position of Diagphram should be less in lenght range"
		
			e_initial = 0.5 * rho_initial * u_initial * u_initial + ( p_initial/(gamma-1)   )     #/*Energy*/

			U[i][0] = rho_initial                      #/*Conserved variable 1*/    
			U[i][1] = rho_initial * u_initial         #/*Conserved variable 1*/  
			U[i][2] = e_initial                       # /*Conserved variable 1*/  
			i=i+1
	def boundaryCondtn(self):
		U[0][0]   = U[1][0]
		U[0][1]   = U[1][1]
		U[0][2]	  = U[1][2]

		U[self.numCells+1][0]   = U[self.numCells][0]
		U[self.numCells+1][1]   = U[self.numCells][1]
		U[self.numCells+1][2]   = U[self.numCells][2]

	def update(self):
		i=1
		while i<=self.numCells:
			U[i][0] = U[i][0] + dt/dx*(netflux[i][0])
			U[i][1] = U[i][1] + dt/dx*(netflux[i][1])
			U[i][2] = U[i][2] + dt/dx*(netflux[i][2])
			i=i+1

	def maxofu(self):
		tempumax=0
		i=0
		while i<= (self.numCells+1 ):
			self.ri   =U[i][0]
			self.ui   =(U[i][1])/ri
			self.pi   =((U[i][2]-(0.5*ui*ui*ri))*(gamma-1))
			#print pi ,"  ", ri,"  ", gamma
			if (self.gamma*self.pi/self.ri ) <= 0:
				ai   =math.sqrt(	math.fabs( (self.gamma*self.pi)/self.ri )    )
				print " There is a sqrt error for Sound Velcity  at time ",t," for position",x[i]," as pressure ",pi," and density ",ri
			else :
				ai   =math.sqrt(	( (gamma*pi)/ri )    )
			if(tempumax <math.fabs( (ui+ai)) ):
				tempumax=math.fabs( (ui+ai)  )
			if(tempumax <math.fabs(ui)   )	:
				tempumax=math.fabs(ui)
			if(tempumax <math.fabs( (ui-ai))):
				tempumax=math.fabs(  (ui-ai)  )
			i=i+1
		return tempumax
	def flux(self):
		i=0
		while i<=self.numCells:
			fi[i]= schemes.vanleer(U[i],U[i+1] )
			#print "  vanleer: ", fi[i],
			#print U[i]," ",U[i+1]," ",fi[i]
			#fi[i]= schemes.stegerwarming(U[i],U[i+1] )
			#fi[i]= schemes.HLLC(U[i],U[i+1] )
			#print U[i]," ",U[i+1]," ",fi[i]
			i=i+1  
		#print " ",fi
		i=1
		while i<=self.numCells:
			netflux[i][0]= fi[i-1][0]-fi[i][0]
			netflux[i][1]= fi[i-1][1]-fi[i][1]
			netflux[i][2]= fi[i-1][2]-fi[i][2]
			i=i+1
		#print " Calc",netflux[49][0],"  ",netflux[49][1],"  ",netflux[49][2]," \t ",netflux[50][0]," ",netflux[50][1]," ",netflux[50][2],"\t ",netflux[51][0]," ",netflux[51][1]," ",netflux[51][2]
	def output(self):	
		scheme="vanleer"
		#scheme="stegerwarming"
		#scheme="HLLC"
		strn= str(t) + "."+scheme+".txt"
		f= open(strn,'w')
		print " Time =",t,
		i=1
		while i<=self.numCells:
			ri   =U[i][0]
			ui   =(U[i][1])/ri
			pi   =((U[i][2]-(0.5*ui*ui*ri))*(gamma-1))
			strn=str(x[i])+"\t"+str(ri)+"\t"+str(pi)+"\t"+str(ui)+"\n" 
			#f.write(x[i],"\t",r[i],"\t",p[i],"\t",u[i],"\n" )
			f.write(strn)
			i=i+1
		f.close()
	def pltoutpt(self):
		scheme="vanleer"
		#scheme="stegerwarming"
		#scheme="HLLC"
		strn= str(t) + "."+scheme+".txt"
		f= open(strn,'r')
	
		x = numpy.zeros(self.numCells)
		ri= numpy.zeros(self.numCells)
		pi= numpy.zeros(self.numCells)
		ui= numpy.zeros(self.numCells)
		i=0
		while i<=(self.numCells-1):
			rline =f.readline()
			#rline =rline.strip()
			rline = rline .split()
			x[i]  = float(rline[0])
			ri[i] = float(rline[1])
			pi[i] = float(rline[2])
			ui[i] = float(rline[3])
			#print x[i],"  ",
			i=i+1
		figure(1)
		plot(x[1:self.numCells],ri[1:self.numCells])
		#show()
		#figure(2)
		plot(x[1:self.numCells],pi[1:self.numCells])
		show()

	def self.main():
		read_data()
		grid()
		initialisation()
		boundaryCondtn()
		#pltoutpt()
		t =0.0
		itr=0
		#while(t<self.tf):
		while(itr<self.itrf):
			flux()
			umax = maxofu()
			update()
			boundaryCondtn()
			umax = maxofu()
			dt=  1.0 *self.cfl* self.dx/umax
			#print "DTIMe", dt
			t=t+dt
			#print "For itr ",itr," The time is",t," and dt is",dt
			print U[49][0],"  ",U[49][1],"  ",U[49][2]," \t ",U[50][0]," ",U[50][1]," ",U[50][2],"\t ",U[51][0]," ",U[51][1]," ",U[51][2]
			print netflux[49][0],"  ",netflux[49][1],"  ",netflux[49][2]," \t ",netflux[50][0]," ",netflux[50][1]," ",netflux[50][2],"\t ",netflux[51][0]," ",netflux[51][1]," ",netflux[51][2]
			itr=itr+1

		print " Time Final", t
		output()
		pltoutpt()
		print " Time Final", t
#	main()
