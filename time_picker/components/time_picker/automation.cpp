#include "automation.h"
#include "esphome/core/log.h"

namespace esphome {
namespace time_picker {

static const char *const TAG = "time_picker.automation";

union convert {
  float from;
  uint32_t to;
};

}  // namespace time_picker
}  // namespace esphome
