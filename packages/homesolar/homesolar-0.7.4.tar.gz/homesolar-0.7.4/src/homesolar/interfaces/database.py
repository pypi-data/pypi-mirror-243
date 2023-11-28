import json
from time import perf_counter

from loguru import logger

# project's imports
from homesolar.services import influxdb
from homesolar.utils import datetime, config, data_formatter
from homesolar.utils import influxdb as influx_utils
from homesolar.utils import sqlite as sqlite_utils
from homesolar.utils.sqlite import SensorData


# Used on All database
async def write_sensor_data(data):
    from homesolar.services import sqlite
    start_time = perf_counter()
    sensor_data = data_formatter.format_sensor_data(data)
    await influxdb.write(sensor_data)
    logger.debug("is it waiting ?")
    mapped_data = sqlite_utils.mapped_for_upsert(sensor_data)
    await sqlite.bulk_upsert_sensors(mapped_data)
    logger.debug(json.dumps(sensor_data))
    logger.debug(f"Time taken for entire sensor_data_write: {perf_counter() - start_time} second(s)")


async def write_sensor_to_influxdb(data):
    await influxdb.write(data_formatter.format_sensor_data(data))


async def write_sensor_to_sqlite(data):
    from homesolar.services import sqlite
    await sqlite.bulk_upsert_sensors(sqlite_utils.mapped_for_upsert(data_formatter.format_sensor_data(data)))


# Used only on InfluxDB
async def get_battery_charge(date):
    flux = influx_utils.generate_flux(
        config.homesolar_config['DATA']['battery_charge_measurement'],
        config.homesolar_config['DATA']['battery_charge_field'],
        datetime.stringify_timestamp(date),
        datetime.get_next_day(date), "DAY"
    )
    result = await influxdb.query(flux)
    logger.debug(result)
    return data_formatter.simplify_serialized_data(influx_utils.serialize(result, "DAY"))


async def get_battery_usage(date, timescale):
    start_time, stop_time = datetime.get_date_pair(date, timescale)
    flux = influx_utils.generate_flux(
        config.homesolar_config['DATA']['battery_power_measurement'],
        config.homesolar_config['DATA']['battery_power_field'],
        start_time,
        stop_time,
        timescale
    )
    result = await influxdb.query(flux)
    logger.debug(result)
    return data_formatter.simplify_serialized_data(influx_utils.serialize(result, timescale))


async def get_solar_production(date, timescale):
    start_time, stop_time = datetime.get_date_pair(date, timescale)
    flux = influx_utils.generate_flux(
        config.homesolar_config['DATA']['solar_production_measurement'],
        config.homesolar_config['DATA']['solar_production_field'],
        start_time,
        stop_time,
        timescale
    )
    result = await influxdb.query(flux)
    logger.debug(result)
    return data_formatter.simplify_serialized_data(influx_utils.serialize(result, timescale))


async def get_grid_usage(date, timescale):
    start_time, stop_time = datetime.get_date_pair(date, timescale)
    flux = influx_utils.generate_flux(
        config.homesolar_config['DATA']['grid_power_measurement'],
        config.homesolar_config['DATA']['grid_power_field'],
        start_time,
        stop_time,
        timescale
    )
    result = await influxdb.query(flux)
    logger.debug(result)
    return data_formatter.simplify_serialized_data(influx_utils.serialize(result, timescale))


async def get_inverter_usage(date, timescale):
    start_time, stop_time = datetime.get_date_pair(date, timescale)
    flux = influx_utils.generate_flux(
        config.homesolar_config['DATA']['inverter_power_measurement'],
        config.homesolar_config['DATA']['inverter_power_field'],
        start_time,
        stop_time,
        timescale
    )
    result = await influxdb.query(flux)
    logger.debug(result)
    return data_formatter.simplify_serialized_data(influx_utils.serialize(result, timescale))


async def get_home_usage(date, timescale):
    start_time, stop_time = datetime.get_date_pair(date, timescale)
    flux = influx_utils.generate_combined_tables_flux(
        [config.homesolar_config['DATA']['grid_power_measurement'],
         config.homesolar_config['DATA']['inverter_power_measurement']],
        [config.homesolar_config['DATA']['grid_power_field'],
         config.homesolar_config['DATA']['inverter_power_field']],
        start_time,
        stop_time,
        timescale
    )
    logger.debug(flux)
    result = await influxdb.query(flux)
    return data_formatter.simplify_serialized_data(influx_utils.serialize(result, timescale))


async def get_chart_data(date, timescale):
    solar_production = await get_solar_production(date, timescale)
    battery_usage = await get_battery_usage(date, timescale)
    grid_usage = await get_grid_usage(date, timescale)
    inverter_usage = await get_inverter_usage(date, timescale)
    home_usage = await get_home_usage(date, timescale)

    if timescale == "DAY":
        battery_charge = await get_battery_charge(date)
    else:
        battery_charge = None

    data = {
        "solar_production": {"name": "solar_production", "values": [], "sum": 0.0} if solar_production == {} else solar_production,
        "battery_usage": {"name": "battery_usage", "values": [], "sum": 0.0} if battery_usage == {} else battery_usage,
        "grid_usage": {"name": "grid_usage", "values": [], "sum": 0.0} if grid_usage == {} else grid_usage,
        "inverter_usage": {"name": "inverter_usage", "values": [], "sum": 0.0} if inverter_usage == {} else inverter_usage,
        "home_usage": {"name": "home_usage", "values": [], "sum": 0.0} if home_usage == {} else home_usage,
        "battery_charge": {"name": "battery_charge", "values": [], "sum": 0.0} if battery_charge == {} else battery_charge
    }
    return data


async def get_measurements(bucket=None):
    flux = influx_utils.generate_measurements_flux(bucket)
    tables = await influxdb.query(flux)
    measurements = [row.values["_value"] for table in tables for row in table]

    logger.debug(f"Measurements: {measurements}")
    return measurements


async def get_fields(measurement, bucket=None):
    flux = influx_utils.generate_fields_flux(measurement, bucket)
    tables = await influxdb.query(flux)
    fields = [row.values["_value"] for table in tables for row in table]

    logger.debug(f"Fields: {fields}")
    return fields


async def get_configurations():
    configurations = []
    measurements = await get_measurements()
    logger.debug(measurements)
    for measurement in measurements:
        fields = await get_fields(measurement)
        configuration = {"measurement": measurement, "fields": fields}
        configurations.append(configuration)

    return configurations


# Used only on Sqlite
async def get_sensor_data(measurement, field):
    from homesolar.services import sqlite
    sensor_data = await sqlite.query(SensorData, SensorData.name.in_([f"{measurement}#{field}"]))
    if sensor_data is None:
        logger.warning("No sensor data with specified name found")
        return None
    else:
        for sensor in sensor_data:
            return data_formatter.parse_to_float_if_possible(sensor.value)


class InfluxInterface:
    @staticmethod
    def get_chart_data(date, timescale):
        pass

    @staticmethod
    def generate_flux(measurement, field, start_time, end_time, timescale, bucket=None, timezone=None, number=0):
        if bucket is None:
            bucket = config.homesolar_config['INFLUXDB']['default_bucket']

        if timezone is None:
            timezone = config.homesolar_config['INFLUXDB']['timezone']

        data_query = ""
        additional_query = ""
        yield_str = '''
|> aggregateWindow (every:1m, fn: mean, createEmpty: false)
|> toFloat()
|> aggregateWindow(every: 1h, fn: sum, createEmpty: false)
|> map(fn: (r) => ({r with _value: r._value/60.0}))
'''

        if timescale == "DAY":
            yield_str = '''
|> aggregateWindow (every:10s, fn: mean, createEmpty: false)
|> toFloat()
|> aggregateWindow(every: 5m, fn: sum, createEmpty: true)
|> map(fn: (r) => ({r with _value: r._value/30.0}))
'''
            yield_str += f' |> yield(name: "{measurement}_{field}")'
            data_query = '''
|> aggregateWindow(every: 1h, fn: sum, createEmpty: false)
|> map(fn: (r) => ({r with _value: r._value/12.0}))
'''
        elif timescale == "MONTH":
            additional_query = f'''
formattedData{number} = data
|> aggregateWindow(every: 1d, fn: sum, createEmpty: true)
|> yield(name: "{measurement}_{field}")
'''
        elif timescale == "YEAR":
            additional_query = f'''
formattedData{number} = data
|> aggregateWindow(every: 1mo, fn: sum, createEmpty: true)
|> yield(name: "{measurement}_{field}")
'''

        result = ""

        if number == 0:
            result += f'''
import "timezone"
option location = timezone.location(name: "{timezone}")
'''
        result += f'''
rawData{number} = from(bucket: "{bucket}")
|> range(start: {start_time}, stop: {end_time})
|> filter(fn: (r) => r["_measurement"] == "{measurement}")
|> filter(fn: (r) => r["_field"] == "{field}")
{yield_str}

data{number} = rawData{number}
{data_query}

{additional_query}

sum{number} = data{number}
|> sum()
|> yield(name: "sum_{number}")
'''
        logger.debug(result)
        return result
