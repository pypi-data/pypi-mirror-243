from AHU.air_humide import air_humide
from AHU.air_humide import air_humide_NB
from AHU.AirPort.AirPort import AirPort



        

class Object:
    def __init__(self):
        
        self.Inlet=AirPort() 
        self.Outlet=AirPort()
        self.id=1
        self.T=5
        self.RH = 60
        self.F = 10000
        self.Pv_sat=0
        self.w=0
        self.T_hum=0
        self.h=0
        self.P=101325
        self.F_m3h=0 #Débit volumique "m3/h air humide
        self.F_dry=0
        
    def calculate(self):
        
        self.F = self.F_m3h * air_humide.func_rho_hum(self.T, self.RH, self.P)/3600 #kg/s
        # self.F = self.F/3600 #m3/s
        #Connecteur Inlet
        self.P=self.Inlet.P
                 
        self.Pv_sat=air_humide.func_Pv_sat(self.T)
       # print("Pvsat=",self.Pv_sat)
        self.w=air_humide.HA(self.Pv_sat,self.RH,self.P)
       # print("HA=",self.w)
        self.T_hum=air_humide.Tw(self.T,self.RH)
      #  print("self.T_hum=",self.T_hum)
        self.h=air_humide.Enthalpie(self.T, self.w)
      #  print("self.h=",self.h)
        self.F_dry=(self.F)/(1+(self.w/1000))
      
      #connecteur   
      
        self.Inlet.w=self.w
        #self.Inlet.P=
        self.Inlet.h=self.h
        self.Inlet.F=self.F
        
        self.Outlet.w=self.Inlet.w
        self.Outlet.P=self.Inlet.P
        self.Outlet.h=self.Inlet.h
        self.Outlet.F=self.Inlet.F
        self.T_outlet=air_humide_NB.Air3_Tdb(self.Outlet.w/1000,self.Outlet.P,self.Outlet.h)
        
    
    
    



