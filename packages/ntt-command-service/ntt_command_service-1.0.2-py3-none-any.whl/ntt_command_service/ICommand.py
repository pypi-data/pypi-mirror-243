from abc import *


class ICommand(ABC):
    @abstractmethod
    def Execute(self) -> None:
        pass

    @abstractmethod
    def CanExecute(self) -> bool:
        pass

    @abstractmethod
    def Undo(self) -> None:
        pass