from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

def get_or_default(json: dict, name: str, default):
    try:
        return json[name]
    except:
        return default

@dataclass
class Gesture:
    gesture: str
    probability: float
    confidence: float
    displacement: float

    def toJSON(self) -> object:
        return {
            "gesture": self.gesture,
            "probability": self.probability,
            "confidence": self.confidence,
            "displacement": self.displacement,
        }

@dataclass
class Acceleration:
    x: float
    y: float
    z: float

@dataclass
class Angle:
    roll: float
    pitch: float
    yaw: float

    def toJSON(self) -> object:
        return {
            "roll": self.roll,
            "pitch": self.pitch,
            "yaw": self.yaw,
        }

@dataclass
class Gyro:
    x: float
    y: float
    z: float

class Button(Enum):
    NONE = 0
    TRIANGLE = 4
    SQUARE = 2
    CIRCLE = 1
    CIRCLE_SQUARE = 3
    CIRCLE_TRIANGLE = 5
    SQUARE_TRIANGLE = 6


class Hand(Enum):
    RIGHT = "right"
    LEFT = "left"

class TBleConnectionStatus(Enum):
    NONE = 0
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTING = 3
    DISCONNECTED = 4

class TBleSelector(Enum):
    NONE = 0
    SENSORS = 1
    VOICE = 2

class AppType(Enum):
    GUI = 1
    CLI = 2

@dataclass
class TSkinState:
    connected: bool
    selector: TBleSelector
    button: Optional[Button]
    angle: Optional[Angle]
    gesture: Optional[Gesture]


    def toJSON(self) -> object:
        return {
            "connected": self.connected,
            "selector": self.selector.value,
            "button": self.button.value if self.button else None,
            "angle": self.angle.toJSON() if self.angle else None,
            "gesture": self.gesture.toJSON() if self.gesture else None,
        }

@dataclass
class GestureConfig:
    model_path: str
    encoder_path: str
    name: str
    created_at: datetime
    gestures: List[str]
    num_sample: int = 10
    gesture_prob_th: float = 0.85
    confidence_th: float = 5

    @classmethod
    def FromJSON(cls, json: dict):
        return cls(
            json["model_path"],
            json["encoder_path"],
            json["name"],
            datetime.fromisoformat(json["created_at"]),
            json["gestures"],
            get_or_default(json, "num_sample", cls.num_sample),
            get_or_default(json, "gesture_prob_th", cls.gesture_prob_th),
            get_or_default(json, "confidence_th", cls.confidence_th)
            )
    
    def toJSON(self) -> object:
        return {
            "model_path": self.model_path,
            "encoder_path": self.encoder_path,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "gestures": self.gestures
        }

@dataclass
class TSkinConfig:
    address: str
    hand: Hand
    name: str = "Tactigon"
    gesture_config: Optional[GestureConfig] = None

    @classmethod
    def FromJSON(cls, json: dict):
        try:
            gesture_config = GestureConfig.FromJSON(json["gesture_config"])
        except:
            gesture_config = None

        return cls(
            json["address"],
            Hand(json["hand"]),
            get_or_default(json, "name", cls.name),
            gesture_config
        )
    
    def toJSON(self) -> object:
        return {
            "address": self.address,
            "hand": self.hand.value,
            "name": self.name,
            "gesture_config": self.gesture_config.toJSON() if self.gesture_config else None,
        }