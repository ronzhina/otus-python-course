class LowFuelError(Exception):
    def __str__(self):
        return "LowFuelError"


class NotEnoughFuel(Exception):
    def __str__(self):
        return "NotEnoughFuel"


class CargoOverload(Exception):
    def __str__(self):
        return "CargoOverload"
