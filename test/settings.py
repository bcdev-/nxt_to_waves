from src import settings
from unittest import TestCase
import json


class Test(TestCase):
    def test_update_config_file(self):
        data = {"static_parameter": "static", "dynamic_parameter": 123}
        settings.CONFIG_FILE_LOCATION = "/tmp/_update_config_file_test.json"
        self.assertEqual(settings.config, {})

        f = open(settings.CONFIG_FILE_LOCATION, "w")
        f.write(json.dumps(data))
        f.close()
        settings.read_settings()
        self.assertEqual(data, settings.config)

        settings.config["dynamic_parameter"] = 666
        settings.read_settings()
        self.assertEqual(data, settings.config)

        settings.config["dynamic_parameter"] = 666
        settings.update()
        data["dynamic_parameter"] = 666
        self.assertEqual(data, settings.config)
