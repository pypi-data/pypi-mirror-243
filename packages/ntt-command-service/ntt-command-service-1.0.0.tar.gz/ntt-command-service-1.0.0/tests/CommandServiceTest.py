import unittest
from unittest.mock import *
from ntt_command_service import *


class CommandServiceTest(unittest.TestCase):
    serCommandService: ICommandService = None

    def setUp(self) -> None:
        self.serCommandService = CommandService()

    def test_GivenACommand_WhenBeAddedIntoCommandService_ThenItIsExecuted(self):
        testCommand = Mock(spec=ICommand)
        testCommand.CanExecute.return_value = True

        self.serCommandService.AddCommand(testCommand)

        testCommand.Execute.assert_called_once()

    def test_GivenACommandButCannotExecute_WhenBeAddedIntoCommandService_ThenItIsNotExecuted(self):
        testCommand = Mock(spec=ICommand)
        testCommand.CanExecute.return_value = False

        self.serCommandService.AddCommand(testCommand)

        testCommand.Execute.assert_not_called()

    def test_GivenACommand_WhenExecutedAndUndo_ThenTheCommandUndoIsCalled(self):
        testCommand = Mock(spec=ICommand)
        testCommand.CanExecute.return_value = True
        self.serCommandService.AddCommand(testCommand)

        self.serCommandService.Undo()
        testCommand.Undo.assert_called_once()

    def test_GivenACommandButCannotBeExecuted_WhenAddAndUndo_ThenTheCommandUndoIsNotCalled(self):
        testCommand_1 = Mock(spec=ICommand)
        testCommand_1.CanExecute.return_value = True
        testCommand_2 = Mock(spec=ICommand)
        testCommand_2.CanExecute.return_value = False
        self.serCommandService.AddCommand(testCommand_1)
        self.serCommandService.AddCommand(testCommand_2)

        self.serCommandService.Undo()

        testCommand_1.Execute.assert_called_once()
        testCommand_1.Undo.assert_called_once()
        testCommand_2.Undo.assert_not_called()

    def test_WhenAskCanUndoAtTheBegging_ThenReturnsFalse(self):
        self.assertFalse(self.serCommandService.CanUndo())

    def test_GivenServiceWith1Command_WhenAskCanUndo_ThenReturnsTrue(self):
        testCommand = Mock(spec=ICommand)
        testCommand.CanExecute.return_value = True
        self.serCommandService.AddCommand(testCommand)

        self.assertTrue(self.serCommandService.CanUndo())

    def test_Given2CommandAddedToService_WhenUndo_ThenUndoIsCalled(self):
        testCommand_1 = Mock(spec=ICommand)
        testCommand_1.CanExecute.return_value = True
        testCommand_2 = Mock(spec=ICommand)
        testCommand_2.CanExecute.return_value = True
        self.serCommandService.AddCommand(testCommand_1)
        self.serCommandService.AddCommand(testCommand_2)

        self.serCommandService.Undo()
        self.serCommandService.Undo()

        testCommand_1.Undo.assert_called_once()
        testCommand_2.Undo.assert_called_once()

    def test_Given2CommandsAreAdded_WhenClear_ThenCannotUndo(self):
        testCommand_1 = Mock(spec=ICommand)
        testCommand_1.CanExecute.return_value = True
        testCommand_2 = Mock(spec=ICommand)
        testCommand_2.CanExecute.return_value = True
        self.serCommandService.AddCommand(testCommand_1)
        self.serCommandService.AddCommand(testCommand_2)

        self.serCommandService.Clear()


    def test_GivenCommandServiceCanNotUndo_WhenUndo_ThenRaiseError(self):
        with self.assertRaises(CommandServiceEmptyError) as context:
            self.serCommandService.Undo()

        self.assertEqual(str(context.exception), "Command Service has no command") 