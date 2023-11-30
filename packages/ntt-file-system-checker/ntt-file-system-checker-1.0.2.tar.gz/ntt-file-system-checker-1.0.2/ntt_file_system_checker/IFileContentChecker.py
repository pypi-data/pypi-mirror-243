from abc import *
from ntt_signal import *


class IFileContentChecker(ABC):
    @abstractproperty
    def ContentChanged(self) -> Signal:
        pass

    @abstractproperty
    def Content(self) -> str:
        pass