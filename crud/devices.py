from sqlalchemy.orm import Session
from datetime import datetime, time
import pandas as pd
import plotly.express as px

from db import models
from schema import devices
from db.database import engine

# Handle system


def get_systems(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.System).offset(skip).limit(limit).all()


def get_system(db: Session, system_id:  int):
    return db.query(models.System).filter(models.System.id == system_id).first()


def get_systemID(db: Session, systemID: str):
    return db.query(models.System).filter(models.System.systemID == systemID).first()


def create_system(db: Session, system: devices.SystemCreate):
    db_system = models.System(**system.dict())
    db.add(db_system)
    db.commit()
    db.refresh(db_system)
    return db_system


def update_system(db: Session, system: devices.SystemUpdate, system_id: int):
    system_query = db.query(models.System).filter(
        models.System.id == system_id)
    if not system_query.first():
        return False
    system_query.update(system.dict(), synchronize_session=False)
    db.commit()
    return True


def delete_system(system_id: int, db: Session):
    existing_system = db.query(models.System).filter(
        models.System.id == system_id)
    if not existing_system.first():
        return False
    existing_system.delete(synchronize_session=False)
    db.commit()
    return True

# Handle pumps


def get_pumps(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Pump).offset(skip).limit(limit).all()


def get_pump(db: Session, pump_id: str):
    return db.query(models.Pump).filter(models.Pump.pump_id == pump_id).first()


def get_system_pumps(db: Session, system_id: int):
    return db.query(models.Pump).filter(models.Pump.system_id == system_id).all()


def create_pump(db: Session, pump: devices.AddPump):
    db_pump = models.Pump(**pump.dict())
    db.add(db_pump)
    db.commit()
    db.refresh(db_pump)
    return db_pump


def update_pump(db: Session, pump: devices.UpdatePump, pump_id: str):
    pump_query = db.query(models.Pump).filter(models.Pump.pump_id == pump_id)
    if not pump_query.first():
        return False
    pump_query.update(pump.dict(), synchronize_session=False)
    db.commit()
    return True


def delete_pump(pump_id: str, db: Session):
    existing_pump = db.query(models.Pump).filter(
        models.Pump.pump_id == pump_id)
    if not existing_pump.first():
        return False
    existing_pump.delete(synchronize_session=False)
    db.commit()
    return True

# Handle Valves


def get_valves(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Valve).offset(skip).limit(limit).all()


def get_valve(db: Session, valve_id: str):
    return db.query(models.Valve).filter(models.Valve.valve_id == valve_id).first()


def get_system_valves(db: Session, system_id: int):
    return db.query(models.Valve).filter(models.Valve.system_id == system_id).all()


def create_valve(db: Session, valve: devices.AddValve):
    db_valve = models.Valve(**valve.dict())
    db.add(db_valve)
    db.commit()
    db.refresh(db_valve)
    return db_valve


def update_valve(db: Session, valve: devices.UpdateValve, valve_id: str):
    valve_query = db.query(models.Valve).filter(
        models.Valve.valve_id == valve_id)
    if not valve_query.first():
        return False
    valve_query.update(valve.dict(), synchronize_session=False)
    db.commit()
    return True


def update_valve_status(db: Session, valve: devices.UpdateValveStatus, valve_id: str):
    valve_query = db.query(models.Valve).filter(
        models.Valve.valve_id == valve_id)
    if not valve_query.first():
        return False
    valve_query.update(valve.dict(), synchronize_session=False)
    db.commit()
    return True


def delete_valve(valve_id: str, db: Session):
    existing_valve = db.query(models.Valve).filter(
        models.Valve.valve_id == valve_id)
    if not existing_valve.first():
        return False
    existing_valve.delete(synchronize_session=False)
    db.commit()
    print(f"Valve {valve_id} was deleted.")
    existing_section = db.query(models.Section).filter(
        models.Section.valve_id == valve_id)
    while existing_section.first():
        existing_section.delete(synchronize_session=False)
        db.commit()
        print(f"Deleting shift section with valveID: {valve_id}...")
    return True


# Handle sensors
def get_sensors(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Sensor).offset(skip).limit(limit).all()


def get_sensor(db: Session, sensor_id: str):
    return db.query(models.Sensor).filter(models.Sensor.sensor_id == sensor_id).first()


def get_system_sensors(db: Session, system_id: int):
    return db.query(models.Sensor).filter(models.Sensor.system_id == system_id).all()


def create_sensor(db: Session, sensor: devices.AddSensor):
    db_sensor = models.Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def update_sensor(db: Session, sensor: devices.UpdateSensor, sensor_id: str):
    sensor_query = db.query(models.Sensor).filter(
        models.Sensor.sensor_id == sensor_id)
    if not sensor_query.first():
        return False
    sensor_query.update(sensor.dict(), synchronize_session=False)
    db.commit()
    return True


def delete_sensor(sensor_id: str, db: Session):
    existing_sensor = db.query(models.Sensor).filter(
        models.Sensor.sensor_id == sensor_id)
    if not existing_sensor.first():
        return False
    existing_sensor.delete(synchronize_session=False)
    db.commit()
    return True

# Handle shifts


def get_shifts(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Shift).offset(skip).limit(limit).all()


def get_shift(db: Session, shift_id: int):
    return db.query(models.Shift).filter(models.Shift.id == shift_id).first()


def get_system_shifts(db: Session, system_id: int):
    return db.query(models.Shift).filter(models.Shift.system_id == system_id).all()


def create_shift(db: Session, shift: devices.AddShift):
    db_shift = models.Shift(**shift.dict())
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift


def delete_shift(shift_id: int, db: Session):
    existing_shift = db.query(models.Shift).filter(models.Shift.id == shift_id)
    if not existing_shift.first():
        print("No shift found!")
        return False
    existing_shift.delete(synchronize_session=False)
    db.commit()
    print(f"Shift {shift_id} was deleted.")
    existing_timer_controler = db.query(models.Timer).filter(
        models.Timer.shift_id == shift_id)
    while existing_timer_controler.first():
        existing_timer_controler.delete(synchronize_session=False)
        db.commit()
        print(f"Deleting timer for shift {shift_id}...")
    return True


def update_shift(db: Session, shift: devices.UpdateShift, shift_id: int):
    shift_query = db.query(models.Shift).filter(models.Shift.id == shift_id)
    if not shift_query.first():
        return False
    shift_query.update(shift.dict(), synchronize_session=False)
    db.commit()
    print(f"Updating shift ID:{shift_id}....")
    return True

# Handle shift's sections and controls


def get_shift_sections(shift_id: int, db: Session):
    return db.query(models.Section).filter(models.Section.shift_id == shift_id).all()


def get_sections(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Section).offset(skip).limit(limit).all()


def get_section(id: int, db: Session):
    return db.query(models.Section).filter(models.Section.id == id).first()


def check_for_valve_in_sections(db: Session, shift_id: int):
    available_valves = []
    system_id = get_shift(db=db, shift_id=shift_id)
    system_valves = get_system_valves(db=db, system_id=system_id.system_id)
    for valve in system_valves:
        available_valves.append(valve.valve_id)
    section_valves = []
    for valve_id in available_valves:
        section_valve = db.query(models.Section).filter(
            models.Section.valve_id == valve_id).first()
        if section_valve:
            section_valves.append(section_valve.valve_id)
    ready_valves = []
    for valve in available_valves:
        if valve not in section_valves:
            ready_valves.append(valve)
    return ready_valves


def create_section(db: Session, section: devices.SectionCreate):
    db_section = models.Section(**section.dict())
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section


def change_section(db: Session, section: devices.SectionUpdate, id: int):
    section_query = db.query(models.Section).filter(
        models.Section.id == id)
    if not section_query.first():
        return False
    section_query.update(section.dict(), synchronize_session=False)
    db.commit()
    return True


def delete_section(id: int, db: Session):
    existing_section = db.query(models.Section).filter(models.Section.id == id)
    if not existing_section.first():
        print(f"No section with ID:{id} has found!")
        return False
    existing_section.delete(synchronize_session=False)
    db.commit()
    print(f"Deleting section ID:{id}...")
    existing_sesor_controler = db.query(models.SensorControler).filter(
        models.SensorControler.section_id == id)
    while existing_sesor_controler.first():
        existing_sesor_controler.delete(synchronize_session=False)
        db.commit()
        print(f"Deleting sensor controlers for section ID:{id}....")
    return True


def get_sensor_controler(id: int, db: Session):
    return db.query(models.SensorControler).filter(
        models.SensorControler.id == id).first()


def get_sensor_controlers(section_id: int, db: Session):
    return db.query(models.SensorControler).filter(
        models.SensorControler.section_id == section_id).all()


def add_new_sensor_controler(db: Session, scontroler: devices.SensorControler):
    db_controler = models.SensorControler(**scontroler.dict())
    db.add(db_controler)
    db.commit()
    db.refresh(db_controler)
    return db_controler


def change_sensor_controler(db: Session, scontroler: devices.SensorControler, id: int):
    controler_query = db.query(models.SensorControler).filter(
        models.SensorControler.id == id)
    if not controler_query.first():
        return False
    controler_query.update(scontroler.dict(), synchronize_session=False)
    db.commit()
    return True


def delete_sensor_controler(id: int, db: Session):
    existing_controler = db.query(models.SensorControler).filter(
        models.SensorControler.id == id)
    if not existing_controler.first():
        return False
    existing_controler.delete(synchronize_session=False)
    db.commit()
    return True


def get_timer(db: Session, id: int):
    return db.query(models.Timer).filter(
        models.Timer.id == id).first()


def get_timers(db: Session, shift_id: int):
    return db.query(models.Timer).filter(models.Timer.shift_id == shift_id).all()


def get_all_timers(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Timer).offset(skip).limit(limit).all()


def add_new_timer(db: Session, tcontroler: devices.TimerControl):
    db_controler = models.Timer(**tcontroler.dict())
    db.add(db_controler)
    db.commit()
    db.refresh(db_controler)
    return db_controler


def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M:%S").time()


def do_timers_interfere(timer1, timer2):
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Check if any of the days in timer1 overlap with timer2
    for day in days_of_week:
        if timer1[day] and timer2[day]:
            start_time1 = parse_time(timer1["starts"])
            stop_time1 = parse_time(timer1["stops"])
            start_time2 = parse_time(timer2["starts"])
            stop_time2 = parse_time(timer2["stops"])

            # Check if the time ranges overlap (taking into account start time equals end time)
            if (
                (start_time1 < stop_time1 and start_time2 < stop_time2 and
                 ((start_time1 <= start_time2 < stop_time1) or
                  (start_time1 < stop_time2 <= stop_time1) or
                  (start_time2 <= start_time1 < stop_time2) or
                  (start_time2 < stop_time1 <= stop_time2))) or
                (start_time1 == stop_time1 and start_time2 == stop_time2 and
                 start_time1 == start_time2)
            ):
                return True
            else:
                return False


def change_timer_settings(db: Session, tcontroler: devices.TimerUpdate, id: int):
    controler_query = db.query(models.Timer).filter(
        models.Timer.id == id)
    if not controler_query.first():
        return False
    controler_query.update(tcontroler.dict(), synchronize_session=False)
    db.commit()
    return True


def delete_timer(id: int, db: Session):
    existing_timer = db.query(models.Timer).filter(models.Timer.id == id)
    if not existing_timer.first():
        return False
    existing_timer.delete(synchronize_session=False)
    db.commit()
    return True


# Handle logs


def get_logs(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Logs).offset(skip).limit(limit).all()


def get_dev_logs(db: Session, dev_id: str):
    return db.query(models.Logs).filter(models.Logs.dev_id == dev_id).all()


def get_log(db: Session, log_id: int):
    return db.query(models.Logs).filter(models.Logs.id == log_id).first()


def create_log(db: Session, log: devices.LogCreate):
    db_log = models.Logs(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def update_log(db: Session, log: devices.UpdateLog, log_id: int):
    log_query = db.query(models.Logs).filter(models.Logs.id == log_id)
    if not log_query.first():
        return False
    log_query.update(log.dict(), synchronize_session=False)
    db.commit()
    return True


def delete_log(log_id: int, db: Session):
    existing_log = db.query(models.Logs).filter(models.Logs.id == log_id)
    if not existing_log.first():
        return False
    existing_log.delete(synchronize_session=False)
    db.commit()
    return True

# Handle flow data


def get_flow_data(db: Session, pump_id: str):
    return db.query(models.FlowData).order_by(models.FlowData.pump_id, models.FlowData.date.desc()).filter(
        models.FlowData.pump_id == pump_id).first()


def get_all_flow_data(db: Session, pump_id: str):
    return db.query(models.FlowData).filter(models.FlowData.pump_id == pump_id)


def create_flow_data(db: Session, flow: devices.AddFlowData):
    db_data = models.FlowData(**flow.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def update_pump_data(db: Session, pump_id: str, current: float):
    query_pump = db.query(models.Pump).filter(models.Pump.pump_id == pump_id)
    if not query_pump.first():
        return False
    query_pump.update({models.Pump.current: current},
                      synchronize_session=False)
    db.commit()
    return True

# Handle sensor data


def get_sensor_data(db: Session, sensor_id: str):
    return db.query(models.SensorData).order_by(models.SensorData.sensor_id, models.SensorData.date.desc()).filter(
        models.SensorData.sensor_id == sensor_id).first()


def get_all_sensor_data(db: Session, sensor_id: str):
    return db.query(models.SensorData).filter(models.SensorData.sensor_id == sensor_id)


def create_sensor_data(db: Session, sensor: devices.AddSensorData):
    db_data = models.SensorData(**sensor.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def update_sensor_data(db: Session, sensor_id: str, readings: float):
    query_readings = db.query(models.Sensor).filter(
        models.Sensor.sensor_id == sensor_id)
    if not query_readings.first():
        return False
    query_readings.update(
        {models.Sensor.readings: readings}, synchronize_session=False)
    db.commit()
    return True


""" Images and figures """


# def create_flow_image(pump_id: str, db: Session):
#     pump_data = get_all_flow_data(db=db, pump_id=pump_id)
#     flow_df = pd.read_sql(sql=pump_data.statement, con=engine)
#     fig = px.bar(flow_df, x="date", y="flow_rate", title="Daily Consumption") 
#     fig.write_image(f"static/images/flowimg/{pump_id}.png")


def show_flow_fig(id: str, db: Session):
    pump_data = get_all_flow_data(db=db, pump_id=id)
    try:
        flow_df = pd.read_sql(sql=pump_data.statement, con=engine)
        fig = px.bar(flow_df, x="date", y="flow_rate", title="Daily Consumption")
        return fig
    except TypeError:
        return 


def show_sensor_fig(id: str, db: Session):
    sensor_data = get_all_sensor_data(db=db, sensor_id=id)
    try:
        sensor_df = pd.read_sql(sql=sensor_data.statement, con=engine)
        fig = px.line(sensor_df, x="date", y=["level_1", "level_2", "level_3"], labels={
        "value": "Moisture (%)",
        "date": "Measurement date",
        "variable": "Measurement"
        }, title="Sensor Readings")
        return fig
    except TypeError:
        return
