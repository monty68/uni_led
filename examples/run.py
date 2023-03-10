import asyncio
import logging

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from uni_led import LEDBLE

_LOGGER = logging.getLogger(__name__)

ADDRESS = "D0291B39-3A1B-7FF2-787B-4E743FED5B25"
ADDRESS = "D0291B39-3A1B-7FF2-787B-4E743FED5B25"


async def run() -> None:
    scanner = BleakScanner()
    future: asyncio.Future[BLEDevice] = asyncio.Future()

    def on_detected(device: BLEDevice, adv: AdvertisementData) -> None:
        if future.done():
            return
        _LOGGER.info("Detected: %s", device)
        if device.address.lower() == ADDRESS.lower():
            _LOGGER.info("Found device: %s", device.address)
            future.set_result(device)

    scanner.register_detection_callback(on_detected)
    await scanner.start()

    def on_state_changed(state: LEDBLEState) -> None:
        _LOGGER.info("State changed: %s", state)

    device = await future
    led = UNILEDBLE(device)
    cancel_callback = led.register_callback(on_state_changed)
    await led.update()
    await led.turn_on()
    await led.set_rgb((255, 0, 0), 255)
    await asyncio.sleep(1)
    await led.set_rgb((0, 255, 0), 128)
    await asyncio.sleep(1)
    await led.set_rgb((0, 0, 255), 255)
    await asyncio.sleep(1)
    await led.set_rgbw((255, 255, 255, 128), 255)
    await asyncio.sleep(1)
    await led.turn_off()
    await led.update()
    cancel_callback()
    await scanner.stop()


logging.basicConfig(level=logging.INFO)
logging.getLogger("uni_led").setLevel(logging.DEBUG)
asyncio.run(run())
