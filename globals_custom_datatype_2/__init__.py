import hashlib

from esphome import config_validation as cv, automation
from esphome import codegen as cg
from esphome.const import (
    CONF_ID,
    CONF_INITIAL_VALUE,
    CONF_RESTORE_VALUE,
    CONF_TYPE,
    CONF_VALUE,
    CONF_NAME,
    CONF_LAMBDA
)
from esphome.core import coroutine_with_priority

CODEOWNERS = ["@RFDarter"]


globals_ns = cg.esphome_ns.namespace("globals")
globalsCustomDatatype_ns = cg.esphome_ns.namespace("globals_custom_datatype")
GlobalsComponent = globals_ns.class_("GlobalsComponent", cg.Component)
RestoringGlobalsComponent = globals_ns.class_("RestoringGlobalsComponent", cg.Component)
RestoringGlobalStringComponent = globals_ns.class_(
    "RestoringGlobalStringComponent", cg.Component
)
GlobalVarSetAction = globals_ns.class_("GlobalVarSetAction", automation.Action)

CONF_MAX_RESTORE_DATA_LENGTH = "max_restore_data_length"


MULTI_CONF = True
CONFIG_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.declare_id(GlobalsComponent),
        cv.Optional(CONF_INITIAL_VALUE): cv.string_strict,
        cv.Optional(CONF_RESTORE_VALUE, default=False): cv.boolean,
        cv.Optional(CONF_MAX_RESTORE_DATA_LENGTH): cv.int_range(0, 254),
        cv.Required(CONF_NAME): cv.string_strict,
        cv.Required(CONF_LAMBDA): cv.templatable(cv.string),
    }
).extend(cv.COMPONENT_SCHEMA)


# Run with low priority so that namespaces are registered first
@coroutine_with_priority(-100.0)
async def to_code(config):
    type_ = cg.RawExpression(config[CONF_NAME])
    restore = config[CONF_RESTORE_VALUE]


    structCppCode = "\n"
    structCppCode += config[CONF_LAMBDA]
    structCppCode += "\n"

    cg.add_global(cg.RawExpression(structCppCode) )   

    template_args = cg.TemplateArguments(type_)
    type = RestoringGlobalsComponent if restore else GlobalsComponent

    res_type = type.template(template_args)
    initial_value = None
    if CONF_INITIAL_VALUE in config:
        initial_value = cg.RawExpression(config[CONF_INITIAL_VALUE])

    rhs = type.new(template_args, initial_value)
    glob = cg.Pvariable(config[CONF_ID], rhs, res_type)
    await cg.register_component(glob, config)

    if restore:
        value = config[CONF_ID].id
        if isinstance(value, str):
            value = value.encode()
        hash_ = int(hashlib.md5(value).hexdigest()[:8], 16)
        cg.add(glob.set_name_hash(hash_))


@automation.register_action(
    "globals.set",
    GlobalVarSetAction,
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.use_id(GlobalsComponent),
            cv.Required(CONF_VALUE): cv.templatable(cv.string_strict),
        }
    ),
)
async def globals_set_to_code(config, action_id, template_arg, args):
    full_id, paren = await cg.get_variable_with_full_id(config[CONF_ID])
    template_arg = cg.TemplateArguments(full_id.type, *template_arg)
    var = cg.new_Pvariable(action_id, template_arg, paren)
    templ = await cg.templatable(
        config[CONF_VALUE], args, None, to_exp=cg.RawExpression
    )
    cg.add(var.set_value(templ))
    return var