import asyncio
from multiprocessing.managers import State

from dotenv import load_dotenv
import os
import board

from controllers.Backup_Controller import BackupController
from controllers.Mailer_Controller import Mailer_Controller
from controllers.LEDS_Controller import LEDSController
from controllers.MQTT_Controller import MQTT_Controller
from controllers.Logs_Controller import LOGS_Controller
from utils.Camera import Camera
from utils.Montion_Detector import Montion_Detector_Controller
from controllers.Screen_Controller import Screen_Controller
# from utils.Key_Scanner import Key_scanner
from utils.Button import Button
from utils.Buzzer import Buzzer
from utils.DHT import DHT
from utils.State import State

load_dotenv()


class AlarmSystem:
    def __init__(self):
        self.state = State.DISARMED
        self.task = None

        self.topics = os.getenv("TOPICS").split(",")
        self.led_blink_interval = float(os.getenv("LED_BLINK_INTERVAL"))
        self.detection_delay = int(os.getenv("DETECTION_DELAY"))
        self.alarm_delay = int(os.getenv("ALARM_DELAY"))
        self.logs = LOGS_Controller(os.getenv("LOGS_LOCATION"))
        self.mqtt = MQTT_Controller(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT")), int(os.getenv("MQTT_TIMEOUT")), os.getenv("MQTT_USERNAME"), os.getenv("MQTT_KEY"), self.logs)
        self.leds = LEDSController(self.led_blink_interval)
        self.screen = Screen_Controller()
        self.motion_detector = Montion_Detector_Controller()
        # self.key_scanner = Key_scanner()
        self.button = Button(board.D12)
        self.buzzer = Buzzer(board.D18)
        self.dht = DHT(board.D5, [self.topics[1], self.topics[2]])
        self.camera = Camera(os.getenv("MEDIA_LOCATION"), os.getenv("IMAGE_LOCATION"), os.getenv("VIDEO_LOCATION"))
        self.mail = Mailer_Controller(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT"), os.getenv("SMTP_USER"), os.getenv("SMTP_PWD"), os.getenv("ALERT_FROM"), os.getenv("ALERT_TO"))
        self.backup = BackupController(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), os.getenv("GOOGLE_CLOUD_PROJECT_ID"), os.getenv("GOOGLE_CLOUD_BUCKET_NAME"), os.getenv("LOGS_LOCATION"), os.getenv("MEDIA_LOCATION"))

        # this is the screen
        self.mqtt.sub(self.topics[3], lambda payload: self.activate() if payload == "ON" else self.deactivate())
        self.mqtt.sub(self.topics[4], lambda payload: self.screen.activate() if payload == "ON" else self.screen.deactivate())
        self.mqtt.sub(self.topics[5], lambda payload: self.buzzer.activate() if payload == "ON" else self.buzzer.deactivate())
        self.mqtt.sub(self.topics[6], lambda payload: self.leds.activate() if payload == "ON" else self.leds.deactivate())
        self.mqtt.sub(self.topics[7], lambda payload: self.dht.activate() if payload == "ON" else self.dht.deactivate())
        self.mqtt.sub(self.topics[8], lambda payload: self.screen.activateTime() if payload == "ON" else self.screen.deactivateTime())

    def activate(self):
        self.state = self.state.ARMED
        self.task.cancel()

    def deactivate(self):
        self.state = self.state.DISARMED
        self.task.cancel()

    async def main(self):
        asyncio.create_task(self.backup_files())
        while True:
            try:
                if self.state == State.DISARMED:
                    self.task = asyncio.create_task(self.idle())
                    await self.task

                elif self.state == State.ARMING:
                    self.task = asyncio.create_task(self.activate_alarm())
                    await self.task

                elif self.state == State.ARMED:
                    self.task = asyncio.create_task(self.detect())
                    await self.task

                elif self.state == State.DISARMING:
                    self.task = asyncio.create_task(self.deactivate_alarm())
                    await self.task

                elif self.state == State.ALERT:
                    self.task = asyncio.create_task(self.alert())
                    await self.task
            except asyncio.CancelledError:
                continue

    async def backup_files(self):
        while True:
            self.backup.upload()
            await asyncio.sleep(3600)

    async def idle(self):
        self.mqtt.save(self.topics[0], self.state)
        self.logs.save(self.topics[0], self.state)

        activate_task = asyncio.create_task(self.button.onClick())
        time_task = asyncio.create_task(self.screen.time())
        temp_task = asyncio.create_task(self.temp())
        hum_task = asyncio.create_task(self.hum())

        tasks = [activate_task, time_task, temp_task, hum_task]

        try:
            done, pending = await asyncio.shield(asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED
            ))

            for task in pending:
                task.cancel()

            self.state = State.ARMING
        except asyncio.CancelledError:
            self.leds.reset()
            for task in tasks:
                task.cancel()

    async def temp(self):
        lastTemp = self.logs.getLatest(self.dht.topic[0])
        while True:
            if self.dht.active:
                if lastTemp is not None:
                    lastTemp = float(lastTemp)
                    self.screen.temp(lastTemp)

                temp = await self.dht.detect_temp(lastTemp)
                if temp is not None and (lastTemp is None or temp != float(lastTemp)):
                    self.mqtt.save(self.dht.topic[0], temp)
                    self.logs.save(self.dht.topic[0], temp)
                    lastTemp = temp
            else:
                self.screen.clearTemp()
                await asyncio.sleep(0.1)

    async def hum(self):
        lastHum = self.logs.getLatest(self.dht.topic[1])
        while True:
            if self.dht.active:
                if lastHum is not None:
                    lastHum = float(lastHum)

                hum = await self.dht.detect_hum(lastHum)
                if hum is not None and (lastHum is None or hum != float(lastHum)):
                    self.mqtt.save(self.dht.topic[1], hum)
                    self.logs.save(self.dht.topic[1], hum)
                    lastHum = hum
            else:
                await asyncio.sleep(0.1)

    async def activate_alarm(self):
        self.mqtt.save(self.topics[0], self.state)
        self.logs.save(self.topics[0], self.state)

        activate_task = asyncio.create_task(self.leds.start(self.alarm_delay))
        cancel_task = asyncio.create_task(self.button.onClick())
        buzzer_task = asyncio.create_task(self.buzzer.warning(self.led_blink_interval))
        screen_task = asyncio.create_task(self.screen.delay(self.alarm_delay))

        tasks = [activate_task, cancel_task, buzzer_task, screen_task]

        try:
            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

            finished_task = done.pop()

            if finished_task == activate_task:
                self.state = State.ARMED
            else:
                self.state = State.DISARMED
        except asyncio.CancelledError:
            for task in tasks:
                task.cancel()

    async def detect(self):
        self.mqtt.save(self.topics[0], self.state)
        self.logs.save(self.topics[0], self.state)

        self.leds.detecting()
        await asyncio.create_task(self.motion_detector.detect())
        self.state = State.DISARMING

    async def deactivate_alarm(self):
        self.mqtt.save(self.topics[0], self.state)
        self.logs.save(self.topics[0], self.state)

        # deactivate_task = asyncio.create_task(self.key_scanner.detect())
        deactivate_task = asyncio.create_task(self.button.onClick())
        light_task = asyncio.create_task(self.leds.warning())
        buzzer_task = asyncio.create_task(self.buzzer.warning(self.led_blink_interval))
        screen_task = asyncio.create_task(self.screen.delay(self.detection_delay))

        tasks = [deactivate_task, light_task, buzzer_task, screen_task]

        try:
            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

            finished_task = done.pop()
            if finished_task == deactivate_task:
                self.state = State.DISARMED
            else:
                self.state = State.ALERT
        except asyncio.CancelledError:
            for task in tasks:
                task.cancel()

    async def alert(self):
        self.mqtt.save(self.topics[0], self.state)
        self.logs.save(self.topics[0], self.state)

        # deactivate_task = asyncio.create_task(self.key_scanner.detect())
        deactivate_task = asyncio.create_task(self.button.onClick())
        record_task = asyncio.create_task(self.camera.record())
        light_task = asyncio.create_task(self.leds.alert())
        buzzer_task = asyncio.create_task(self.buzzer.alert())
        self.screen.alert()
        self.mail.send_emergency_alert()

        tasks = [deactivate_task, record_task, light_task, buzzer_task]

        try:
            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

            self.state = State.DISARMED
        except asyncio.CancelledError:
            for task in tasks:
                task.cancel()

if __name__ == '__main__':
    alarm = AlarmSystem()
    try:
        asyncio.run(alarm.main())
    except asyncio.CancelledError:
        alarm.leds.deinit()
        alarm.motion_detector.deinit()
        alarm.button.deinit()
        alarm.buzzer.deinit()
        alarm.dht.deinit()
        alarm.camera.deinit()