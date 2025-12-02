import digitalio
import asyncio

class Buzzer:
    def __init__(self, pin):
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.OUTPUT
        self.pin.value = False
        self.active = True

    def on(self):
        self.pin.value = True

    def off(self):
        self.pin.value = False

    async def warning(self, interval):
        try:
            while True:
                if self.active:
                    self.on()
                await asyncio.sleep(interval)
                self.off()
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            self.off()

    async def alert(self):
        try:
            while True:
                if self.active:
                    self.on()
                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            self.off()

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def deinit(self):
        self.pin.deinit()