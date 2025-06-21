from sqlalchemy import Column, Integer, String
from app.database import Base

class PCBuild(Base):
    __tablename__ = "pc_builds"

    id = Column(Integer, primary_key=True, index=True)
    processor = Column(String(100))
    graphics_card = Column(String(100))
    ram = Column(String(50))
    storage = Column(String(100))
    cooling = Column(String(100))
    case_style = Column(String(100))
    monitor = Column(String(100))
    rgb_lights = Column(String(100))
    mouse = Column(String(100))
    keyboard = Column(String(100))
    headset = Column(String(100))
    speakers = Column(String(100))
    power_supply = Column(String(100))
    os = Column(String(50))

