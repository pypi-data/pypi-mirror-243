__version__ = "4.1.9"
__all__ = ["TSkin", "TSkinConfig", "GestureConfig", "TSkinState", "Hand", "Button", "Angle", "Gyro", "Acceleration", "Gesture"]

import sys
import logging
from typing import Optional
from multiprocessing import Pipe

if sys.platform == "win32":
    from multiprocessing.connection import PipeConnection
else:
    from multiprocessing.connection import Pipe as PipeConnection

from .hal import BLE
from .middleware import Tactigon_Gesture
from .models import TBleSelector, Gesture, Button, Angle, Acceleration, Gyro, TSkinState, TSkinConfig, Hand, GestureConfig

class TSkin:
    logger: logging.Logger
    config: TSkinConfig

    ble: BLE
    tgesture: Tactigon_Gesture

    sensor_rx: Optional[PipeConnection] = None
    sensor_tx: Optional[PipeConnection] = None

    adpcm_rx: Optional[PipeConnection] = None
    adpcm_tx: Optional[PipeConnection] = None


    def __init__(self,
                config: TSkinConfig,
                debug: bool = False
                ):
        
        self.logger = logging.getLogger()
        self.logger.addHandler(logging.StreamHandler())

        if debug:
            self.logger.setLevel(logging.DEBUG)

        self.debug = debug
        self.config = config

        if self.config.gesture_config:
            self.sensor_rx, self.sensor_tx = Pipe(duplex=False)

            self.tgesture = Tactigon_Gesture(
                self.config.gesture_config,
                self.sensor_rx,
                self.logger,
            )

        self.BLE = BLE(self.config.name, self.config.address, self.config.hand, self.logger, self.sensor_tx, None, None, self.adpcm_tx)

        self.logger.debug("[TSkin] Object create. Config: %s", self.config)
           
    def start(self):
        self.BLE.start()

        if self.config.gesture_config:
            self.tgesture.start()

        self.logger.debug("[TSkin] TSkin %s (%s) started", self.config.name, self.config.address)

    def terminate(self):
        if self.config.gesture_config:
            self.tgesture.terminate()

        self.BLE.terminate()

        self.logger.debug("[TSkin] TSkin %s (%s) terminated", self.config.name, self.config.address)

    def select_sensors(self) -> None:
        if self.debug:
            logging.info("[TSkin] TSkin %s (%s) select sensors stream.", self.config.name, self.config.address)
        return self.BLE.select_sensors()
    
    def select_voice(self) -> None:
        if self.debug:
            logging.info("[TSkin] TSkin %s (%s) select voice stream.", self.config.name, self.config.address)
        return self.BLE.select_voice()
    
    @property
    def selector(self) -> TBleSelector:
        return self.BLE.selector
    
    @property
    def connected(self) -> bool:
        return self.BLE.connected
    
    @property
    def gesture(self) -> Optional[Gesture]:
        if not self.config.gesture_config:
            return None
        
        return self.tgesture.gesture(reset=True)
    
    @property
    def gesture_preserve(self) -> Optional[Gesture]:
        if not self.config.gesture_config:
            return None
        
        return self.tgesture.gesture(reset=False)

    @property
    def button(self) -> Optional[Button]:
        return self.BLE.button
    
    @property
    def angle(self) -> Optional[Angle]:
        return self.BLE.angle
    
    @property
    def acceleration(self) -> Optional[Acceleration]:
        return self.BLE.acceleration
    
    @property
    def gyro(self) -> Optional[Gyro]:
        return self.BLE.gyro
    
    @property
    def state(self) -> TSkinState:
        s = self.BLE.selector

        return TSkinState(
            self.connected,
            s,
            self.button,
            self.angle,
            self.gesture,
        )
    
    @property
    def state_preserve_gesture(self) -> TSkinState:
        s = self.BLE.selector

        return TSkinState(
            self.connected,
            s,
            self.button if s == TBleSelector.SENSORS else None,
            self.angle if s == TBleSelector.SENSORS else None,
            self.gesture_preserve if s == TBleSelector.SENSORS else None,
        )
    
    def __str__(self):
        return "TSkin(name='{0}', address='{1}', gesture={2})".format(self.config.name, self.config.address, self.config.gesture_config)