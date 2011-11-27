import math 
import numpy
class tests(object):
	def test(self,Ui,Ui1):
		gamma= 1.4
		de=0.000001
		fpi  = numpy.array([0.0,0.0,0.0])
		fni1 = numpy.array([0.0,0.0,0.0])
		fi   = numpy.array([0.0,0.0,0.0])

		# Parameters of left state
		ri   =Ui[0]
		ui   =(Ui[1])/ri
		pi   =((Ui[2]-(0.5*ui*ui*ri))*(gamma-1))
		ai   =math.sqrt((gamma*pi)/ri )    
		mi   = ui/ai

		# Parameters of right state
		ri1  =Ui1[0]
		ui1  =(Ui1[1])/ri1
		pi1  =((Ui1[2]-(0.5*ui1*ui1*ri1))*(gamma-1))
		ai1  = math.sqrt((gamma*pi1)/ri1 )   
		mi1  = ui1/ai1
		# The Following is the flux splitting of Steger Warming

		if( (math.fabs(mi) ) < ( 1+ de ) ) :
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

		if( (math.fabs(mi1) ) < (1+ de ) ) :
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

		#Net Flux 
		for i in [0,1,2]:
			fi[i] = fpi[i]+fni1[i]

		return fi
