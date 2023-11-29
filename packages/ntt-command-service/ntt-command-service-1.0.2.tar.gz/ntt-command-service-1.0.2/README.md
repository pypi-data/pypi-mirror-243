# ntt-command-service
Library for implementing Command Pattern

## Examples

```python
from ntt_command_service import *
from typing import List

fScores: List[float] = []

class AppendDataCommand(ICommand):
    def __init__(self, fScores: List[float], fScore: float):
        self._fScores = fScores
        self._fScore = fScore

    def Execute(self) -> None:
        self._fScores.append(self._fScore)

    def CanExecute(self) -> bool:
        return True

    def Undo(self) -> None:
        self._fScore.pop()

serCommandService = CommandService()
serCommandService.AddCommand(AppendDataCommand(fScores, 3))
# ----> fScores = [3]
serCommandService.AddCommand(AppendDataCommand(fScores, 5))
# ----> fScores = [3, 5]
serCommandService.AddCommand(AppendDataCommand(fScores, 1))
# ----> fScores = [3, 5, 1]
serCommandService.Undo()
# ----> fScores = [3, 5]
serCommandService.Clear()
serCommandService.CanUndo()
# ----> False
```