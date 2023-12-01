from AHU.air_humide import air_humide
from AHU.air_humide import air_humide_NB

from AHU.AirPort.AirPort import AirPort

class Object:
    def __init__(self):
        self.Inlet=AirPort() 
        self.Outlet=AirPort()
        self.P=0
        self.P_drop=0
        self.id=2
        # données air neuf
        self.T_in=0
        self.h_in=0
        self.w_in=12
        self.F=0
        self.F_dry=0
        
        #consigne
        self.T_out_target=20
        # calcul Outlet Coil
        self.h_out=0
        self.Q_th=12
        self.RH_out=0
       
        
    def calculate(self):
        
          #connecteur  
        self.Outlet.P=self.Inlet.P-self.P_drop
      
        self.w_in=self.Inlet.w
        self.P=self.Inlet.P
        self.h_in=self.Inlet.h
        self.F=self.Inlet.F
        # print("cond self.F",self.F)
        self.T_in=air_humide_NB.Air3_Tdb(self.w_in/1000,self.Inlet.P,self.h_in)
        self.F_dry=(self.F)/(1+self.w_in/1000) #[kg air sec/s]
        ''' Témpérature fluide entré Coil < Température consigne -> Rechauffement sensible'''
        if self.T_out_target>self.T_in:
            
            self.h_out=air_humide.Enthalpie(self.T_out_target,self.w_in)
            # self.h_out=air_humide_NB.Air2_Hs(self.T_out_target, air_humide_NB.Air4_RH(self.T_out_target,self.Outlet.P, self.w_in/1000), self.Outlet.P) 
          #  print("h_out=",self.h_out)
            self.F_dry=(self.F)/(1+self.w_in/1000) # [kg air sec/s]
           # print("self.F_dry=",self.F_dry,"self.Inlet.P=",self.Inlet.P,"self.F=",self.F)
            self.Q_th=(self.h_out-self.h_in)*self.F_dry
           # print("self.Q_th=",self.Q_th)
            self.RH_out=air_humide.HR(air_humide.func_Pv_sat(self.T_out_target),self.w_in,self.Outlet.P) #parametrer la pression
           # print("self.RH_out=",self.RH_out)
        
            ''' Température fluide entrée Coil > température de consigne -> Aucune action'''    
        else:
            self.h_out=self.h_in
            self.Q_th=0
 
              
       
        #connecteur   
      
          
        self.Outlet.w=self.Inlet.w
        
        self.Outlet.h=self.h_out
        
        self.Outlet.F=self.F_dry*(1+self.Outlet.w/1000)  #[kg air sec/s] * [m3/kg air sec] =[m3/s]
#
        # print(self.Outlet.w/1000, self.Outlet.P, self.Outlet.h)       
        # self.Twb_out=air_humide_NB.Air3_Twb(self.Outlet.w/1000, self.Outlet.P, self.Outlet.h)


