#pragma once

#include "../../time_picker/time_picker.h"
#include "esphome/core/automation.h"
#include "esphome/core/component.h"
#include "esphome/core/preferences.h"

namespace esphome {
namespace template_ {

class TemplateTimePicker : public time_picker::TimePicker, public PollingComponent {
 public:
  void set_template(std::function<optional<time_picker::Time>()> &&f) { this->f_ = f; }

  void setup() override;
  void update() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::HARDWARE; }

  Trigger<time_picker::Time> *get_set_trigger() const { return set_trigger_; }
  void set_optimistic(bool optimistic) { optimistic_ = optimistic; }
  void set_initial_value(time_picker::Time initial_value) { initial_value_ = initial_value; }
  void set_restore_value(bool restore_value) { this->restore_value_ = restore_value; }

 protected:
  void control(time_picker::Time value) override;
  bool optimistic_{false};
  time_picker::Time initial_value_{0,0,0};
  bool restore_value_{false};
  Trigger<time_picker::Time> *set_trigger_ = new Trigger<time_picker::Time>();
  optional<std::function<optional<time_picker::Time>()>> f_;

  ESPPreferenceObject pref_;
};

}  // namespace template_
}  // namespace esphome
