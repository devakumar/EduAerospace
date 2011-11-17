import math 
import numpy 
#import schemes 
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
Info ={}
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

Info['minfsq']=minfsq   # For AUSM plus , AUSM up
Info['ku'] = ku   # For AUSM plus , AUSM up
Info['kp'] = kp  # For AUSM plus , AUSM up
Info['sigma'] = sigma   # For AUSM plus , AUSM up
Info['beta'] = beta   # For AUSM plus , AUSM up
Info['alpha'] = alpha   # For AUSM plus , AUSM up

class cfdSolver(object):
#	self.netflux=numpy.zeros((self.numCells+2,3))
#	self.U   =  numpy.zeros((self.numCells+2,3))
#	self.fi   =  numpy.zeros((self.numCells+2,3))
#	x= numpy.zeros((self.numCells+2))
#	dx = self.length/self.numCells
#	dt=1.0
#	t=0.0
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

		self.dx = self.length/self.numCells
		i=0
		while i<= (self.numCells +1):
			x[i] =(   (i*dx)-( dx/2.0)   )
			#print i,"  "
			i=i+1


	def initialisation(self):
		i = 1
		while i<=self.numCells :
			if self.length >= self.diphrmPostn :
				if self.x[i]<= self.diphrmPostn :
					rho_initial = self.rho_l
					u_initial =  self.u_l      
					p_initial = self.p_l       
				elif self.x[i]<=self.length :                         
					rho_initial = self.rho_r   
					u_initial = self.u_r       
					p_initial = self.p_r       
			elif self.length <= self.diphrmPostn :
				print "Position of Diagphram should be less in lenght range"
		
			e_initial = 0.5 * rho_initial * u_initial * u_initial + ( p_initial/(gamma-1)   )     #/*Energy*/

			self.U[i][0] = rho_initial                      #/*Conserved variable 1*/    
			self.U[i][1] = rho_initial * u_initial         #/*Conserved variable 1*/  
			self.U[i][2] = e_initial                       # /*Conserved variable 1*/  
			i=i+1
	def boundaryCondtn(self):
		self.U[0][0] = self.U[1][0]
		self.U[0][1] = self.U[1][1]
		self.U[0][2] = self.U[1][2]

		self.U[self.numCells+1][0] = self.U[self.numCells][0]
		self.U[self.numCells+1][1] = self.U[self.numCells][1]
		self.U[self.numCells+1][2] = self.U[self.numCells][2]

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
			self.ri = U[i][0]
			self.ui = (U[i][1])/ri
			self.pi = ((U[i][2]-(0.5*ui*ui*ri))*(gamma-1))
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
	
		self.x = numpy.zeros(self.numCells)
		self.ri= numpy.zeros(self.numCells)
		self.pi= numpy.zeros(self.numCells)
		self.ui= numpy.zeros(self.numCells)
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

	def main(self):
		print "COMing In"
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
			self.dt=  1.0 *self.cfl* self.dx/umax
			update()
			boundaryCondtn()
			itr=itr+1
			self.t=self.t+self.dt
			plt()

			#print "DTIMe", dt
			#print "For itr ",itr," The time is",t," and dt is",dt
			#print U[49][0],"  ",U[49][1],"  ",U[49][2]," \t ",U[50][0]," ",U[50][1]," ",U[50][2],"\t ",U[51][0]," ",U[51][1]," ",U[51][2]
			#print netflux[49][0],"  ",netflux[49][1],"  ",netflux[49][2]," \t ",netflux[50][0]," ",netflux[50][1]," ",netflux[50][2],"\t ",netflux[51][0]," ",netflux[51][1]," ",netflux[51][2]

		print " Time Final", t
		output()
		pltoutpt()
		print " Time Final", t
#	main()


class schemes(object):
	def __init__(self, statesInfo= Info):
		self.statesInfo = statesInfo
		self.minfsq=statesInfo['minfsq']
		self.ku=statesInfo['ku']
		self.kp=statesInfo['kp']
		self.sigma=statesInfo['sigma']
		self.beta=statesInfo['beta']
		self.alpha = statesInfo['alpha']	
	def vanleer(Ui,Ui1):
		#print "vanleer"
		fpi  = numpy.array([0.0,0.0,0.0])
		fni1 = numpy.array([0.0,0.0,0.0])
		fi   = numpy.array([0.0,0.0,0.0])

		ri   =Ui[0]
		ui   =(Ui[1])/ri
		pi   =((Ui[2]-(0.5*ui*ui*ri))*(gamma-1))
		ai   =math.sqrt((gamma*pi)/ri )    
		mi   = ui/ai

		ri1  =Ui1[0]
		ui1  =(Ui1[1])/ri1
		pi1  =((Ui1[2]-(0.5*ui1*ui1*ri1))*(gamma-1))
		ai1  = math.sqrt((gamma*pi1)/ri1 )   
		mi1  = ui1/ai1

		if( (math.fabs(mi) ) < (1+ ei ) ) :
			#	print "(math.fabs(mi) ) < (1+ e )",
			fpi[0] = float((ai*ri)*(0.25*(mi+1)*(mi+1)) )
			#print " fpi[0]= ",fpi[0], "(ai*ri)*(0.25*(mi+1)*(mi+1))" ,float((ai*ri)*(0.25*(mi+1)*(mi+1)))
			fpi[1] = fpi[0]*(   (	( (gamma-1)*ui)	+	(2*ai)	)/gamma)
			#print "fpi[1]: ",fpi[1]
			fpi[2] = fpi[0]*(((((gamma-1)*ui+2*ai)*((gamma-1)*ui+2*ai))/(2*(gamma*gamma-1))))
			#print "\t 1 fpi[2]=",fpi[2], " fpi[0]= ",fpi[0], "(ai*ri)*(0.25*(mi+1)*(mi+1))=",(ai*ri)*(0.25*(mi+1)*(mi+1))
			#print "\t 1 fpi1[1]= ",fpi[1]," fpi[0]*(   (	( (gamma-1)*ui)	+	(2*ai)	)/gamma)= ",(fpi[0]*(   (	( (gamma-1)*ui)	+	(2*ai)	)/gamma) )
		elif mi >1 :
			#	print "mi1>1",
			fpi[0]= mi* ri * ai
			fpi[1]=  ai* ai*ri*(mi*mi+ (1/gamma) ) 
			fpi[2]= ri* ai* ai* ai *mi*(.5 *mi*mi+ (    1 /(gamma - 1)  ) )
		elif mi < -1:
			#	print "mi1<-1",
			fpi[0]=0.0
			fpi[1]= 0.0
			fpi[2]= 0.0

		if( (math.fabs(mi1) ) < (1+ ei ) ) :
			#	print "(math.fabs(mi1) ) < (1+ e ) ",
			#fni1[0]= mi1* ri1 * ai1
			#fni1[1]=  ai1* ai1*ri1*(mi1 *mi1 + (1/gamma) ) 
			#fni1[2]= ri1* ai1* ai1* ai1 *mi1 *(.5 *mi1 *mi1+ (    1 /(gamma - 1)  ) )
			#fpi10=(0.25*(mi1+1)*(mi1+1))
		
			#fni1[0]=ri1*ui1 - fni1[0]
			#fni1[1]=ri1*ui1*ui1+pi1 - fni1[1]
			#print "\t 3 fni1[1]= ",fni1[1]
			#fni1[2]=(((ai1*ai1)/(gamma-1))+0.5*(ui1*ui1))*ri1*ui1 -fni1[2]

			fpi10=(0.25*(mi1+1)*(mi1+1))
			fni1[0]= ri1*ui1- (ai1*ri1)* fpi10
			fni1[1]= ri1*ui1*ui1+pi1 -(	(ai1*ri1)*fpi10*((((gamma-1)*ui1)+(2*ai1))/gamma) 		)
			fni1[2]= (((ai1*ai1)/(gamma-1))+0.5*(ui1*ui1))*ri1*ui1 - (	(ai1*ri1)* fpi10 *(((((gamma-1)*ui1+2*ai1)*((gamma-1)*ui1+2*ai1))/(2*(gamma*gamma-1))))	) 


		#	print "\t 4 fni1[1]= ",fni1[1],
			#print "\t 2 fni1[2]= ",fni1[2]

		elif mi1>1 :
			#	print "mi1>1",
			fni1[0]= 0 
			fni1[1]= 0
			fni1[2]= 0
			#print "\t 2  fni1[2]= ",fni1[2]

		elif mi1<-1 :
			#	print "mi1<-1",
			fni1[0]= mi1* ri1 * ai1
			fni1[1]= ai1* ai1*ri1*(mi1 *mi1 + (1/gamma) ) 
			fni1[2]= ri1* ai1* ai1* ai1 *mi1 *(.5 *mi1 *mi1+ (    1 /(gamma - 1)  ) )
		#	print "\t 3 fni1[1]= ",fni1[1]

		for i in [0,1,2]:
			fi[i] = fpi[i]+fni1[i]
			#print " ",fi[i]," fni1[i]=",fni1[i]," fpi[i]=",fpi[i]

		#print " "," fi[0]=",fi[0]," "," fi[1]=",fi[1]," "," fi[2]=",fi[2]
		return fi 
	def stegerwarming(Ui,Ui1):
		fpi  = numpy.array([0.0,0.0,0.0])
		fni1 = numpy.array([0.0,0.0,0.0])
		fi   = numpy.array([0.0,0.0,0.0])

		ri   =Ui[0]
		ui   =(Ui[1])/ri
		pi   =((Ui[2]-(0.5*ui*ui*ri))*(gamma-1))
		ai   =math.sqrt((gamma*pi)/ri )    
		mi   = ui/ai

		ri1  =Ui1[0]
		ui1  =(Ui1[1])/ri1
		pi1  =((Ui1[2]-(0.5*ui1*ui1*ri1))*(gamma-1))
		ai1  = math.sqrt((gamma*pi1)/ri1 )   
		mi1  = ui1/ai1

		if( (math.fabs(mi) ) < ( 1+ e ) ) :
			fpi[0]=(ri/( 2* gamma))*(	 ( 2*gamma*ui ) +ai -ui 	 ) 
			fpi[1]=(ri/( 2* gamma))*(    2*(gamma -1)*ui*ui + (  (ui+ai)*(ui+ai)   ) 		)
			fpi[2]=(ri/( 2* gamma))*( 	(gamma-1 )*ui*ui*ui+ (ui+ai)*(ui+ai)*(ui+ai)/2.0  +  	( (3 - gamma)*(ui+ai)*ai*ai)/(2*(gamma-1)  )	)
	
		elif mi >1 :
			fpi[0]= mi* ri * ai
			fpi[1]=  ai* ai*ri*(mi*mi+ (1/gamma) ) 
			fpi[2]= ri* ai* ai* ai *mi*(.5 *mi*mi+ (    1 /(gamma - 1)  ) )
		elif mi < -1:
			fpi[0]=0
			fpi[1]= 0 
			fpi[2]= 0

		if( (math.fabs(mi1) ) < (1+ e ) ) :
			fni1[0]=(ri1/( 2* gamma))*( ui1-ai1   ) 
			fni1[1]=(ri1/( 2* gamma))*(      (ui1-ai1)*(ui1-ai1)	) 
			fni1[2]=(ri1/( 2* gamma))*( 	 (ui1-ai1)*(ui1-ai1)*(ui1-ai1)/2.0  +  (   (3 - gamma)*(ui1-ai1)*ai1*ai1)/(2*(gamma-1)  )	)

		if mi1>1 :
			fni1[0]=0 
			fni1[1]= 0
			fni1[2]= 0


		elif mi1<-1 :
			fni1[0]= mi1* ri1 * ai1
			fni1[1]=  ai1* ai1*ri1*(mi1 *mi1 + (1/gamma) ) 
			fni1[2]= ri1* ai1* ai1* ai1 *mi1 *(.5 *mi1 *mi1+ (    1 /(gamma - 1)  ) )

		for i in [0,1,2]:
			fi[i] = fpi[i]+fni1[i]

		return fi
	def ausm(Ui,Ui1):
		fpi  = numpy.array([0.0,0.0,0.0])
		fni1 = numpy.array([0.0,0.0,0.0])
		fi   = numpy.array([0.0,0.0,0.0])
		fc   = numpy.array([0.0,0.0,0.0])
		fc1  = numpy.array([0.0,0.0,0.0])

		ri   =Ui[0]
		ui   =(Ui[1])/ri
		pi   =((Ui[2]-(0.5*ui*ui*ri))*(gamma-1))
		ai   =math.sqrt((gamma*pi)/ri )    
		mi   = ui/ai

		ri1  =Ui1[0]
		ui1  =(Ui1[1])/ri1
		pi1  =((Ui1[2]-(0.5*ui1*ui1*ri1))*(gamma-1))
		ai1  = math.sqrt((gamma*pi1)/ri1 )   
		mi1  = ui1/ai1

		if(math.fabs(mi) < (1.0+ e) ):
			mpi=.25* (mi+1.0)*(mi+1.0)
			mni=  -1.0*.25* (mi-1.0)*(mi-1.0)
			ppi= .5* pi *( 1.0+ mi)
			pni=.5 * pi* ( 1.0-mi)

		else :
			mpi= 0.5* (mi+math.fabs(mi) )
			mni=0.5* (mi-math.fabs(mi) )		
			ppi= 0.5*pi* (mi+math.fabs(mi) )/mi
			pni= 0.5*pi* (mi-math.fabs(mi) )/mi

		fc[0]= (ri * ai )
		fc[1]= ( ri* ui *ai  )
		fc[2]=  (ai * (   (.5 *ri * ui* ui)+   ( (     gamma /(gamma - 1.0) )* math.pi) ) )
	

		if(math.fabs(mi1) < (1.0+ e) ):
			mpi1=.25* (m1i+1.0)*(mi1+1.0)
			mni1=  -1.0*.25* (mi1-1.0)*(mi1-1.0)
			ppi1= .5* pi1 *( 1.0+ mi1)
			#pni1=.5 * pi1* ( 1.0-mi1)

		else :
			mpi1= 0.5* (mi1+math.fabs(mi1) )
			mni1=0.5* (mi1-math.fabs(mi1) )		
			#ppi1= 0.5*pi1* (mi1+math.fabs(mi1) )/mi1
			pni1= 0.5*pi1* (mi1-math.fabs(mi1) )/mi1

		fc1[0]= (ri1 * ai1 )
		fc1[1]= ( ri1* ui1 *ai1  )
		fc1[2]=  (ai1 * (   (.5 *ri1 * ui1* ui1)+   ( (     gamma /(gamma - 1.0) )* math.pi) ) )

		mihalf= mpi+mni1
			
		fi[0]=   ( mihalf*0.5* ( fc[0]+fc1[0]  )  ) - ( .5*  math.fabs(mihalf) *( fc1[0] -fc[0]) )
		fi[1]=   ( mihalf*0.5* ( fc[1]+fc1[1]  )  ) - ( .5*  math.fabs(mihalf) *( fc1[1] -fc[1]) ) +( ppi+ pni1 )
		fi[2]=   ( mihalf*0.5* ( fc[2]+fc1[2]  )  ) - ( .5*  math.fabs(mihalf) *( fc1[2] -fc[2]) )

		return fi

	def mchfnc1plus( m):
		return( ( .5* (m+math.fabs(m)) ))

	def mchfnc1minus( m):
		return( ( .5* (m-math.fabs(m)) ) )

	def mchfnc2plus( m):
		return( ( 0.25* (m+1.0)*(m+1.0) ) )

	def mchfnc2minus( m):
		return( ( -0.25* (m-1.0)*(m-1.0) ) )

	def mchfnc4plus( m):
		if(math.fabs(m) > 1.0-e):
			kc= mchfnc1plus(m) 
		else:
			kc= (mchfnc2plus(m) * (1.0-(16.0*self.beta*mchfnc2minus(m) ) ) )
		return( kc)

	def mchfnc4minus( m):
		if(math.fabs(m) > 1.0-e) :
			kc= mchfnc1minus(m) 
		else :
			kc= (mchfnc2minus(m) * (1.0+(16.0*self.beta*mchfnc2plus(m) ) ) )
		return( kc)


	def prsfnc5plus(  m):
		if (m> 1.0-e) :
			kc= 0.5* (m+math.fabs(m) )/m
		else:
			kc=  mchfnc2plus(m) *( (2.0-m)- 16.0* self.alpha* m* mchfnc2minus(m) )
		return (kc)
	
	def prsfnc5minus( m):
		if (m> 1.0-e) :
			kc= 0.5* (m-math.fabs(m) )/m
		else:
			kc=  mchfnc2minus(m) *( (-2.0-m)+ 16.0* self.alpha* m* mchfnc2plus(m) )
		return kc


	def ausmplus(Ui,Ui1):

		fpi  = numpy.array([0.0,0.0,0.0])
		fni1 = numpy.array([0.0,0.0,0.0])
		fi   = numpy.array([0.0,0.0,0.0])
		#gamma=1.4

		ri   =Ui[0]
		ui   =(Ui[1])/ri
		pi   =((Ui[2]-(0.5*ui*ui*ri))*(gamma-1))
		ai   =math.sqrt((gamma*pi)/ri )
		mi   = ui/ai

		ri1  =Ui1[0]
		ui1  =(Ui1[1])/ri1
		pi1  =((Ui1[2]-(0.5*ui1*ui1*ri1))*(gamma-1))
		ai1  = math.sqrt((gamma*pi1)/ri1 )   
		mi1  = ui1/ai1

		#if ahalfcond == 'mean':
		#	ahalfi= (ai+ai1)/2.0
		#else:
		astari  = 2*(gamma-1) * ( ( .5*ui*ui ) + gamma*pi/ ( (gamma-1)*ri ) ) /(gamma+1)
		acapi   = astari*astari/ ( max( astari, (math.fabs(ui) )))

		astari1 = 2*(gamma-1) * ( ( .5*ui1*ui1 ) + gamma*pi1/ ( (gamma-1)*ri1 ) ) /(gamma+1)
		acapi1  = astari1*astari1/ ( max( astari1, (math.fabs(ui1) )))

		ahalfi= min( acapi,acapi1 )

		mchli= ui/ahalfi
		mchri=ui1/ahalfi

		mhalfi=( mchfnc4plus(mchli)  ) +   (mchfnc4minus(mchri) )
		mchphalfi= .5* (mhalfi+math.fabs(mhalfi) )
		mchnhalfi= .5* (mhalfi-math.fabs(mhalfi) )

		phalfi= ( prsfnc5plus(mchli) *pi   )+ ( prsfnc5minus(mchri) *pi1 )
	
		#ahalfi= (ai+ai1)/2.0		 #Up

		fi[0]=  ahalfi*( mchphalfi*ri+ mchnhalfi*ri1 )
		fi[1]=  ahalfi*( mchphalfi*ri*ui+ mchnhalfi*ri1*ui1 )+phalfi
		fi[2]=  ahalfi*(  ( mchphalfi*( (gamma*pi/(gamma-1)  )+ (.5*ri*ui*ui )  )  )+  ( mchnhalfi*( (gamma*pi1/(gamma-1)  )+ (.5*ri1*ui1 *ui1 )  ) )  )

		return fi

	def AUSMup(Ui,Ui1):
		fi   = numpy.array([0,0,0])

		ri   =Ui[0]
		ui   =(Ui[1])/ri
		pi   =((Ui[2]-(0.5*ui*ui*ri))*(gamma-1))
		ai   =math.sqrt((gamma*pi)/ri )    
		mi   = ui/ai

		ri1  =Ui1[0]
		ui1  =(Ui1[1])/ri1
		pi1  =((Ui1[2]-(0.5*ui1*ui1*ri1))*(gamma-1))
		ai1  = math.sqrt((gamma*pi1)/ri1 )   
		mi1  = ui1/ai1

		astari= 2*(gamma-1) * ( ( .5*ui*ui ) + gamma*pi/ ( (gamma-1)*ri ) ) /(gamma+1)
		astari1= 2*(gamma-1) * ( ( .5*ui1*ui1 ) + gamma*pi1/ ( (gamma-1)*ri1 ) ) /(gamma+1)

		acapi= astari*astari/ ( max( astari, (math.fabs(ui) )))
		acapi1= astari1*astari1/ ( max( astari1, (math.fabs(ui1) )))

		ahalfi= min( acapi,acapi1 )
	
		mchli= ui/ahalfi
		mchri=ui1/ahalfi
		#self.minfsq=0
		mbarsqi= (  (ui*ui +ui1*ui1 )/ (2*ahalfi*ahalfi) )
		mnotsqi= min( 1, (max( mbarsqi,self.minfsq) ) )

		if( (math.fabs(math.sqrt(mnotsqi)) ) > .105572809) :
			fami= math.fabs(math.sqrt(mnotsqi)) * (2.0- ( math.fabs(math.sqrt(mnotsqi) )  ) )
		else :
			fami= .4

		fapi= (math.fabs( math.sqrt(  ( 4.0+ (16.0*self.alpha/3.0) )  )  ) )/5.0 
		mhalfi=( mchfnc4plus(mchli)  ) +   (mchfnc4minus(mchri) ) -( ( self.kp* (max( (1.0- (self.sigma*mnotsqi) ),0)   ) *(pi1-pi) *2 )/ (fami *ahalfi*ahalfi* (ri+ri1) ) ) 

		if(mhalfi>0):
			massdoti= ahalfi* mhalfi* ri
		else:
			massdoti=ahalfi* mhalfi* ri1

		phalfi= ( prsfnc5plus(mchli) *pi   )+ ( prsfnc5minus(mchri) *pi1 )- ( self.ku*prsfnc5plus(mchli)*prsfnc5minus(mchri)*(ri+ri1) * fapi* (ui1-ui) *ahalfi )

		if massdoti>=0 :
			fi[0]=   ( massdoti)
			fi[1]=   ( massdoti* ui)+ phalfi
			fi[2]=   ( massdoti*( ( .5*ui*ui ) + gamma*pi/ ( (gamma-1)*ri ) )  )
		else:
			fi[0]=   ( massdoti)
			fi[1]=   ( massdoti* ui1)+ phalfi
			fi[2]=   ( massdoti*( ( .5*ui1*ui1 ) + gamma*pi1/ ( (gamma-1)*ri1 ) )  )
		return fi

	def HLL(Ui,Ui1):
		fpi  = numpy.array([0.0,0.0,0.0])
		fni1 = numpy.array([0.0,0.0,0.0])
		fi   = numpy.array([0.0,0.0,0.0])

		ri   =Ui[0]
		ui   =(Ui[1])/ri
		pi   =((Ui[2]-(0.5*ui*ui*ri))*(gamma-1))
		ai   =math.sqrt((gamma*pi)/ri )    
		mi   = ui/ai

		ri1  =Ui1[0]
		ui1  =(Ui1[1])/ri1
		pi1  =((Ui1[2]-(0.5*ui1*ui1*ri1))*(gamma-1))
		ai1  = math.sqrt((gamma*pi1)/ri1 )   
		mi1  = ui1/ai1

		sl= min(ui-ai,ui1-ai1)
		sr= max(ui+ai,ui1+ai1)

		if sl >= 0 :
			fi[0]= mi* ri * ai
			fi[1]=  ai* ai*ri*(mi*mi+ (1/gamma) )
			fi[2]= ri* ai* ai* ai *mi*(.5 *mi*mi+ (    1 /(gamma - 1)  ) )

		elif sl<0 and sr>0 :
			fpi[0]= mi* ri * ai
			fpi[1]=  ai* ai*ri*(mi*mi+ (1/gamma) )
			fpi[2]= ri* ai* ai* ai *mi*(.5 *mi*mi+ (    1 /(gamma - 1)  ) )

			fni1[0]= mi1* ri1 * ai1
			fni1[1]=  ai1* ai1*ri1*(mi1 *mi1 + (1/gamma) )
			fni1[2]= ri1* ai1* ai1* ai1 *mi1 *(.5 *mi1 *mi1+ (    1 /(gamma - 1)  ) )

			fi[0] =  (    sr*fpi[0]-sl*fni1[0]+ sl*sr*(  Ui1[0]-Ui[0]  )        )/(     sr-sl    )
			fi[1] =  (    sr*fpi[1]-sl*fni1[1]+ sl*sr*(  Ui1[1]-Ui[1]  )        )/(     sr-sl    )
			fi[2] =  (    sr*fpi[2]-sl*fni1[2]+ sl*sr*(  Ui1[2]-Ui[2]  )        )/(     sr-sl    )

		elif sr<=0 :
			fi[0]= mi1* ri1 * ai1
			fi[1]=  ai1* ai1*ri1*(mi1 *mi1 + (1/gamma) )
			fi[2]= ri1* ai1* ai1* ai1 *mi1 *(.5 *mi1 *mi1+ (    1 /(gamma - 1)  ) )

		return fi
	def HLLC(Ui,Ui1):
		fpi  = numpy.array([0.0,0.0,0.0])
		fni1 = numpy.array([0.0,0.0,0.0])
		fi   = numpy.array([0.0,0.0,0.0])

		ri   =Ui[0]
		ui   =(Ui[1])/ri
		pi   =((Ui[2]-(0.5*ui*ui*ri))*(gamma-1))
		ai   =math.sqrt((gamma*pi)/ri )    
		mi   = ui/ai

		ei= Ui[2]

		ri1  =Ui1[0]
		ui1  =(Ui1[1])/ri1
		pi1  =((Ui1[2]-(0.5*ui1*ui1*ri1))*(gamma-1))
		ai1  = math.sqrt((gamma*pi1)/ri1 )   
		mi1  = ui1/ai1

		ei1=Ui1[1]
		
		hi=(ei+pi)/ri
		hi1=(ei1+pi1)/ri1
	
		ai = sqrt(1.4*pi/ri)
		ai1=sqrt(1.4*pi1/ri1)
		
		#Step 1: Calculate the roe avei1ages
		
		r = sqrt(ri/ri1)

		uroe = (ui + r * ui1)/(1+r)
		hroe = (hi + r * hi1)/(1+r)	
		aroe = sqrt(0.4 * (hroe - 0.5 * (uroe * uroe )))
		
		
		temp1 = ui - ai
		temp2 = uroe - aroe
		
		if(temp1<temp2):
			sl = temp1
		else:
			sl = temp2

		temp1 = ui1 + ai1
		temp2 = uroe + aroe
	
		ur=ui1
		pr=pi1
		
		if(temp1>temp2):
			sr = temp1
		else:
			sr = temp2

		sm = (pi1 - pi + ri * ui * (sl - ui) - ri1 * ui1 * (sr - ui1) ) / (ri * (sl - ui) - ri1 * (sr - ui1))

		if(sl>=0):
			fi[0] = ri * ul
			fi[1] = ri * ul * ul + pl
			fi[2] = (el + pl) * ul
	
		if(sl<0 and sm>0):
			temp = ri * (sl - ul)/(sl - sm)
			u1hllc = temp
			u2hllc = temp * sm
			u3hllc = temp * (el/ri + (sm - ul) * (sm + pl / (ri * (sl - ul))))

			fi[0] = ri * ul + sl * (u1hllc - ri)
			fi[1] = ri * ul * ul + pl + sl * (u2hllc - ri * ul)
			fi[2] = (el + pl) * ul + sl * (u3hllc - el)

		if(sr>0 and sm<=0):
			temp = ri1 * (sr - ur)/(sr - sm)
			u1hllc = temp
			u2hllc = temp * sm
			u3hllc = temp * (ei1/ri1 + (sm - ur) * (sm + pr / (ri1 * (sr - ur))))
			
			fi[0] = ri1 * ur + sr * (u1hllc - ri1)
			fi[1] = ri1 * ur * ur + pr + sr * (u2hllc - ri1 * ur)
			fi[2] = (ei1 + pr) * ur + sr * (u3hllc - ei1)
		
		if(sr<=0):
			fi[0] = ri1 * ui1
			fi[1] = ri1 * ui1 * ui1 + pi1
			fi[2] = (ei1 + pi1) * ui1
		return fi

