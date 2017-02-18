import json
import tempfile
import os
import os.path
import logging
import sys

logger = logging.getLogger(__name__)

class Settings():
    def __init__(self, CONFIG_FILE_LOCATION=None):
        self.CONFIG_FILE_NAME = "config.json"
        self.CONFIG_FILE_LOCATION = self.CONFIG_FILE_NAME
        try:
            os.path.isfile(CONFIG_FILE_LOCATION)
        except (FileNotFoundError, TypeError):
            for location in sys.path:
                try:
                    if os.path.isfile(os.path.join(location, self.CONFIG_FILE_NAME)):
                        self.CONFIG_FILE_LOCATION = os.path.join(location, self.CONFIG_FILE_NAME)
                except FileNotFoundError:
                    pass
        try:
            self.config = json.loads(open(self.CONFIG_FILE_LOCATION).read())
        except FileNotFoundError:
            raise AttributeError("Config file " + self.CONFIG_FILE_LOCATION + " not found.\nExiting")
        except json.decoder.JSONDecodeError as ex:
            raise AttributeError("Config file " + self.CONFIG_FILE_LOCATION + " is incorrect.\nError message: " + str(ex))

    def update(self):
        fd, path = tempfile.mkstemp()
        os.write(fd, json.dumps(self.config, indent=4).encode('utf-8'))
        os.close(fd)
        os.rename(path, self.CONFIG_FILE_LOCATION)  # On Linux systems move is atomic
