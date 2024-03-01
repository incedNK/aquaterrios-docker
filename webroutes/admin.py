from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import plotly


from schema.users import User
from crud import devices
from crud.login import get_current_user
from crud.users import get_users, alerts, get_subscribers
from db.database import get_db


web_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@web_router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@web_router.get("/reset", response_class=HTMLResponse)
def reset_password(request: Request):
    return templates.TemplateResponse("reset.html", {"request": request})


@web_router.get("/get_key", response_class=HTMLResponse)
def reset_password(request: Request):
    return templates.TemplateResponse("get_key.html", {"request": request})


@web_router.get("/profile", response_model=User)
def current_user(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user = current_user
    alerts = []
    for alert in current_user.alerts:
        if not alert.read:
            alerts.append(alert)
    users = get_users(db=db)
    if not current_user:
        return {"detail": "You are not logged in"}
    return templates.TemplateResponse("profile.html", {"request": request, "current_user": current_user, "alerts": alerts, "users": users})


@web_router.get("/flow/{id}")
def get_flow_figures(id: str, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = current_user
    alerts = []
    for alert in current_user.alerts:
        if not alert.read:
            alerts.append(alert)
    users = get_users(db=db)
    data = devices.show_flow_fig(id=id, db=db)
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return templates.TemplateResponse("fig.html", {"request": request, "graphJSON": graphJSON, "current_user": user,
                                                   "alerts": alerts, "users": users})


@web_router.get("/sensor/{id}")
def get_flow_figures(id: str, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = current_user
    alerts = []
    for alert in current_user.alerts:
        if not alert.read:
            alerts.append(alert)
    users = get_users(db=db)
    data = devices.show_sensor_fig(id=id, db=db)
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return templates.TemplateResponse("fig.html", {"request": request, "graphJSON": graphJSON, "current_user": user,
                                                   "alerts": alerts, "users": users})


@web_router.get("/systems")
def admin_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    if not current_user:
        return {"detail": "You are not logged in"}
    if not current_user.admin:
        return {"detali": "You are not authorized"}
    systems = devices.get_systems(db=db)
    return templates.TemplateResponse("systems.html", {"request": request, "systems": systems, "current_user": current_user,
                                                       "users": users})


@web_router.get("/pumps")
def admin_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    if not current_user:
        return {"detail": "You are not logged in"}
    if not current_user.admin:
        return {"detali": "You are not authorized"}
    systems = devices.get_systems(db=db)
    pumps = devices.get_pumps(db=db)
    return templates.TemplateResponse("pumps.html", {"request": request, "systems": systems, "pumps": pumps, "current_user": current_user,
                                                     "users": users})


@web_router.get("/valves")
def admin_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    if not current_user:
        return {"detail": "You are not logged in"}
    if not current_user.admin:
        return {"detali": "You are not authorized"}
    systems = devices.get_systems(db=db)
    valves = devices.get_valves(db=db)
    sections = devices.get_sections(db=db)
    return templates.TemplateResponse("valves.html", {"request": request, "systems": systems, "sections": sections,
                                                      "valves": valves, "current_user": current_user, "users": users})


@web_router.get("/sensors")
def admin_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    sensor_data = []
    if not current_user:
        return {"detail": "You are not logged in"}
    if not current_user.admin:
        return {"detali": "You are not authorized"}
    systems = devices.get_systems(db=db)
    sensors = devices.get_sensors(db=db)
    for sensor in sensors:
        data = devices.get_sensor_data(db=db, sensor_id=sensor.sensor_id)
        sensor_data.append(data)

    return templates.TemplateResponse("sensors.html", {"request": request, "systems": systems, "sensors": sensors,
                                                       "current_user": current_user, "users": users, "sensor_data": sensor_data})


@web_router.get("/logs")
def admin_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    if not current_user:
        return {"detail": "You are not logged in"}
    if not current_user.admin:
        return {"detali": "You are not authorized"}
    logs = devices.get_logs(db=db)
    notifications = alerts(db=db)
    subsctiptions = get_subscribers(db=db)
    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs, "alerts": notifications,
                                                    "subscriptions": subsctiptions, "current_user": current_user, "users": users})


@web_router.get("/system/{id}")
def system(id: int, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db=db)
    alerts = []
    for alert in current_user.alerts:
        if not alert.read:
            alerts.append(alert)
    pump_logs = []
    valve_logs = []
    sensor_logs = []
    red_sensors = []
    green_sensors = []
    blue_sensors = []
    sensor_data = []
    pump_flow_rate = []
    pump_flow_date = []
    controlers = []
    used_valves = []
    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    levels = [{"set_lvl_1": "Measure at 10 cm",
               "set_lvl_2": "Measure at 20 cm", "set_lvl_3": "Measure at 40 cm"}]

    if not current_user:
        return {"detail": "You are not logged in"}
    system = devices.get_system(db=db, system_id=id)
    for sensor in system.system_sensors:
        if sensor.readings < 50:
            red_sensors.append(sensor)
        elif sensor.readings >= 50 and sensor.readings < 80:
            green_sensors.append(sensor)
        else:
            blue_sensors.append(sensor)
    if current_user.username != system.owner and not current_user.admin:
        return {"detail": "You are not authorized"}
    for pump in system.system_pumps:
        flow_data = devices.get_all_flow_data(
            db=db, pump_id=pump.pump_id).all()
        for data in flow_data:
            pump_flow_rate.append(data.flow_rate)
            pump_flow_date.append(data.date.strftime('%d-%m-%Y'))
        if len(pump_flow_rate) > 7:
            pump_flow_rate = pump_flow_rate[-7:]
        if len(pump_flow_date) > 7:
            pump_flow_date = pump_flow_date[-7:]
        pumps_logs = devices.get_dev_logs(db=db, dev_id=pump.pump_id)
        for pump_log in pumps_logs:
            pump_logs.append(pump_log)
    for valve in system.system_valves:
        valves_logs = devices.get_dev_logs(db=db, dev_id=valve.valve_id)
        for valve_log in valves_logs:
            valve_logs.append(valve_log)
    for sensor in system.system_sensors:
        sensors_logs = devices.get_dev_logs(db=db, dev_id=sensor.sensor_id)
        for sensor_log in sensors_logs:
            sensor_logs.append(sensor_log)
    for sensor in system.system_sensors:
        data = devices.get_sensor_data(db=db, sensor_id=sensor.sensor_id)
        sensor_data.append(data)

    for shift in system.system_shifts:
        for section in shift.shifts_sections:
            used_valves.append(section.valve_id)
            for controler in section.section_sensors:
                controlers.append(controler)

    return templates.TemplateResponse("system.html", {"request": request, "system": system, "pump_logs": pump_logs, "valve_logs": valve_logs,
                                                      "sensor_logs": sensor_logs, "current_user": current_user, "alerts": alerts, "red_sensors": red_sensors,
                                                      "green_sensors": green_sensors, "blue_sensors": blue_sensors, "sensor_data": sensor_data, "levels": levels,
                                                      "users": users, "controlers": controlers, "used_valves": used_valves, "week_days": week_days, "pump_flow": json.dumps(pump_flow_rate),
                                                      "pump_date": json.dumps(pump_flow_date)})
