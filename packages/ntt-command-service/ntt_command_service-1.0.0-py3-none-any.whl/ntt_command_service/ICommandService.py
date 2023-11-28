from abc import *
from .ICommand import ICommand


class ICommandService(ABC):
    @abstractmethod
    def AddCommand(self, iCommand: ICommand) -> None:
        pass

    @abstractmethod
    def Undo(self) -> None:
        pass

    @abstractmethod
    def CanUndo(self) -> bool:
        pass

    @abstractmethod
    def Clear(self) -> None:
        pass