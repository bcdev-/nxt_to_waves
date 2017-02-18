import time
from .settings import config, read_settings

class Gateway:
    def __init__(self):
        pass

    def tick(self):
        print("Tick")
        last_block = config
        # last_block =
        # nxt.get_newest_block()
        # nxt.scan_deposits()
        # waves.distribute_deposits()


    def start(self):
        print("Starting NXT->Waves Gateway")
        read_settings()
        while True:
            self.tick()
            time.sleep(1)
