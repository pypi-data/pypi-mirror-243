from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
from CoolProp.CoolProp import PropsSI
import pandas as pd 
from datetime import datetime

import math

class Object:
    def __init__(self):
        self.Timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
        self.Inlet1 = FluidPort(fluid='Dodecane', F=15/3.6, T=120 + 273.15,P=101325)
        self.Outlet1 = FluidPort(fluid='Dodecane',F=15/3.6, T=60 + 273.15,P=101325)
        self.Inlet2 = FluidPort(fluid='water', T=20 + 273.15,P=101325)
        self.Outlet2 = FluidPort(fluid='water',T=30 + 273.15,P=101325)

        self.T1o=None
        self.T2o=None
        self.C1=None
        self.C2=None
        self.R=None # Le rapport des débits de capacités des deux fluides est 
        self.Eff=None # efficacité


        self.P_drop=0
   
     
        self.df = pd.DataFrame()


        
    def calculate (self):
    
        self.Outlet1.P=self.Inlet1.P-self.P_drop
        self.Outlet1.F=self.Inlet1.F
        self.Outlet1.fluid=self.Inlet1.fluid
        self.Outlet2.fluid=self.Inlet2.fluid

        #self.Outlet1.calculate_properties()

        self.Qth=self.Inlet1.F*(self.Outlet1.h-self.Inlet1.h)

        print( 'self.Inlet2.F', self.Inlet2.F)
        if self.Inlet2.F is None or self.Inlet2.F==0 :
            self.Inlet2.F=abs(self.Qth/(self.Outlet2.h-self.Inlet2.h))
            self.Outlet2.F=self.Inlet2.F

        

       

        self.Inlet1.calculate_properties()
        self.Inlet2.calculate_properties()
        self.Outlet1.calculate_properties()
        self.Outlet2.calculate_properties()

        self.C1=self.Inlet1.F*self.Inlet1.cp
        self.C2=self.Inlet2.F*self.Inlet2.cp
        self.R=self.C1/self.C2
        if self.R<1:
            self.Eff=(self.Inlet1.T-self.Outlet1.T)/(self.Inlet1.T-self.Inlet2.T)

        print((self.Inlet1.T-self.Outlet2.T),(self.Outlet1.T-self.Inlet2.T))

        self.DTLM=((self.Inlet1.T-self.Outlet2.T)-(self.Outlet1.T-self.Inlet2.T))/math.log((self.Inlet1.T-self.Outlet2.T)/(self.Outlet1.T-self.Inlet2.T))
        self.UA=abs(self.Qth/self.DTLM)

        self.df = pd.DataFrame({'DTLM_HEX': [self.Timestamp,self.Qth], },
                      index = ['Timestamp',self.Qth])     


# from ThermodynamicCycles.Source import Source
# from ThermodynamicCycles.Connect import Fluid_connect

# SOURCE1=Source.Object()
# SOURCE1.F_m3h=15
# SOURCE1.Pi_bar=1
# SOURCE1.fluid='Dodecane'
# SOURCE1.Ti_degC=120
# SOURCE1.calculate()

# SOURCE2=Source.Object()
# SOURCE2.Pi_bar=1
# SOURCE2.fluid='water'
# SOURCE2.Ti_degC=20
# SOURCE2.calculate()

# HEX=Object()
# HEX.T1o=60
# HEX.T2o=30
# Fluid_connect(HEX.Inlet1,SOURCE1.Outlet)
# Fluid_connect(HEX.Inlet2,SOURCE2.Outlet)
# HEX.calculate()
# print("-------------------------------",HEX.df)

# print(HEX.Outlet1.df)
# print(HEX.Outlet2.df)

# print(HEX.R)
# print(HEX.Eff)
# print(HEX.UA)