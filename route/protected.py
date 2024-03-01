from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
import jsonify

from db.database import get_db
from crud.login import get_current_user
from crud import users
from crud import devices
from schema.users import UserUpdate, AdminUserUpdate, UpdateNote, NoteCreate, LostPassword
from schema.devices import SystemCreate, AddPump, AddValve, AddSensor, AddShift, ShiftsWithID, SystemUpdate, UpdatePump, UpdateValve, SensorControler, TControlWithID, SControlWithID, TimerControl, TimerUpdate, UpdateSensor, UpdateShift, UpdateLog, SectionWithID, SectionCreate, SectionUpdate

base_router = APIRouter()

""" CREATEROUTES """
""" Create new system, shift, device """
# Create system(s)


@base_router.post("/systems")
def create_new_system(system: SystemCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    owner = users.get_user(db=db, username=system.owner)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found user in database"
        )
    try:
        system = devices.create_system(db=db, system=system)
        return {"detail": "New system was created successfully"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Create pump(s)


@base_router.post("/pumps")
def create_new_pump(pump: AddPump, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    system = devices.get_system(db=db, system_id=pump.system_id)
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found system in database"
        )
    try:
        devices.create_pump(db=db, pump=pump)
        return {"detail": "New pump was successfully added to system"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Create valve(s)


@base_router.post("/valves")
def create_new_valve(valve: AddValve, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    system = devices.get_system(db=db, system_id=valve.system_id)
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found system in database"
        )
    try:
        devices.create_valve(db=db, valve=valve)
        return {"detail": "New valve was successfully added to system"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Create sensor(s)


@base_router.post("/sensors")
def create_new_sensor(sensor: AddSensor, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    system = devices.get_system(db=db, system_id=sensor.system_id)
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found system in database"
        )
    try:
        devices.create_sensor(db=db, sensor=sensor)
        return {"detail": "New sensor was successfully added to system"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )


# Create shifts
@base_router.post("/shift", response_model=ShiftsWithID)
def create_new_shift(shift: AddShift, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    system = devices.get_system(db=db, system_id=shift.system_id)
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found system in database"
        )
    if current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        new_shift = devices.create_shift(db=db, shift=shift)
        return new_shift
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Create shift's section


@base_router.post("/section", response_model=SectionWithID)
def create_new_shift_section(section: SectionCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    shift = devices.get_shift(db=db, shift_id=section.shift_id)
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found shift in database"
        )
    system = devices.get_system(db=db, system_id=shift.system_id)
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found system in database"
        )
    if current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    available_valves = devices.check_for_valve_in_sections(
        db=db, shift_id=section.shift_id)
    try:
        if section.valve_id in available_valves:
            new_section = devices.create_section(db=db, section=section)
            return new_section
        else:
            return {"detail": "Selected valve is not available. Please try another one."}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Create sensor controler


@base_router.post("/sensorControler", response_model=SControlWithID)
def create_new_sensor_controler(controler: SensorControler, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    sensor_contolers = devices.get_sensor_controlers(
        db=db, section_id=controler.section_id)
    section = devices.get_section(db=db, id=controler.section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found section in database"
        )
    shift = devices.get_shift(db=db, shift_id=section.shift_id)
    system = devices.get_system(db=db, system_id=shift.system_id)
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found system in database"
        )
    if current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    available_sensors = []
    for sensor in system.system_sensors:
        available_sensors.append(sensor.sensor_id)

    sensors = []
    for new_sensor in sensor_contolers:
        sensors.append(new_sensor.sensor_id)
    try:
        if controler.sensor_id in sensors:
            return {"detail": "You have already added this sensor to group."}
        if controler.sensor_id not in available_sensors:
            return {"detail": "There is no such sensor in system. Check device ID."}
        else:
            new_controler = devices.add_new_sensor_controler(
                db=db, scontroler=controler)
            return new_controler
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Create timer controler


@base_router.post("/timer", response_model=TControlWithID)
def create_new_timer(controler: TimerControl, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    check_timers = []
    timers = []
    shift = devices.get_shift(db=db, shift_id=controler.shift_id)

    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found shift in database"
        )
    system = devices.get_system(db=db, system_id=shift.system_id)
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found system in database"
        )
    if current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    system_shifts = []
    for entry in system.system_shifts:
        system_shifts.append(entry)
    for data in system_shifts:
        for timer in data.shift_timers:
            timers.append(timer)

    for timer in timers:
        timer_to_dict = timer.serialize()
        check_timers.append(timer_to_dict)

    # if controler.starts >= controler.stops:
    #     return {"detail": "Start values must be less than stop value."}

    else:
        try:
            for timer in check_timers:
                print("Checking available timers....")
                if devices.do_timers_interfere(timer1=timer, timer2=controler.serialize()):
                    return {"detail": "Timers match each other."}
            new_timer = devices.add_new_timer(db=db, tcontroler=controler)
            return new_timer
        except:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Something went wrong with connection to database"
            )

# Create user alert


@base_router.post("/alert")
def create_new_alert(alert: NoteCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    user = users.get_user(db=db, username=alert.user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found username in database"
        )
    try:
        users.create_alert(db=db, new_alert=alert)
        return {"detail": "New message was successfully sent to user."}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )


""" UPDATEROUTES """
""" Update user, system and device routes """
# Update user by user


@base_router.put("/user/{username}")
def user_self_update(username: str, user: UserUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if current_user.username != username and not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    user_to_update = users.get_user(db=db, username=username)
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found user in database"
        )
    try:
        users.update_user(username=username, db=db, user=user)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Change password by user


@base_router.patch("/change_password/{username}")
def user_change_password(username: str, password: LostPassword, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    user_to_update = users.get_user(db=db, username=username)
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found user in database"
        )
    try:
        users.change_password(db=db, username=username, password=password)
        return {"detail": "Successfully changed password"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Update user by admin


@base_router.put("/admin/{username}")
def user_admin_update(username: str, user: AdminUserUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    user_to_update = users.get_user(db=db, username=username)
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found user in database"
        )
    try:
        users.admin_update_user(db=db, username=username, user=user)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Update system


@base_router.put("/system/{system_id}")
def system_update(system_id: int, to_update: SystemUpdate, db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user)):

    system_to_update = devices.get_system(db=db, system_id=system_id)
    if not system_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found system in database"
        )
    if current_user.username != system_to_update.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.update_system(db=db, system=to_update, system_id=system_id)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Update pump


@base_router.put("/pump/{pump_id}")
def pump_update(pump_id: str, pump_to_update: UpdatePump, db: Session = Depends(get_db),
                current_user: str = Depends(get_current_user)):

    existing_pump = devices.get_pump(db=db, pump_id=pump_id)
    if not existing_pump:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found pump in database"
        )
    system = devices.get_system(db=db, system_id=existing_pump.system_id)
    if current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.update_pump(db=db, pump=pump_to_update, pump_id=pump_id)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Update valve


@base_router.put("/valve/{valve_id}")
def valve_update(valve_id: str, valve_to_update: UpdateValve, db: Session = Depends(get_db),
                 current_user: str = Depends(get_current_user)):

    existing_valve = devices.get_valve(db=db, valve_id=valve_id)
    if not existing_valve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found valve in database"
        )
    system = devices.get_system(db=db, system_id=existing_valve.system_id)
    if current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.update_valve(db=db, valve=valve_to_update, valve_id=valve_id)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )


# Update sensor
@base_router.put("/sensor/{sensor_id}")
def sensor_update(sensor_id: str, sensor_to_update: UpdateSensor, db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user)):

    existing_sensor = devices.get_sensor(db=db, sensor_id=sensor_id)
    if not existing_sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found sensor in database"
        )
    system = devices.get_system(db=db, system_id=existing_sensor.system_id)
    if current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.update_sensor(
            db=db, sensor=sensor_to_update, sensor_id=sensor_id)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Update shift


# @base_router.put("/shift/{shift_id}")
# def shift_update(shift_id: int, shift_to_update: UpdateShift, db: Session = Depends(get_db),
#                  current_user: str = Depends(get_current_user)):

#     existing_shift = devices.get_shift(db=db, shift_id=shift_id)
#     if not existing_shift:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Could not found shift in database"
#         )
#     system = devices.get_system(db=db, system_id=existing_shift.system_id)
#     if current_user.username != system.owner:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You are not authorized to update database"
#         )
#     try:
#         devices.update_shift(
#             db=db, shift=shift_to_update, shift_id=shift_id)

#         return {"detail": "Successfully updated database"}
#     except:
#         raise HTTPException(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#             detail="Something went wrong with connection to database"
#         )


# Update section


@base_router.put("/section/{id}")
def section_update(id: int, section_to_update: SectionUpdate, db: Session = Depends(get_db),
                   current_user: str = Depends(get_current_user)):

    section = devices.get_section(db=db, id=id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found shift in database"
        )
    shift = devices.get_shift(db=db, shift_id=section.shift_id)
    system = devices.get_system(db=db, system_id=shift.system_id)
    if current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    sensor_option = ["AVG", "ONE", "ALL"]
    if section_to_update.stops_at <= section_to_update.starts_at or section_to_update.starts_at < 0 or section_to_update.stops_at > 100:
        return {"detail": "Start values must be less than 100, greater than 0 and start value must be lower than stop value."}
    if section_to_update.sensors_settings not in sensor_option:
        return {"detail": "Select one of options: AVG/ONE/ALL."}
    try:
        devices.change_section(db=db, section=section_to_update, id=id)

        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Update sensor controler


@base_router.patch("/sensorControler/{controler_id}")
def change_sensor_controler_settings(controler_id: int, controler_to_update: SensorControler, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    controler = devices.get_sensor_controler(db=db, id=controler_id)
    if not controler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found controler in database"
        )
    sensor_contolers = devices.get_sensor_controlers(
        db=db, section_id=controler.section_id)
    section = devices.get_section(db=db, id=controler.section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found section in database"
        )
    shift = devices.get_shift(db=db, shift_id=section.shift_id)
    system = devices.get_system(db=db, system_id=shift.system_id)
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found system in database"
        )
    if current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    available_sensors = []
    for sensor in system.system_sensors:
        available_sensors.append(sensor.sensor_id)
    sensors = []
    for new_sensor in sensor_contolers:
        sensors.append(new_sensor.sensor_id)

    if controler_to_update.section_id != section.id:
        return {"detail": "Can't update unproper section ID."}
    elif controler_to_update.sensor_id not in available_sensors:
        return {"detail": "There is no such sensor in system. Please check device ID."}
    else:
        try:
            if controler_to_update.sensor_id in sensors:
                return {"detail": "You have already added this sensor to group."}
            else:
                devices.change_sensor_controler(
                    db=db, scontroler=controler_to_update, id=controler_id)

                return {"detail": "Successfully updated database"}
        except:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Something went wrong with connection to database"
            )


# Update timer shift controler


@base_router.patch("/timer/{id}")
def change_timer_controler_settings(id: int, controler_to_update: TimerUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

    controler = devices.get_timer(db=db, id=id)
    if not controler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found controler in database"
        )
    check_timers = []
    timers = []
    shift = devices.get_shift(db=db, shift_id=controler.shift_id)
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found shift in database"
        )
    system = devices.get_system(db=db, system_id=shift.system_id)
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found system in database"
        )
    if current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )

    system_shifts = []
    for entry in system.system_shifts:
        system_shifts.append(entry)
    for data in system_shifts:
        for timer in data.shift_timers:
            if timer.id != id:
                timers.append(timer)

    for timer in timers:
        timer_to_dict = timer.serialize()
        check_timers.append(timer_to_dict)

    if controler_to_update.starts >= controler_to_update.stops:
        return {"detail": "Start values must be less than stop value."}

    else:
        try:
            for timer in check_timers:
                print("Checking available timers....")
                if devices.do_timers_interfere(timer1=timer, timer2=controler_to_update.serialize()):
                    return {"detail": "Timers match each other."}
            devices.change_timer_settings(
                db=db, tcontroler=controler_to_update, id=id)
            return {"detail": "Successfully updated database"}
        except:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Something went wrong with connection to database"
            )


# Update log route
@base_router.put("/log/{log_id}")
def log_update(log_id: int, log_to_update: UpdateLog, db: Session = Depends(get_db)):
    existing_log = devices.get_log(db=db, log_id=log_id)
    if not existing_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found shift in database"
        )
    try:
        devices.update_log(db=db, log_id=log_id, log=log_to_update)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Update notification route


@base_router.put("/alert/{note_id}")
def read_alert_update(note_id: int, note_to_update: UpdateNote, db: Session = Depends(get_db),
                      current_user: str = Depends(get_current_user)):

    existing_alert = users.user_alert(db=db, note_id=note_id)
    if not existing_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found alert in database"
        )
    user = users.get_user(db=db, username=existing_alert.user)
    if current_user.username != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        users.update_alert(db=db, note=note_to_update, note_id=note_id)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )


""" DELETEROUTES """
# Delete user route


@base_router.delete("/{username}")
def delete_user(username: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    user_to_delete = users.get_user(db=db, username=username)
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found user in database"
        )
    try:
        users.delete_user(username=username, db=db)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Delete system route


@base_router.delete("/system/{system_id}")
def delete_system(system_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    system_to_delete = devices.get_system(db=db, system_id=system_id)
    if not system_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found system in database"
        )
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.delete_system(system_id=system_id, db=db)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Delete pump route


@base_router.delete("/pump/{pump_id}")
def delete_pump(pump_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    pump_to_delete = devices.get_pump(db=db, pump_id=pump_id)
    if not pump_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found pump in database"
        )
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.delete_pump(pump_id=pump_id, db=db)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Delete valve route


@base_router.delete("/valve/{valve_id}")
def delete_valve(valve_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    valve_to_delete = devices.get_valve(db=db, valve_id=valve_id)
    if not valve_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found valve in database"
        )
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.delete_valve(valve_id=valve_id, db=db)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Delete sensor route


@base_router.delete("/sensor/{sensor_id}")
def delete_sensor(sensor_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    sensor_to_delete = devices.get_sensor(db=db, sensor_id=sensor_id)
    if not sensor_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found sensor in database"
        )
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.delete_sensor(sensor_id=sensor_id, db=db)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Delete shift route


@base_router.delete("/shift/{shift_id}")
def delete_shift(shift_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    shift_to_delete = devices.get_shift(db=db, shift_id=shift_id)
    if not shift_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found shift in database"
        )
    system = devices.get_system(db=db, system_id=shift_to_delete.system_id)
    if not current_user.admin and current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.delete_shift(shift_id=shift_id, db=db)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Delete Shift section route


@base_router.delete("/section/{id}")
def delete_shift_section(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    section_to_delete = devices.get_section(db=db, id=id)
    if not section_to_delete:
        return {"detail": f"There is no section with ID: {id}."}

    shift = devices.get_shift(db=db, shift_id=section_to_delete.shift_id)
    system = devices.get_system(db=db, system_id=shift.system_id)

    if not section_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found shift in database"
        )
    if not current_user.admin and current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.delete_section(db=db, id=id)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Delete sensor controler route


@base_router.delete("/sensorControl/{id}")
def delete_sensor_controler(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    controler_to_delete = devices.get_sensor_controler(db=db, id=id)
    if not controler_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no controler with ID: {id}."
        )

    section = devices.get_section(db=db, id=controler_to_delete.section_id)
    shift = devices.get_shift(db=db, shift_id=section.shift_id)
    system = devices.get_system(db=db, system_id=shift.system_id)

    if not current_user.admin and current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.delete_sensor_controler(db=db, id=id)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )


# Delete timer route


@base_router.delete("/timer/{id}")
def delete_timer(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    timer_to_delete = devices.get_timer(db=db, id=id)
    if not timer_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no timer with ID: {id}."
        )

    shift = devices.get_shift(db=db, shift_id=timer_to_delete.shift_id)
    system = devices.get_system(db=db, system_id=shift.system_id)

    if not current_user.admin and current_user.username != system.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        devices.delete_timer(db=db, id=id)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Delete log route


@base_router.delete("/log/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log_to_delete = devices.get_log(db=db, log_id=log_id)
    if not log_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found log in database"
        )
    try:
        devices.delete_log(log_id=log_id, db=db)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Delete subscriber route


@base_router.delete("/subscriber/{subscriber_id}")
def delete_subscriber(subscriber_id: int, db: Session = Depends(get_db)):
    subscriber_to_delete = users.get_subscriber_by_id(db=db, id=subscriber_id)
    if not subscriber_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found log in database"
        )
    try:
        users.delete_subscriber(subscriber_id=subscriber_id, db=db)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )

# Delete notification route


@base_router.delete("/alert/{note_id}")
def delete_alert(note_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    alert_to_delete = users.user_alert(db=db, note_id=note_id)
    if not alert_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found alert in database"
        )
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        users.delete_alert(note_id=note_id, db=db)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )


@base_router.delete("/viewed_alert/{username}")
def delete_all_alerts(username: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    alerts_to_delete = users.user_alerts(db=db, user=username)
    if not alerts_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not found alert in database"
        )
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update database"
        )
    try:
        users.delete_viewed_alerts(db=db, user=username)
        return {"detail": "Successfully updated database"}
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong with connection to database"
        )
