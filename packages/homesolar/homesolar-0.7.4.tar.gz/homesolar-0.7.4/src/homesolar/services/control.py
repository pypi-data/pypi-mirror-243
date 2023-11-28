import json
import time

from loguru import logger

from homesolar.utils.sqlite import Condition, SensorData, Parameter, Action


def control_loop(timeout):
    logger.debug("Controls Started")
    create_dummy_data()
    try:
        elapsed_time = 0
        while True:
            if time.perf_counter() - elapsed_time >= timeout:
                elapsed_time = time.perf_counter()
                loop()
                logger.debug("Controls Checked")
    except Exception as e:
        logger.exception(f"Something went wrong when looping through controls [{e}]")


def check_controls():
    conditions = get_conditions()
    for condition in conditions:
        if check_parameters(condition.parameters):
            for action in condition.actions:
                do_action(action)


def check_parameters(parameters):
    results = []
    for parameter in parameters:
        value1 = parse_to_float(parameter.value)
        value2 = parse_to_float(get_sensor_data(parameter.name))
        results.append(compare_values(parameter.operator, value1, value2))

    result = results[0]
    for idx, parameter in enumerate(parameters):
        if idx == len(results):
            break
        # AND
        if parameter.logic == 1:
            result = result and results[idx + 1]
        # OR
        if parameter.logic == 2:
            result = result or results[idx + 1]

    return result


def do_action(action):
    value = json.loads(action.value)
    if value["type"] == "MQTT":
        task = {
            "name": "publish",
            "topic": value["topic"],
            "payload": value["payload"]
        }
        logger.debug(task)
        return
    if value["type"] == "GPIO":
        task = {
            "name": "gpio",
            "value": value["payload"]
        }
        logger.debug(task)
        return
    return


def get_conditions():
    return []


def get_sensor_data(sensor_name):
    return 0


def parse_to_float(value):
    try:
        return float(value)
    except:
        return value


def compare_values(operator, value1, value2):
    # Equals
    if operator == 1:
        if value1 == value2:
            return True
    # Not Equals
    if operator == 2:
        if value1 != value2:
            return True
    # Greater
    if operator == 3:
        if value1 > value2:
            return True
    # Less
    if operator == 4:
        if value1 < value2:
            return True
    # Greater or Equals
    if operator == 5:
        if value1 >= value2:
            return True
    # Less or Equals
    if operator == 6:
        if value1 <= value2:
            return True

    return False


def create_dummy_data():
    from homesolar.services.sqlite import sqlite_session
    with sqlite_session() as session:
        param_a = Parameter(name="TasmotaSolar#Power", operator=2, value="2000asdasd00", logic=1)
        param_b = Parameter(name="TasmotaSolar#Power", operator=2, value="1000", logic=2)
        param_c = Parameter(name="BMS#Power", operator=2, value="1000", logic=1)
        param_d = Parameter(name="BMS#Power", operator=2, value="2000", logic=2)
        param_e = Parameter(name="BMS#Power", operator=2, value="2000", logic=-1)

        action_a = Action(value="Turn On")
        action_b = Action(value="Turn OFF")
        action_c = Action(value="Toggle")

        session.add_all([param_a, param_b, param_c, param_d, param_e, action_a, action_b, action_c])
        session.commit()

        condition_a = Condition(
            name="ConditionA",
            description="Condition A Description",
            parameters=[
                param_a, param_b, param_c, param_d, param_e
            ],
            actions=[
                action_a, action_b, action_c
            ]
        )

        session.add_all([condition_a])
        session.commit()


def loop():
    from homesolar.services.sqlite import sqlite_session
    while True:
        with sqlite_session() as session:
            conditions = session.query(Condition)
            logger.debug(conditions)
            for condition in conditions:
                condition_resolve = ""
                for parameter in condition.parameters:
                    data = session.query(SensorData).filter(SensorData.name.in_([str(parameter.name)]))
                    if data:
                        condition_resolve += str(
                            compare(try_parse_to_float(data.value), try_parse_to_float(parameter.value),
                                    parameter.operator))
                    else:
                        condition_resolve += "False"
                    if parameter.logic != -1:
                        condition_resolve += f" {parameter.logic} "
                    else:
                        break

            break


def resolve_condition(resolve: str) -> bool:
    items = resolve.split(" ")

    result = False
    operator = -1
    for index, item in enumerate(items):
        parsed_item = parse_resolve_item(item)

        if index == 0:
            result = parsed_item
        elif parsed_item == 1:
            operator = parsed_item
        elif parsed_item == 2:
            operator = parsed_item
        elif operator != "":
            if operator == 1:
                result = result and parsed_item
            else:
                result = result or parsed_item

    logger.debug(f"({resolve}) resolved as", result)
    return result


def parse_resolve_item(item: str) -> any:
    if item == "True":
        return True
    elif item == "False":
        return False
    return item


def try_parse_to_float(value: any) -> any:
    try:
        return float(value)
    except ValueError:
        return value


def compare(v1: any, v2: any, operator: int) -> bool:
    if not isinstance(v1, type(v2)):
        return False

    if operator == 1:
        if v1 > v2:
            return True
    elif operator == 2:
        if v1 >= v2:
            return True
    elif operator == 3:
        if v1 < v2:
            return True
    elif operator == 4:
        if v1 <= v2:
            return True
    elif operator == 5:
        if v1 == v2:
            return True
    elif operator == 6:
        if v1 != v2:
            return True
    return False
