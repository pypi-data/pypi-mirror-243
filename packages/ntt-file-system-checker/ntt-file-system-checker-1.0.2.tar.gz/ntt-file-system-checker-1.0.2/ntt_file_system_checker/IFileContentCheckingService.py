from abc import *
from ntt_signal import *


class IFileContentCheckingService(ABC):
    @abstractproperty
    def IsRunning(self) -> bool:
        pass

    @abstractmethod
    def AddCheckedFile(self, strFile: str, 
                                contentChanged: Signal) -> None:
        pass

    @abstractmethod
    def Start(self) -> None:
        pass

    @abstractmethod
    def Stop(self) -> None:
        pass