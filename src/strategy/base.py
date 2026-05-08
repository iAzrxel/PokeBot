from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def choose(self, player, battle):
        pass