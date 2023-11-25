# pylint: disable=C0114
class Climate:
    """This is the package to convert Temperature units e.g celcius, fahrenheit, Kelvin"""

    def __init__(self, degree):
        self.degree = degree

    def fahrenheit(self):  # Takes single argument as Celsius
        """
        This function converts Celsius to Fahrenheit
        Argument should be Number
        """
        return f'{(self.degree * 9/5) + 32}°F'

    def celsius(self):  # Takes single argument as Fahrenheit
        """
        This function converts Fahrenheit to Celsius
        Argument should be Number
        """
        return f'{(self.degree - 32) * (5/9)}°C'

    def kelvin(self):  # Takes single argument as Celcius
        """
        This function converts Celsius to Kelvin
        Argument should be Number
        """
        return f'{self.degree + 273.15}°K'
