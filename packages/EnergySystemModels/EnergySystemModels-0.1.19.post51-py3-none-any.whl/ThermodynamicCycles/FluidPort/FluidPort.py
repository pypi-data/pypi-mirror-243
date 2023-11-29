from CoolProp.CoolProp import PropsSI

class FluidPort:
    def __init__(self, fluid='ammonia', P=101325, h=10000):
        self.F = None
        self.P = P
        self.h = h
        self.fluid = fluid
        self.T = None
        self.S = None
        self.calculate_properties()

    def propriete(self, Pro, I1, ValI1, I2, ValI2):
        result = PropsSI(Pro, I1, ValI1, I2, ValI2, self.fluid)
        return result

    def calculate_properties(self):
        # Ensure all needed properties are set
        if self.P is not None and self.h is not None and self.fluid is not None:
            self.T = PropsSI('T', 'P', self.P, 'H', self.h, self.fluid)
            self.S = PropsSI('S', 'P', self.P, 'H', self.h, self.fluid)
        else:
            print("Insufficient data to calculate properties.")

# # Example usage
# port = FluidPort()
# print("Temperature (K):", port.T)
# print("Entropy (J/kg-K):", port.S)
