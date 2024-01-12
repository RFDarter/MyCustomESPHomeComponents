#pragma once

#include <utility>
#include "esphome/core/entity_base.h"
#include "esphome/core/helpers.h"

namespace esphome {
namespace time_picker {

enum TimePickerMode : uint8_t {
  TIME_PICKER_MODE_AUTO = 0,
};

class TimePickerTraits : public EntityBase_DeviceClass{
 public:
  // Set/get the frontend mode.
  void set_mode(TimePickerMode mode) { this->mode_ = mode; }
  TimePickerMode get_mode() const { return this->mode_; }

 protected:
  TimePickerMode mode_{TIME_PICKER_MODE_AUTO};
};

}  // namespace time_picker
}  // namespace esphome
