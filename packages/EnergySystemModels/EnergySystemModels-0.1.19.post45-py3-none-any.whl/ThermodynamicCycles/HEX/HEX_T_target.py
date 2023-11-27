from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
from CoolProp.CoolProp import PropsSI
import pandas as pd 
from datetime import datetime

class Object:
    def __init__(self):
        self.Timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #self.IsenEff=0.7
        self.Inlet=FluidPort() 
        self.F=0.1
        self.Inlet.F=self.F
        self.Outlet=FluidPort()
       # self.Sis=0
        self.To=None
        self.Ti_degC=None
        #self.His=0
        #self.LP=1*100000
        self.Ho=0
        self.T_target=0
        self.P_drop=0
        self.So=0
        # self.Tdischarge_target=80
        # self.T3ref2=0
        
        self.Qhex=0
        # self.Qlosses=0
        self.df = pd.DataFrame()
 
        
    def calculate (self):
        self.F=self.Inlet.F
        self.Outlet.P=self.Inlet.P-self.P_drop

        ##entrée :
        try:
            self.Ti_degC=PropsSI("T", "P", self.Inlet.P, "H", self.Inlet.h,self.Inlet.fluid)-273.15
        except:
            self.Ti_degC=0-273.15
        
        #conditions de Outlet
        self.To=self.T_target+273.15
        self.Ho = PropsSI('H','P',self.Outlet.P,'T',self.To,self.Inlet.fluid)
        self.So = PropsSI('S','P',self.Outlet.P,'H',self.Ho,self.Inlet.fluid)
        
        self.Outlet.h=self.Ho
        self.Outlet.F=self.F
        self.Outlet.fluid=self.Inlet.fluid
        
        self.Qhex=self.Inlet.F*(self.Ho-self.Inlet.h)

        self.df = pd.DataFrame({'HEX_T_target': [self.Timestamp,self.T_target,self.Qhex/1000,], },
                      index = ['Timestamp','hex_T_target(°C)','hex_Qhex(kW)'])     