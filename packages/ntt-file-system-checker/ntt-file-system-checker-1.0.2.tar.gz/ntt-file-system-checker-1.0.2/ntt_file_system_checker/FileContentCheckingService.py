import os
import sys
import logging
from typing import *
from threading import Thread
from ntt_signal import Signal
from .constants import *
from .IFileContentChecker import *
from .IFileContentCheckingService import *
import time


class FileContentCheckingService(IFileContentCheckingService):
    def __init__(self) -> None:
        self.FileChanged = Signal()
        self.FileDeleted = Signal()
        self._bIsRunning: bool = False

        self.logger = logging.getLogger(SERVICE_LOGGING_NAME)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self._strTrackingFiles: Dict[str, List[str, Signal]] = {}

    @property
    def IsRunning(self) -> bool:
        return self._bIsRunning

    def Start(self) -> None:
        self.logger.info("Starting the File content checking service")

        self._bIsRunning = True
        thread = Thread(target=self._Running)
        thread.start()

    def _Running(self) -> None:
        while self._bIsRunning:
            time.sleep(0.2)
            for strFile, lstFileData in self._strTrackingFiles.items():
                with open(strFile, "r") as file:
                    strContent, fileChanged = lstFileData
                    strNewContent = file.read()

                    if strNewContent != strContent:
                        fileChanged.Emit()
                        self._strTrackingFiles[strFile][0] = strNewContent

    def Stop(self) -> None:
        self.logger.info("Stopping the file checking service")
        self._bIsRunning = False

    def AddCheckedFile(self, strFile: str, 
                                contentChanged: Signal) -> None:
        self.logger.info(f"Start tracking {strFile}")
        strContent: str = ""

        try:
            with open(strFile, "r") as file:
                strContent = file.read()
                contentChanged.Emit()
        except Exception as e:
            print(e)
            with open(strFile, "w") as file:
                file.write("")

        self._strTrackingFiles[strFile] = [strContent, contentChanged]