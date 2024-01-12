import hashlib

from esphome import config_validation as cv, automation
from esphome import codegen as cg
from esphome.const import (
    CONF_ID,
    CONF_INITIAL_VALUE,
    CONF_RESTORE_VALUE,
)
from esphome.core import coroutine_with_priority

CODEOWNERS = ["@rfdarter"]
time_picker_ns = cg.esphome_ns.namespace("time_picker")
Time = time_picker_ns.struct("Time");
TimePicker = time_picker_ns.class_("TimePickerComponent", cg.Component)
RestoringTimePicker = time_picker_ns.class_("RestoringTimePickerComponent", cg.Component)

TimePickerTimeSetAction = time_picker_ns.class_("TimePickerTimeSetAction", automation.Action)

CONF_MAX_RESTORE_DATA_LENGTH = "max_restore_data_length"
CONF_INITIAL_VALUE_SEC = "sec"
CONF_INITIAL_VALUE_MIN = "min"
CONF_INITIAL_VALUE_HOUR = "hour"

MULTI_CONF = True
CONFIG_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.declare_id(TimePicker),
        cv.Optional(CONF_INITIAL_VALUE_SEC): cv.int_range(0, 60),
        cv.Optional(CONF_INITIAL_VALUE_MIN): cv.int_range(0, 60),
        cv.Optional(CONF_INITIAL_VALUE_HOUR): cv.int_range(0, 23),
        cv.Optional(CONF_RESTORE_VALUE, default=False): cv.boolean,
    }
).extend(cv.COMPONENT_SCHEMA)


# Run with low priority so that namespaces are registered first
@coroutine_with_priority(-100.0)
async def to_code(config):
    restore = config[CONF_RESTORE_VALUE]
    type = RestoringTimePicker if restore else TimePicker    
    
    initial_value = {
        "second" : 0,
        "minute" : 0,
        "hour" : 0,
    }
     
    turpl_test = [("second", cg.uint8(0)), ("minute", cg.uint8(0)), ("hour", cg.uint8(0))]
    
    if CONF_INITIAL_VALUE_SEC in config:
        initial_value["second"] = cg.uint8(config[CONF_INITIAL_VALUE_SEC])
  
    if CONF_INITIAL_VALUE_MIN in config:
        initial_value["minute"] = cg.uint8(config[CONF_INITIAL_VALUE_MIN])  
 
    if CONF_INITIAL_VALUE_HOUR in config:
        initial_value["hour"] = cg.uint8(config[CONF_INITIAL_VALUE_HOUR])   
    


    rhs = type.new( cg.StructInitializer(Time, *tuple(initial_value.items())) )
    # rhs = cg.StructInitializer(Time)
    glob = cg.Pvariable(config[CONF_ID], rhs, type)
    await cg.register_component(glob, config)

    if restore:
        value = config[CONF_ID].id
        if isinstance(value, str):
            value = value.encode()
        hash_ = int(hashlib.md5(value).hexdigest()[:8], 16)
        cg.add(glob.set_name_hash(hash_))


@automation.register_action(
    "time_picker.set",
    TimePickerTimeSetAction,
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.use_id(TimePicker),
            cv.Required(CONF_INITIAL_VALUE_SEC): cv.int_range(0, 60),
            cv.Required(CONF_INITIAL_VALUE_MIN): cv.int_range(0, 60),
            cv.Required(CONF_INITIAL_VALUE_HOUR): cv.int_range(0, 23),
        }
    ),
)
async def time_picker_set_to_code(config, action_id, template_arg, args):
    full_id, paren = await cg.get_variable_with_full_id(config[CONF_ID])
    
    template_arg = cg.TemplateArguments(full_id.type, *template_arg)
        
    initial_value = {
        "second" : cg.uint8(config[CONF_INITIAL_VALUE_SEC]),
        "minute" : cg.uint8(config[CONF_INITIAL_VALUE_MIN]),
        "hour" : cg.uint8(config[CONF_INITIAL_VALUE_HOUR]),
    }
    
    var = cg.new_Pvariable(action_id, template_arg, paren)
    templ = cg.StructInitializer(Time, *tuple(initial_value.items())) 
    cg.add(var.set_value(templ))
    return var
