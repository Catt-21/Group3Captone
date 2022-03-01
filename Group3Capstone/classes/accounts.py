from abc import ABC, abstractmethod
class Accounts():
    @abstractmethod
    def __createAccount__(self):
        pass

    @abstractmethod
    def __deleteAccount__(self):
         pass

    @abstractmethod
    def __editAccount__(self):
        pass