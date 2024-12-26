import json
import logging
import os
from datetime import datetime


class MyLogger:

    def __init__(self):
        self.logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self.rootLogger = logging.getLogger()
        self.this_date = datetime.now().strftime('%Y-%m-%d')
        self.fileHandler = logging.FileHandler(
            "{0}/{1}.log".format(os.environ.get("logPath", ""), f"{self.this_date}.log"))
        self.fileHandler.setFormatter(self.logFormatter)
        self.rootLogger.addHandler(self.fileHandler)

        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setFormatter(self.logFormatter)
        self.rootLogger.addHandler(self.consoleHandler)

    def log(self, message: dict):
        # makes sure the date file always rolls over.
        if self.this_date is not datetime.now().strftime('%Y-%m-%d'):
            self.this_date = datetime.now().strftime('%Y-%m-%d')
            self.fileHandler = logging.FileHandler(
                "{0}/{1}.log".format(os.environ.get("logPath", ""), f"{self.this_date}.log"))
            self.fileHandler.setFormatter(self.logFormatter)
            self.rootLogger.addHandler(self.fileHandler)
        output = f"Logger:\n{json.dumps(message)}\n"
        self.rootLogger.debug(output)
        print(output)

