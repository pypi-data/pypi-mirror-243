import json
from collections.abc import MutableMapping

from loguru import logger


def parse_to_float_if_possible(string):
    result = string
    try:
        result = float(string)
    except Exception as e:
        logger.warning(f"Cannot parse to float [{e}]")
        result = parse_to_bool_if_possible(string)
    finally:
        return result


def parse_to_bool_if_possible(string):
    if string in ["true", "True"]:
        result = True
    else:
        result = string
        logger.warning("Cannot parse to boolean")
    return result


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def format_sensor_data(data):
    try:
        payload = json.loads(data["payload"])
        fields = flatten_dict(payload)
    except json.JSONDecodeError:
        fields = {"value": str(data["payload"].decode("utf-8"))}
    data = {
        "measurement": data["name"],
        "fields": fields
    }
    try:
        data["time"] = int(data["time"])
    except:
        pass

    return data


def simplify_serialized_data(data, measurement=None, field=None, multiplexer=1):
    try:
        simplified_data = {}
        sum_value = 0
        for table in data:
            if measurement is None:
                if table['name'] == "data":
                    simplified_data["name"] = f"{table['measurement']}#{table['field']}"
                    simplified_data["values"] = table["values"]

                    for value in table["values"]:
                        simplified_data["sum"] = None_sum(sum_value, value["value"])
            else:
                if table['measurement'] == measurement and table['field'] == field:
                    if table['name'] == "data":
                        simplified_data["name"] = f"{table['measurement']}#{table['field']}"
                        simplified_data["values"] = table["values"]

                        for value in table["values"]:
                            simplified_data["sum"] = None_sum(sum_value, value["value"])
        if sum_value == 0:
            return {}

        simplified_data["sum"] = simplified_data["sum"] * multiplexer

        return simplified_data
    except Exception as e:
        logger.exception(f"Failed to simplify the data, returning [{e}]")
        return data


def None_sum(*args):
    args = [a for a in args if a is not None]
    return sum(args) if args else None


def combine_simplified_data(data_a, data_b):
    combined_data = {}
    try:
        if data_a is None or data_a == {}:
            if data_b is not None:
                return data_b

        if data_b is None or data_b == {}:
            return data_a

        new_values = []
        for idx, value in enumerate(data_a["values"]):
            new_value = value
            new_value["value"] = None_sum(value["value"], data_b["values"][idx]["value"])
            new_values.append(new_value)

        new_sum = None_sum(data_a["sum"] + data_b["sum"])
        new_name = data_a["name"] + data_b["name"]
        combined_data = {
            "name": new_name,
            "values": new_values,
            "sum": new_sum
        }
    except Exception as e:
        logger.exception(f"Failed to combine data, [{e}]")
    finally:
        return combined_data
