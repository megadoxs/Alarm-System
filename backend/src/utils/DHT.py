import asyncio
import adafruit_dht
import board

class DHT:
    def __init__(self, pin, topic, retries=5):
        self.dht = adafruit_dht.DHT11(pin)
        self.retries = retries
        self.topic = topic
        self.active = True

    async def detect_temp(self, lastTemp):
            for attempt in range(self.retries):
                try:
                    temp = self.dht.temperature
                    if temp is not None and (lastTemp is None or temp != float(lastTemp)):
                        return temp
                except RuntimeError:
                    await asyncio.sleep(0.5)
                await asyncio.sleep(0.1)
            return lastTemp

    async def detect_hum(self, lastHum):
            for attempt in range(self.retries):
                try:
                    temp = self.dht.humidity
                    if temp is not None and (lastHum is None or temp != float(lastHum)):
                        return temp
                except RuntimeError:
                    await asyncio.sleep(0.5)
                await asyncio.sleep(0.1)
            return lastHum

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def deinit(self):
        self.dht.exit()