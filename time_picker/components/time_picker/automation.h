#pragma once

#include "time_picker.h"
#include "esphome/core/automation.h"
#include "esphome/core/component.h"

namespace esphome {
namespace time_picker {

class TimePickerStateTrigger : public Trigger<time_picker::Time> {
 public:
  explicit TimePickerStateTrigger(TimePicker *parent) {
    parent->add_on_state_callback([this](time_picker::Time value) { this->trigger(value); });
  }
};

template<typename... Ts> class TimePickerSetAction : public Action<Ts...> {
 public:
  TimePickerSetAction(TimePicker *time) : time_(time) {}
  TEMPLATABLE_VALUE(time_picker::Time, value)

  void play(Ts... x) override {
    auto call = this->time_->make_call();
    call.set_value(this->value_.value(x...));
    call.perform();
  }

 protected:
 TimePicker *time_;
};

}  // namespace time_picker
}  // namespace esphome
