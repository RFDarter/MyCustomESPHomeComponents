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

CONF_STRUCT_NAME = "struct_name"

CODEOWNERS = ["@RFDarter"]


MULTI_CONF = True

CONFIG_SCHEMA = cv.Schema(
    {        
        # cv.Required(CONF_STRUCT_NAME): cv.Schema(
        #     {
        #         cv.Required(CONF_ENTRIES): cv.ensure_list(
        #         {
        #             cv.Required(CONF_NAME): cv.string_strict,
        #             cv.Required(CONF_DATATYPE): cv.string_strict,
        #         })
        #     }),
    
        cv.Required(CONF_STRUCT_NAME): cv.string_strict,
        cv.Required(CONF_LAMBDA): cv.templatable(cv.string),

    }
).extend(cv.COMPONENT_SCHEMA)




# Run with low priority so that namespaces are registered first
@coroutine_with_priority(-100.0)
async def to_code(config):
    structName = config[CONF_STRUCT_NAME]

    structCppCode = "\n"
    structCppCode += "namespace esphome {\n"
    structCppCode += "namespace custom_struct {\n"
    structCppCode += "typedef struct "
    structCppCode += structName
    structCppCode += config[CONF_LAMBDA]
    structCppCode += structName
    structCppCode += ";\n"
    structCppCode += "}// namespace custom_struct\n"
    structCppCode += "}// namespace esphome\n"
    structCppCode += "\n"


    cg.add_global(cg.RawExpression(structCppCode) )   
