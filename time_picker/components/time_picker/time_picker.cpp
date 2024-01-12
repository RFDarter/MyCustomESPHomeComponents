#include "time_picker.h"
#include "esphome/core/log.h"

namespace esphome {
namespace time_picker {

static const char *const TAG = "time_picker";

void TimePicker::publish_state(Time state) {
  this->has_state_ = true;
  this->state = state;
  ESP_LOGD(TAG, "'%s': Sending state %s", this->get_name().c_str(), state.toString().c_str());
  this->state_callback_.call(state);
}

void TimePicker::add_on_state_callback(std::function<void(Time)> &&callback) {
  this->state_callback_.add(std::move(callback));
}

}  // namespace number
}  // namespace esphome
