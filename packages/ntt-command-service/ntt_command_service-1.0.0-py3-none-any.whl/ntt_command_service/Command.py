from .ICommand import ICommand


class Command(ICommand):
    def __init__(self, fExecute: callable) -> None:
        super().__init__()
        self._fExecute = fExecute

    def Execute(self) -> None:
        self._fExecute()

    def CanExecute(self) -> bool:
        return True

    def Undo(self) -> None:
        pass