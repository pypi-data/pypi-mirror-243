from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
from CoolProp.CoolProp import PropsSI
import pandas as pd 
from datetime import datetime

class Object:
    def __init__(self):
        self.Timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.Inlet1=FluidPort() 
        self.Outlet1=FluidPort()
        self.Inlet2=FluidPort() 
        self.Outlet2=FluidPort()

        self.P_drop=0
        self.Qth=None
     
        self.df = pd.DataFrame()

        self.Inlet1.F=15/3.6
        self.Inlet1.fluid="Dodecane"
        self.Inlet1.T=120+273.15
        self.Outlet1.T=60+273.15

        self.Inlet2.fluid="water"
        self.Inlet2.T=20+273.15
        self.Outlet2.T=30+273.15
        
    def calculate (self):
    
        self.Outlet1.P=self.Inlet1.P-self.P_drop
        self.Outlet1.F=self.Inlet1.F
        self.Outlet1.fluid=self.Inlet1.fluid

        #self.Outlet1.calculate_properties()

        self.Qth=self.Inlet1.F*(self.Outlet1.h-self.Inlet1.h)

        self.df = pd.DataFrame({'HEX_T_target': [self.Timestamp,self.Qth], },
                      index = ['Timestamp',self.Qth])     

     
HEX=Object()
HEX.calculate()
print(HEX.df)