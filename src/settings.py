import json
import tempfile
import os
import os.path
import logging
import sys

logger = logging.getLogger(__name__)


class Settings:
    def __init__(self, config_file_location=None):
        self.CONFIG_FILE_NAME = "config.json"
        self.CONFIG_FILE_LOCATION = self.CONFIG_FILE_NAME
        if config_file_location != None:
            self.CONFIG_FILE_LOCATION = config_file_location
        self.reload()

    def reload(self):
        if not os.path.isfile(self.CONFIG_FILE_LOCATION):
            for location in sys.path:
                try:
                    if os.path.isfile(os.path.join(location, self.CONFIG_FILE_NAME)):
                        self.CONFIG_FILE_LOCATION = os.path.join(location, self.CONFIG_FILE_NAME)
                        break
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
        os.write(fd, json.dumps(self.config, indent=4, sort_keys=True).encode('utf-8'))
        os.close(fd)
        os.rename(path, self.CONFIG_FILE_LOCATION)  # On Linux systems move is atomic

        # Let's make sure that the changes were really written
        correct_config = self.config
        self.reload()
        if correct_config != self.config:
            raise Exception()
