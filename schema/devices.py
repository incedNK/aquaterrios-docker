from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional, Union, List


# Pump's schemas
class Flow(BaseModel):
    pump_id: str
    capacity: Union[float, None] = None
    current: Union[float, None] = None


class AddPump(Flow):
    system_id: int


class UpdatePump(BaseModel):
    current: float
    updated_at: datetime = datetime.now()


class Pump(Flow):
    system_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class AddFlowData(BaseModel):
    pump_id: str
    flow_rate: float
    date: datetime = datetime.now()


class GetFlowData(BaseModel):
    flow_rate: Optional[float]
    date: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


# Valve's schemas
class ValveBase(BaseModel):
    valve_id: str
    status: Union[bool, None] = None


class AddValve(ValveBase):
    system_id: int


class UpdateValve(BaseModel):
    status: Optional[bool]
    updated_at: datetime = datetime.now()


class UpdateValveStatus(BaseModel):
    status: Optional[bool]
    updated_at: datetime = datetime.now()


class Valve(ValveBase):
    system_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True

# Sensor's schemas


class SensorBase(BaseModel):
    sensor_id: str
    readings: Optional[float] = 50
    set_lvl_1: bool = False
    set_lvl_2: bool = True
    set_lvl_3: bool = False


class AddSensor(SensorBase):
    system_id: int


class UpdateSensor(BaseModel):
    set_lvl_1: Optional[bool]
    set_lvl_2: Optional[bool]
    set_lvl_3: Optional[bool]
    updated_at: datetime = datetime.now()


class Sensor(SensorBase):
    system_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class AddSensorData(BaseModel):
    sensor_id: str
    bat_level: float
    level_1: float
    level_2: float
    level_3: float
    temperature: float
    moisture: float


class SensorData(BaseModel):
    date: datetime
    bat_level: float
    level_1: float
    level_2: float
    level_3: float
    temperature: float
    moisture: float

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class SensorControler(BaseModel):
    section_id: int
    sensor_id: Optional[str]
    updated_at: datetime = datetime.now()


class SControl(BaseModel):
    id: int
    updated_at: datetime
    sensor_id: Union[str, None] = None

    class Config:
        orm_mode = True


class SControlWithID(BaseModel):
    detail: str = "New section was successfully added to shift"
    id: int

    class Config:
        orm_mode = True


class SectionCreate(BaseModel):
    shift_id: int
    valve_id: str
    updated_at: datetime = datetime.now()


class SectionUpdate(BaseModel):
    sensors_settings: Optional[str]
    starts_at: Optional[float]
    stops_at: Optional[float]
    updated_at: datetime = datetime.now()


class Section(BaseModel):
    id: int
    updated_at: datetime
    valve_id: str
    sensors_settings: Optional[str]
    starts_at: Optional[float]
    stops_at: Optional[float]
    section_sensors: List[SControl] = []

    class Config:
        orm_mode = True


class SectionWithID(BaseModel):
    detail: str = "New section was successfully added to shift"
    id: int

    class Config:
        orm_mode = True


class TimerControl(BaseModel):
    shift_id: int
    Mon: Optional[bool] = None
    Tue: Optional[bool] = None
    Wed: Optional[bool] = None
    Thu: Optional[bool] = None
    Fri: Optional[bool] = None
    Sat: Optional[bool] = None
    Sun: Optional[bool] = None
    starts: Optional[time] = None
    stops: Optional[time] = None
    updated_at: datetime = datetime.now()

    def serialize(self):
        return {"Mon": self.Mon, "Tue": self.Tue, "Wed": self.Wed, "Thu": self.Thu,
                "Fri": self.Fri, "Sat": self.Sat, "Sun": self.Sun,
                "starts": str(self.starts), "stops": str(self.stops)}


class TimerUpdate(BaseModel):
    Mon: Optional[bool]
    Tue: Optional[bool]
    Wed: Optional[bool]
    Thu: Optional[bool]
    Fri: Optional[bool]
    Sat: Optional[bool]
    Sun: Optional[bool]
    starts: Optional[time]
    stops: Optional[time]
    updated_at: datetime = datetime.now()

    def serialize(self):
        return {"Mon": self.Mon, "Tue": self.Tue, "Wed": self.Wed, "Thu": self.Thu,
                "Fri": self.Fri, "Sat": self.Sat, "Sun": self.Sun,
                "starts": str(self.starts), "stops": str(self.stops)}


class TControl(BaseModel):
    id: int
    updated_at: datetime
    Mon: Union[bool, None] = None
    Tue: Union[bool, None] = None
    Wed: Union[bool, None] = None
    Thu: Union[bool, None] = None
    Fri: Union[bool, None] = None
    Sat: Union[bool, None] = None
    Sun: Union[bool, None] = None
    starts: Union[time, None] = None
    stops: Union[time, None] = None

    class Config:
        orm_mode = True


class TControlWithID(BaseModel):
    detail: str = "New timer was successfully added to shift"
    id: int

    class Config:
        orm_mode = True


class AddShift(BaseModel):
    system_id: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class UpdateShift(BaseModel):
    updated_at: datetime = datetime.now()


class Shifts(BaseModel):
    id: int
    updated_at: datetime
    shifts_sections: List[Section] = []
    shift_timers: List[TControl] = []

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class ShiftsWithID(BaseModel):
    detail: str = "New shift was successfully added to system"
    id: int

    class Config:
        orm_mode = True


class SystemBase(BaseModel):
    name: str
    location: str


class SystemCreate(SystemBase):
    systemID: str
    owner: str


class SystemUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    updated_at: datetime = datetime.now()


class SystemID(BaseModel):
    id: int
    name: str
    location: str
    owner: str

    class Config:
        orm_mode = True


class System(SystemBase):
    id: int
    systemID: str
    owner: str
    created_at: datetime
    updated_at: datetime
    system_pumps: List[Pump] = []
    system_valves: List[Valve] = []
    system_sensors: List[Sensor] = []
    system_shifts: List[Shifts] = []

    class Config:
        orm_mode = True


class LogCreate(BaseModel):
    dev_id: str
    message: str
    disable: bool = False


class Logs(LogCreate):
    date: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class UpdateLog(BaseModel):
    disable: bool = True


class CurrentTime(BaseModel):
    current_time: datetime = datetime.now()

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }
