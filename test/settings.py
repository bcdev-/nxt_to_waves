from src.settings import Settings
from unittest import TestCase
import json


class Test(TestCase):
    def test_update_config_file(self):
        data = {"static_parameter": "static", "dynamic_parameter": 123}
        CONFIG_FILE_LOCATION = "/tmp/_update_config_file_test.json"

        f = open(CONFIG_FILE_LOCATION, "w")
        f.write(json.dumps(data))
        f.close()
        settings = Settings(CONFIG_FILE_LOCATION)
        self.assertEqual(settings.config, data)

        settings.config["dynamic_parameter"] = 666
        settings.reload()
        self.assertEqual(data, settings.config)

        settings.config["dynamic_parameter"] = 666
        settings.update()
        data["dynamic_parameter"] = 666
        self.assertEqual(data, settings.config)

        settings.reload()
        self.assertEqual(data, settings.config)
