from abc import ABC

from homework_02.exceptions import LowFuelError, NotEnoughFuel


class Vehicle(ABC):

    def __init__(self, weight=1000, fuel=0, fuel_consumption=10):
        self.started = False
        self.weight = weight
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption

    def start(self):
        if not self.started:
            if self.fuel > 0:
                self.started = True
            else:
                raise LowFuelError

    def move(self, distance):
        fuel_for_distance = distance * self.fuel_consumption
        if self.fuel >= fuel_for_distance:
            self.fuel -= fuel_for_distance
        else:
            raise NotEnoughFuel
