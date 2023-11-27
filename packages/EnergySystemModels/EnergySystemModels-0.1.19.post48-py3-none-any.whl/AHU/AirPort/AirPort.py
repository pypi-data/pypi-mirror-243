from AHU.air_humide import air_humide



class AirPort:
    def __init__(self):
        self.F=0 # d'air d'air
        self.P = 101325 # pression
        self.h = 10000 # enthalpie spéc
        self.w = 0 # Humidité absolue
        
    def propriete(self):
        self.result="HR,Pv_sat,T="
        self.T=air_humide.Temperature(self.h, self.w)
        self.Pv_sat=air_humide.func_Pv_sat(self.T)
        self.RH=air_humide.HR(self.Pv_sat, self.w, self.P)
        return self.result,self.RH,self.Pv_sat,self.T
    

