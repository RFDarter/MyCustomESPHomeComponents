#include "template_time_picker.h"
#include "esphome/core/log.h"

namespace esphome {
namespace template_ {

static const char *const TAG = "template.time_picker";

void TemplateTimePicker::setup() {
  if (this->f_.has_value())
    return;

  time_picker::Time value;
  if (!this->restore_value_) {
    value = this->initial_value_;
  } else {
    this->pref_ = global_preferences->make_preference<time_picker::Time>(1944399030U ^ this->get_object_id_hash());
    //this->pref_ = global_preferences->make_preference<time_picker::Time>(sizeof(time_picker::Time), this->get_object_id_hash(), false);
  if (!this->pref_.load(&value)) {
      value = this->initial_value_;
    }
  }
  this->publish_state(value);
}

void TemplateTimePicker::update() {
  if (!this->f_.has_value())
    return;

  auto val = (*this->f_)();
  if (!val.has_value())
    return;

  this->publish_state(*val);
}

void TemplateTimePicker::control(time_picker::Time value) {
  this->set_trigger_->trigger(value);

  if (this->optimistic_)
    this->publish_state(value);

  if (this->restore_value_)
    this->pref_.save(&value);
}
void TemplateTimePicker::dump_config() {
  LOG_TIME_PICKER("", "Template Number", this);
  ESP_LOGCONFIG(TAG, "  Optimistic: %s", YESNO(this->optimistic_));
  LOG_UPDATE_INTERVAL(this);
}

}  // namespace template_
}  // namespace esphome
