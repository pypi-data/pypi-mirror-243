from ntt_signal import *
from .IFileContentCheckingService import *
from .IFileContentChecker import *
from nttinject import *


@dependency_inject(IFileContentCheckingService)
class FileContentChecker(IFileContentChecker):
    def __init__(self, serFileContentCheckingService: IFileContentCheckingService,
                        strFileName: str) -> None:
        self._ContentChanged = Signal()
        self._strFileName = strFileName
        self._strContent: str = ""
        
        serFileContentCheckingService.AddCheckedFile(strFileName, 
                                                        self._ContentChanged)

    @property
    def Content(self) -> str:
        with open(self._strFileName, "r") as file:
            self._strContent = file.read()

        return self._strContent

    @property
    def ContentChanged(self) -> Signal:
        return self._ContentChanged