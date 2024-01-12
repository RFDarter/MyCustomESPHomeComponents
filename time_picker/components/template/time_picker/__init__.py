from esphome import automation
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import time_picker
from esphome.const import (
    CONF_ID,
    CONF_INITIAL_VALUE,
    CONF_LAMBDA,
    CONF_MAX_VALUE,
    CONF_MIN_VALUE,
    CONF_OPTIMISTIC,
    CONF_RESTORE_VALUE,
    CONF_STEP,
    CONF_SET_ACTION,
)
from .. import template_ns

CONF_INITIAL_VALUE = "initial_value"
CONF_INITIAL_SECOND = "second"
CONF_INITIAL_MINUTE = "minute"
CONF_INITIAL_HOUR = "hour"

CODEOWNERS = ["@rfdarter"]


TemplateTimePicker = template_ns.class_(
    "TemplateTimePicker", time_picker.TimePicker, cg.PollingComponent
)


def validate(config):
    if CONF_LAMBDA in config:
        if config[CONF_OPTIMISTIC]:
            raise cv.Invalid("optimistic cannot be used with lambda")
        if CONF_INITIAL_VALUE in config:
            raise cv.Invalid("initial_value cannot be used with lambda")
        if CONF_RESTORE_VALUE in config:
            raise cv.Invalid("restore_value cannot be used with lambda")
    elif CONF_INITIAL_VALUE not in config:
        turpl_test = [("second", cg.uint8(0)), ("minute", cg.uint8(0)), ("hour", cg.uint8(0))]
        # config[CONF_INITIAL_VALUE][CONF_INITIAL_SECOND] = 0
        # config[CONF_INITIAL_VALUE][CONF_INITIAL_MINUTE] = 0
        # config[CONF_INITIAL_VALUE][CONF_INITIAL_HOUR] = 0

    if not config[CONF_OPTIMISTIC] and CONF_SET_ACTION not in config:
        raise cv.Invalid(
            "Either optimistic mode must be enabled, or set_action must be set, to handle the number being set."
        )
        
    return config

    
CONFIG_SCHEMA = cv.All(
    time_picker.time_picker_schema(TemplateTimePicker)
    .extend(
        {
            cv.Optional(CONF_LAMBDA): cv.returning_lambda,
            cv.Optional(CONF_OPTIMISTIC, default=False): cv.boolean,
            cv.Optional(CONF_SET_ACTION): automation.validate_automation(single=True),
            cv.Optional(CONF_INITIAL_VALUE): cv.Schema({
                cv.Optional(CONF_INITIAL_SECOND, default=0): cv.int_range(min=0, max=59),
                cv.Optional(CONF_INITIAL_MINUTE, default=0): cv.int_range(min=0, max=59),
                cv.Optional(CONF_INITIAL_HOUR, default=0): cv.int_range(min=0, max=23),
            }),
            cv.Optional(CONF_RESTORE_VALUE): cv.boolean,
        }
    )
    .extend(cv.polling_component_schema("60s")),
    validate,
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await time_picker.register_time_picker(
        var,
        config,
    )
    
    if CONF_LAMBDA in config:
        template_ = await cg.process_lambda(
            config[CONF_LAMBDA], [], return_type=cg.optional.template(time_picker.Time)
        )
        cg.add(var.set_template(template_))
    else:    
        cg.add(var.set_optimistic(config[CONF_OPTIMISTIC]))
        
        if CONF_RESTORE_VALUE in config:
            cg.add(var.set_restore_value(config[CONF_RESTORE_VALUE]))

        if CONF_INITIAL_VALUE in config:
            initList = [("second", config[CONF_INITIAL_VALUE][CONF_INITIAL_SECOND]), 
                        ("minute", config[CONF_INITIAL_VALUE][CONF_INITIAL_MINUTE]), 
                        ("hour", config[CONF_INITIAL_VALUE][CONF_INITIAL_HOUR])]      
            tmp = cg.StructInitializer(time_picker.Time, *initList)
            cg.add(var.set_initial_value(tmp) )
            
    if CONF_SET_ACTION in config:
        await automation.build_automation(
            var.get_set_trigger(), [(time_picker.Time, "x")], config[CONF_SET_ACTION]
        )
