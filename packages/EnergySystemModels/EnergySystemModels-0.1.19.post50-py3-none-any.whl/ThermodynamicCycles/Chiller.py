# =============================================================================
# Chiller Model (Evaporator + Compressor + Desuperheater + Condenser + Expansion_Valve)
# =============================================================================

import CoolProp.CoolProp as CP
from ThermodynamicCycles.Evaporator import Evaporator
from ThermodynamicCycles.Compressor import Compressor
from ThermodynamicCycles.Desuperheater import Desuperheater
from ThermodynamicCycles.Expansion_Valve import Expansion_Valve
from ThermodynamicCycles.Condenser import Condenser
from ThermodynamicCycles.Connect import Fluid_connect

from ThermodynamicCycles import Temperature_Entropy_Chart

class Object:
    def __init__(self, fluid='R134a', evap_params=None, comp_params=None, cond_params=None):
        # Initialize chiller components
        self.EVAP = Evaporator.Object()
        self.COMP = Compressor.Object()
        self.DESURCH = Desuperheater.Object()
        self.COND = Condenser.Object()
        self.DET = Expansion_Valve.Object()

        # Set fluid for all components
        self.fluid = fluid
        self.EVAP.fluid = self.fluid
        self.COMP.fluid = self.fluid
        self.DESURCH.fluid = self.fluid
        self.COND.fluid = self.fluid
        self.DET.fluid = self.fluid

        # Set parameters for each component
        self.set_evaporator_parameters(evap_params)
        self.set_compressor_parameters(comp_params)
        self.set_condenser_parameters(cond_params)

    def set_evaporator_parameters(self, params):
        if params:
            self.EVAP.Ti_degC= params.get('Ti_degC', 5)
            self.EVAP.surchauff = params.get('surchauff', 2)
            self.EVAP.Inlet.F = params.get('F', 1)
            

    def set_compressor_parameters(self, params):
        if params:
            self.COMP.Tcond_degC = params.get('Tcond_degC', 40)
            self.COMP.eta_is = params.get('eta_is', 0.8)
            self.COMP.Tdischarge_target = params.get('Tdischarge_target', 80)
            if 'Qcomp' in params:
                self.COMP.Qcomp = params['Qcomp']

    def set_condenser_parameters(self, params):
        if params:
            self.COND.subcooling = params.get('subcooling', 2)

    def calculate_cycle(self):
        # Calculation algorithm
        self.EVAP.Inlet.h = CP.PropsSI('H', 'P', 1 * 1e5, 'T', 40 + 273.15, self.fluid)
        self.EVAP.calculate() 
        Fluid_connect(self.COMP.Inlet, self.EVAP.Outlet)
        self.COMP.calculate()
        Fluid_connect(self.DESURCH.Inlet, self.COMP.Outlet)
        self.DESURCH.calculate()
        Fluid_connect(self.COND.Inlet, self.DESURCH.Outlet)
        self.COND.calculate()
        Fluid_connect(self.DET.Inlet, self.COND.Outlet)
        Fluid_connect(self.DET.Outlet, self.EVAP.Inlet)
        self.DET.calculate()
        Fluid_connect(self.EVAP.Inlet, self.DET.Outlet)
        self.EVAP.calculate() # Recalculate evaporator
      

    def calculate_performance(self):
        # Cycle performance
        EER = self.EVAP.Qevap / self.COMP.Qcomp
        QcondTot = self.COND.Qcond + self.DESURCH.Qdesurch
        COP = QcondTot / self.COMP.Qcomp
        return EER, QcondTot, COP

    def print_results(self):
        # Print Results
        print("COMPONENT DATAFRAMES:\n")
        print("Compressor:")
        print(self.COMP.df)
        print("\nEvaporator:")
        print(self.EVAP.df)
        print("\nDesuperheater:")
        print(self.DESURCH.df)
        print("\nCondenser:")
        print(self.COND.df)
        print("\nExpansion Valve:")
        print(self.DET.df)

    def plot_TS_diagram(self):
        # Create a Temperature-Entropy chart object
        chart = Temperature_Entropy_Chart.Object(self.fluid)

        # Collect temperature and entropy data points from each component
        points = [
            {"T": self.EVAP.Tsv - 273.15, "S": self.EVAP.Ssv},
            {"T": self.EVAP.Outlet.T - 273.15, "S": self.EVAP.Outlet.S},
            {"T": self.COMP.Outlet.T - 273.15, "S": self.COMP.Outlet.S},
            {"T": self.DESURCH.Outlet.T - 273.15, "S": self.DESURCH.Outlet.S},
            {"T": self.COND.Tsl- 273.15, "S": self.COND.Ssl},
            {"T": self.COND.Outlet.T - 273.15, "S": self.COND.Outlet.S},
            {"T": self.DET.Outlet.T - 273.15, "S": self.DET.Outlet.S},
            {"T": self.EVAP.Tsv - 273.15, "S": self.EVAP.Ssv}
        ]

        # Add points to the chart
        chart.add_points(points)

        # Display the chart
        chart.show(draw_arrows=True)

# Usage example
chiller_params = {
    'evap_params': {'Ti_degC': 5, 'surchauff': 5},
    'comp_params': {'Tcond_degC': 60, 'eta_is': 0.8, 'Tdischarge_target': 80, 'Qcomp': 100000},
    'cond_params': {'subcooling': 5}
}

chiller = Object(fluid="R407C", **chiller_params)
chiller.calculate_cycle()
EER, QcondTot, COP = chiller.calculate_performance()
print(f"EER: {round(EER, 1)}")
print(f"Total Condenser Heat (QcondTot): {round(QcondTot/1000, 1)} kW")
print(f"COP: {round(COP, 1)}")

chiller.print_results()


# Plot the T-S Diagram
chiller.plot_TS_diagram()