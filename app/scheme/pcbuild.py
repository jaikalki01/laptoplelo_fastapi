from pydantic import BaseModel

class PCBuild(BaseModel):
    processor: str
    graphics_card: str
    ram: str
    storage: str
    cooling: str
    case_style: str
    monitor: str
    rgb_lights: str
    mouse: str
    keyboard: str
    headset: str
    speakers: str
    power_supply: str
    os: str
