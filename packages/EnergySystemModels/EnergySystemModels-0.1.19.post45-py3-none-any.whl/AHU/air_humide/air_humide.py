from math import*
def func_Pv_sat(T_db) :

#calcul de la pression de vapeur sat
# référence : 2013 ASHRAE Handbook—Fundamentals (SI) - CHAPTER 1 - PSYCHROMETRICS - Equations (5) and (6) - Hyland and Wexler 1983 equations
# Pv_sat = saturation pressure, Pa
# Tk = absolute temperature, K = °C + 273.15


	C1 = -5.6745359 * 10 ** 3
	C2 = 6.3925247 * 10 ** 0
	C3 = -9.677843 * 10 ** (-3)
	C4 = 6.2215701 * 10 ** (-7)
	C5 = 2.0747825 * 10 ** (-9)
	C6 = -9.484024 * 10 ** (-13)
	C7 = 4.1635019 * 10 ** (0)
	C8 = -5.8002206 * 10 ** (3)
	C9 = 1.3914993 * 10 ** (0)
	C10 = -4.8640239 * 10 ** (-2)
	C11 = 4.1764768 * 10 ** (-5)
	C12 = -1.4452093 * 10 ** (-8)
	C13 = 6.5459673 * 10 ** (0)

	Tk = T_db + 273.15

	if T_db < 0 : #valable entre -100 et 0 °C

		Pv_sat = exp(C1 / Tk + C2 + C3 * Tk + C4 * Tk ** 2 + C5 * Tk ** 3 + C6 * Tk ** 4 + C7 * log(Tk))
	else :  #valable entre 0 et 200 °C

		Pv_sat = exp(C8 / Tk + C9 + C10 * Tk + C11 * Tk ** 2 + C12 * Tk ** 3 + C13 * log(Tk))




	return Pv_sat

def func_RH(w, P=101325.0, Pv_sat=None, T_db=None):
    if Pv_sat is None:
        if T_db is None:
            raise ValueError("Either Pv_sat or T_db must be provided")
        else:
            Pv_sat = func_Pv_sat(T_db)

    Pv = P * (w / 1000) / ((w / 1000) + 0.62198)
    RH = (Pv / Pv_sat) * 100
    return RH


def func_w( RH=None, P=101325.0,Pv_sat=None,T_db=None,h=None):
	if Pv_sat is None:
		if T_db is None:
			raise ValueError("Either Pv_sat or T_db must be provided")
		else:
			Pv_sat = func_Pv_sat(T_db)
	
	if RH is not None:
		Pv = Pv_sat * (RH / 100)
		if Pv<P:
			w = 0.62198 * Pv / (P - Pv) * 1000
		else:
			w =None
	if h is not None:
		w   = ((h-1.006 * T_db)/(2501 + 1.0805 * T_db))*1000

	return w



def func_h(T_db, w):
	Enthalpie = 1.006 * T_db + (w / 1000) * (2501 + 1.0805 * T_db)
	return Enthalpie

def func_rho_hum(T_db, RH, P=101325):

	Tk = T_db + 273.15


	Rv = 461
	Ra = 287.66
	Psat = func_Pv_sat(T_db)


	Pv = Psat * (RH / 100)
	rho_v = Pv / (Rv * Tk)
	rho_a = (P - Pv) / (Ra * Tk)

	Rah = Ra / (1 - ((RH / 100) * Psat / P) * (1 - Ra / Rv))

	rho_hum = (rho_a * Ra + rho_v * Rv) / Rah

	return rho_hum






from scipy.optimize import fsolve
from math import exp, log

def func_T_db(RH=None, w=None, h=None, Pv_sat=None, P=101325):
    if RH is not None and w is not None:
        # Calcul de T_db à partir de RH et w
        def equations(T_db):
            Pv_sat_calculated = func_Pv_sat(T_db)
            Pv = P * (w / 1000) / (0.62198 + w / 1000)
            return Pv_sat_calculated * RH / 100 - Pv

        T_db_initial_guess = 20.0
        T_db_solution = fsolve(equations, T_db_initial_guess)
        return T_db_solution[0]

    elif h is not None and w is not None:
        # Calcul de T_db à partir de h et w
        return (h - (w / 1000) * 2501) / (1.006 + (w / 1000) * 1.0805)

    elif Pv_sat is not None:
        # Calcul de T_db à partir de Pv_sat
        def inverse_Pv_sat(T_db):
            return func_Pv_sat(T_db) - Pv_sat

        T_db_initial_guess = 20.0
        T_db_solution = fsolve(inverse_Pv_sat, T_db_initial_guess)
        return T_db_solution[0]

    else:
        raise ValueError("Insufficient parameters provided for T_db calculation")

   


def Tw(Td, HR) :   #calcul de la temp du bulbe humide
	Tw = Td * atan(0.151977 * (HR + 8.313659) ** (1 / 2)) + atan(Td + HR) - atan(HR - 1.676331) + 0.00391838 * (HR) ** (3 / 2) * atan(0.023101 * HR) - 4.686035
#Tw = 20 * atan(0.151977 * (50 + 8.313659) ** (1 / 2)) + atan(20 + 50) - atan(50 - 1.676331) + 0.00391838 * (50) ** (3 / 2) * atan(0.023101 * 50) - 4.686035
	return Tw


#Wet-Bulb Temperature from Relative Humidity and Air Temperature
#ROLAND STULL
#University of British Columbia, Vancouver, British Columbia, Canada
#(Manuscript received 14 July 2011, in final form 28 August 2011)


def HA(Pv_sat, HR, P):



	Pv = Pv_sat * (HR / 100)
	HA = 0.62198 * Pv / (P - Pv) * 1000


	return HA


def HR(Pv_sat, HA, P=101325.0):
	Pv = P * (HA / 1000) / ((HA / 1000) + 0.62198)
	HR = (Pv / Pv_sat) * 100
	return HR


def T_sat(w_target):

	T = -100
	Erreur = HA(func_Pv_sat(T), 100) - w_target


	while Erreur <= 0 :
		T = T + 0.02
		Erreur = HA(func_Pv_sat(T), 100) - w_target



	T_sat = T

	return T_sat



def T_Humidifier(w_target, HA_init, Tinit):

	T = -100
	Erreur = -Enthalpie(Tinit, HA_init) + Enthalpie(T, w_target)

	while Erreur < 0 :
		T = T + 0.01
		Erreur = -Enthalpie(Tinit, HA_init) + Enthalpie(T, w_target)
 


	T_Humidifier = T - 0.01

	return T_Humidifier




def T_rosee(Pv):
	T = -100
	Erreur = -Pv + func_Pv_sat(T)

	while Erreur < 0 :
		T = T + 0.01
		Erreur = -Pv + func_Pv_sat(T)
  


	T_rosee = T - 0.01

	return T_rosee










def Enthalpie(T, HA):
	Enthalpie = 1.006 * T + (HA / 1000) * (2501 + 1.0805 * T)
	return Enthalpie
    
def Temperature(Enthalpie, HA):
	T=(Enthalpie-(HA / 1000) *2501)/(1.006+ (HA / 1000) *1.0805)
    
	return T

def T_Enthalpie_Ha(Enthalpie, HA):

	T_Enthalpie_Ha = (Enthalpie - (HA / 1000) * 2501) / (1.006 + (HA / 1000) * 1.0805)

	return T_Enthalpie_Ha



#def Temperature_Melange(m1, T1, HR1, m2, T2, HR2)

#Temperature_Melange = T_Enthalpie_Ha((Enthalpie(T1, (HA(func_Pv_sat(T1), HR1))) * (m1 / (1 + (HA(func_Pv_sat(T1), HR1)) / 1000)) + (Enthalpie(T2, (HA(func_Pv_sat(T2), HR2)))) * (m2 / (1 + (HA(func_Pv_sat(T2), HR2)) / 1000))) / ((m2 / (1 + (HA(func_Pv_sat(T2), HR2)) / 1000)) + (m1 / (1 + (HA(func_Pv_sat(T1), HR1)) / 1000))), 1000 * (((m2 / (1 + (HA(func_Pv_sat(T2), HR2)) / 1000)) * ((HA(func_Pv_sat(T2), HR2)) / 1000)) + ((m1 / (1 + (HA(func_Pv_sat(T1), HR1)) / 1000)) * ((HA(func_Pv_sat(T1), HR1)) / 1000))) / ((m2 / (1 + (HA(func_Pv_sat(T2), HR2)) / 1000)) + (m1 / (1 + (HA(func_Pv_sat(T1), HR1)) / 1000))))
#return
#def HA_Melange(m1, T1, HR1, m2, T2, HR2)

#HA_Melange = 1000 * (((m2 / (1 + (HA(func_Pv_sat(T2), HR2)) / 1000)) * ((HA(func_Pv_sat(T2), HR2)) / 1000)) + ((m1 / (1 + (HA(func_Pv_sat(T1), HR1)) / 1000)) * ((HA(func_Pv_sat(T1), HR1)) / 1000))) / ((m2 / (1 + (HA(func_Pv_sat(T2), HR2)) / 1000)) + (m1 / (1 + (HA(func_Pv_sat(T1), HR1)) / 1000)))
#return


#ρ_hum

def rho_ah(T, HR, P):

	Tk = T + 273.15


	Rv = 461
	Ra = 287.66
	Psat = func_Pv_sat(T)


	Pv = Psat * (HR / 100)
	rho_v = Pv / (Rv * Tk)
	rho_a = (P - Pv) / (Ra * Tk)

	Rah = Ra / (1 - ((HR / 100) * Psat / P) * (1 - Ra / Rv))

	rho_ah = (rho_a * Ra + rho_v * Rv) / Rah

	return rho_ah


