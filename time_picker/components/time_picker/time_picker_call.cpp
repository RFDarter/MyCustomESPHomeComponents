#include "time_picker_call.h"
#include "esphome/core/log.h"
#include "time_picker.h"

namespace esphome {
namespace time_picker {

static const char *const TAG = "time_picker";

TimePickerCall &TimePickerCall::set_value(const Time &value) {
  this->value_ = value;
  return *this;
}

void TimePickerCall::validate_() {
  const auto *name = this->parent_->get_name().c_str();

  if (!this->value_.has_value()) {
    ESP_LOGW(TAG, "'%s' - No value set for TimePickerCall", name);
    return;
  }
}

void TimePickerCall::perform() {
  this->validate_();
  if (!this->value_.has_value()) {
    ESP_LOGW(TAG, "'%s' - No value set for TimePickerCall", this->parent_->get_name().c_str());
    return;
  }
  Time target_value = this->value_.value();

  ESP_LOGD(TAG, "'%s' - Setting time value: %s", this->parent_->get_name().c_str(), target_value.toString().c_str());

  this->parent_->control(target_value);
}

}  // namespace time_picker
}  // namespace esphome
