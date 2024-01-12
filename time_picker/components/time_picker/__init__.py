import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.components import mqtt
from esphome.const import (
    CONF_INTERNAL,
    CONF_ABOVE,
    CONF_BELOW,
    CONF_DEVICE_CLASS,
    CONF_ENTITY_CATEGORY,
    CONF_ID,
    CONF_ICON,
    CONF_MODE,
    CONF_ON_VALUE,
    CONF_ON_VALUE_RANGE,
    CONF_TRIGGER_ID,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_MQTT_ID,
    CONF_VALUE,
    CONF_OPERATION,
    CONF_CYCLE,
    DEVICE_CLASS_APPARENT_POWER,
    DEVICE_CLASS_AQI,
    DEVICE_CLASS_ATMOSPHERIC_PRESSURE,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_CARBON_DIOXIDE,
    DEVICE_CLASS_CARBON_MONOXIDE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_DATA_RATE,
    DEVICE_CLASS_DATA_SIZE,
    DEVICE_CLASS_DISTANCE,
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_EMPTY,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_ENERGY_STORAGE,
    DEVICE_CLASS_FREQUENCY,
    DEVICE_CLASS_GAS,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_IRRADIANCE,
    DEVICE_CLASS_MOISTURE,
    DEVICE_CLASS_MONETARY,
    DEVICE_CLASS_NITROGEN_DIOXIDE,
    DEVICE_CLASS_NITROGEN_MONOXIDE,
    DEVICE_CLASS_NITROUS_OXIDE,
    DEVICE_CLASS_OZONE,
    DEVICE_CLASS_PH,
    DEVICE_CLASS_PM1,
    DEVICE_CLASS_PM10,
    DEVICE_CLASS_PM25,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_POWER_FACTOR,
    DEVICE_CLASS_PRECIPITATION,
    DEVICE_CLASS_PRECIPITATION_INTENSITY,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_REACTIVE_POWER,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_SOUND_PRESSURE,
    DEVICE_CLASS_SPEED,
    DEVICE_CLASS_SULPHUR_DIOXIDE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS,
    DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS_PARTS,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_VOLUME,
    DEVICE_CLASS_VOLUME_STORAGE,
    DEVICE_CLASS_WATER,
    DEVICE_CLASS_WEIGHT,
    DEVICE_CLASS_WIND_SPEED,
)
from esphome.core import CORE, coroutine_with_priority
from esphome.cpp_helpers import setup_entity
from esphome.cpp_generator import MockObjClass

CODEOWNERS = ["@rfdarter"]

DEVICE_CLASSES = [
    DEVICE_CLASS_APPARENT_POWER,
    DEVICE_CLASS_AQI,
    DEVICE_CLASS_ATMOSPHERIC_PRESSURE,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_CARBON_DIOXIDE,
    DEVICE_CLASS_CARBON_MONOXIDE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_DATA_RATE,
    DEVICE_CLASS_DATA_SIZE,
    DEVICE_CLASS_DISTANCE,
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_EMPTY,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_ENERGY_STORAGE,
    DEVICE_CLASS_FREQUENCY,
    DEVICE_CLASS_GAS,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_IRRADIANCE,
    DEVICE_CLASS_MOISTURE,
    DEVICE_CLASS_MONETARY,
    DEVICE_CLASS_NITROGEN_DIOXIDE,
    DEVICE_CLASS_NITROGEN_MONOXIDE,
    DEVICE_CLASS_NITROUS_OXIDE,
    DEVICE_CLASS_OZONE,
    DEVICE_CLASS_PH,
    DEVICE_CLASS_PM1,
    DEVICE_CLASS_PM10,
    DEVICE_CLASS_PM25,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_POWER_FACTOR,
    DEVICE_CLASS_PRECIPITATION,
    DEVICE_CLASS_PRECIPITATION_INTENSITY,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_REACTIVE_POWER,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_SOUND_PRESSURE,
    DEVICE_CLASS_SPEED,
    DEVICE_CLASS_SULPHUR_DIOXIDE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS,
    DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS_PARTS,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_VOLUME,
    DEVICE_CLASS_VOLUME_STORAGE,
    DEVICE_CLASS_WATER,
    DEVICE_CLASS_WEIGHT,
    DEVICE_CLASS_WIND_SPEED,
]
IS_PLATFORM_COMPONENT = True

time_picker_ns = cg.esphome_ns.namespace("time_picker")
Time = time_picker_ns.struct("Time")
TimePicker = time_picker_ns.class_("TimePicker", cg.EntityBase)
TimePickerPtr = time_picker_ns.operator("ptr")

# Triggers
TimePickerStateTrigger = time_picker_ns.class_(
    "TimePickerStateTrigger", automation.Trigger.template(Time)
)

# Actions
TimePickerSetAction = time_picker_ns.class_("TimePickerSetAction", automation.Action)

TimePickerMode = time_picker_ns.enum("TimePickerMode")

TIME_PICKER_MODES = {
    "AUTO": TimePickerMode.TIME_PICKER_MODE_AUTO,
}

validate_device_class = cv.one_of(*DEVICE_CLASSES, lower=True, space="_")

TIME_PICKER_SCHEMA = cv.ENTITY_BASE_SCHEMA.extend(cv.MQTT_COMMAND_COMPONENT_SCHEMA).extend(
    {
        cv.OnlyWith(CONF_MQTT_ID, "mqtt"): cv.declare_id(mqtt.MQTTTextSensor),
        cv.Optional(CONF_ON_VALUE): automation.validate_automation(
            {
                cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(TimePickerStateTrigger),
            }
        ),
        cv.Optional(CONF_MODE, default="AUTO"): cv.enum(TIME_PICKER_MODES, upper=True),
        cv.Optional(CONF_DEVICE_CLASS): validate_device_class,
    }
)

_UNDEF = object()


def time_picker_schema(
    class_: MockObjClass,
    *,
    icon: str = _UNDEF,
    entity_category: str = _UNDEF,
    device_class: str = _UNDEF,
) -> cv.Schema:
    schema = {cv.GenerateID(): cv.declare_id(class_)}

    for key, default, validator in [
        (CONF_ICON, icon, cv.icon),
        (CONF_ENTITY_CATEGORY, entity_category, cv.entity_category),
        (CONF_DEVICE_CLASS, device_class, validate_device_class),
    ]:
        if default is not _UNDEF:
            schema[cv.Optional(key, default=default)] = validator

    return TIME_PICKER_SCHEMA.extend(schema)


async def setup_time_picker_core_(var, config):
    await setup_entity(var, config)

    cg.add(var.set_internal(False))
    cg.add(var.traits.set_mode(config[CONF_MODE]))

    for conf in config.get(CONF_ON_VALUE, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [(Time, "x")], conf)
    if CONF_MQTT_ID in config:
        mqtt_ = cg.new_Pvariable(config[CONF_MQTT_ID], var)
        await mqtt.register_mqtt_component(mqtt_, config)
    if CONF_DEVICE_CLASS in config:
        cg.add(var.traits.set_device_class(config[CONF_DEVICE_CLASS]))


async def register_time_picker(var, config):
    if not CORE.has_id(config[CONF_ID]):
        var = cg.Pvariable(config[CONF_ID], var)
    # cg.add(cg.App.register_component(var))
    if CONF_INTERNAL in config:
        cg.add(cg.RawExpression(str(config)) )
    await setup_time_picker_core_(var, config)


async def new_time_picker(config, *args):
    var = cg.new_Pvariable(config[CONF_ID], *args)
    await register_time_picker(var, config)
    return var


@coroutine_with_priority(40.0)
async def to_code(config):
    cg.add_define("USE_TIME_PICKER")
    cg.add_global(time_picker_ns.using)


OPERATION_BASE_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.use_id(TimePicker),
    }
)


@automation.register_action(
    "time_picker.set",
    TimePickerSetAction,
    OPERATION_BASE_SCHEMA.extend(
        {
            cv.Required(CONF_VALUE): cv.templatable(cv.float_),
        }
    ),
)

async def time_picker_set_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config[CONF_VALUE], args, Time)
    cg.add(var.set_value(template_))
    return var
