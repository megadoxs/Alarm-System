

import utils.LED
from utils.LED import LED
import board
import time
import asyncio


class LEDSController:
    def __init__(self, interval):
        self.interval = interval
        self.leds = [
            LED(board.D16), # Green LED
            LED(board.D20), # Yellow LED
            LED(board.D21)  # Red LED
        ]
        self.leds[0].on() # Enables the green LED by default
        self.active = True

    async def start(self, delay): # used to arm system
        try:
            self.leds[0].off()  # turns green LED off

            start_time = time.time()
            while time.time() - start_time < delay: # blinks yellow LED
                if self.active:
                    self.leds[1].toggle()
                await asyncio.sleep(self.interval) # blink time

            if self.active:
                self.leds[1].off()  # turns yellow LED off
        except asyncio.CancelledError:
            if self.active:
                self.leds[0].on()
                self.leds[1].off()

    def detecting(self):
        if self.active:
            self.leds[2].on()

    def reset(self):
        self.leds[0].off()
        self.leds[1].off()
        self.leds[2].off()

    async def warning(self): # used in disarm
        try:
            self.leds[2].off()

            while True:
                if self.active:
                    self.leds[1].toggle()
                await asyncio.sleep(self.interval)
        except asyncio.CancelledError:
            if self.active:
                self.leds[1].off()
                self.leds[0].on()

    async def alert(self):
        self.leds[0].off()
        try:
            while True:
                if self.active:
                    self.leds[2].toggle()
                await asyncio.sleep(self.interval)
        except asyncio.CancelledError:
            if self.active:
                self.leds[2].off()
                self.leds[0].on()

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
        self.leds[0].off()
        self.leds[1].off()
        self.leds[2].off()
    
    def deinit(self):
        for led in self.leds:
            led.deinit()