#pragma once

#include "esphome/core/component.h"
#include "esphome/core/automation.h"
#include "esphome/core/helpers.h"
#include "esphome/core/entity_base.h"
#include <cstring>
#include <string>
#include "time_picker_call.h"
#include "time_picker_traits.h"

namespace esphome {
namespace time_picker {

#define LOG_TIME_PICKER(prefix, type, obj) \
  if ((obj) != nullptr) { \
    ESP_LOGCONFIG(TAG, "%s%s '%s'", prefix, LOG_STR_LITERAL(type), (obj)->get_name().c_str()); \
    if (!(obj)->get_icon().empty()) { \
      ESP_LOGCONFIG(TAG, "%s  Icon: '%s'", prefix, (obj)->get_icon().c_str()); \
    } \
    if (!(obj)->traits.get_device_class().empty()) { \
      ESP_LOGCONFIG(TAG, "%s  Device Class: '%s'", prefix, (obj)->traits.get_device_class().c_str()); \
    } \
  }

class TimePicker : public EntityBase {
 public:
  Time state;

  void publish_state(Time state);

  TimePickerCall make_call() { return TimePickerCall(this); }

  void add_on_state_callback(std::function<void(Time)> &&callback);

  TimePickerTraits traits;

  /// Return whether this number has gotten a full state yet.
  bool has_state() const { return has_state_; }

 protected:
  friend class TimePickerCall;

  /** Set the value of the number, this is a virtual method that each number integration must implement.
   *
   * This method is called by the NumberCall.
   *
   * @param value The value as validated by the NumberCall.
   */
  virtual void control(Time value) = 0;

  CallbackManager<void(Time)> state_callback_;
  bool has_state_{false};
};

// class TimePicker : public Component {
//  public:
//   explicit TimePicker() = default;
//   explicit TimePicker(Time initial_value) : value_(initial_value) {}

//   Time &value() { return this->value_; }
//   void setup() override {}

//  protected:
//   Time value_{};
// };

// // struct Time2
// {
//   /** seconds after the minute [0-60]
//    * @note second is generally 0-59; the extra range is to accommodate leap seconds.
//    */
//   uint8_t second;
//   /// minutes after the hour [0-59]
//   uint8_t minute;
//   /// hours since midnight [0-23]
//   uint8_t hour;

//   Time2(const uint8_t second_, const uint8_t minute_, const uint8_t hour_) : second(second_), minute(minute_), hour(hour_) {}
//   // Standardkonstruktor hinzufügen (default-constructible)
//   Time2() : second(0), minute(0), hour(0) {}

//   // Kopierkonstruktor hinzufügen (copyable)
//   Time2(const Time2& other) : second(other.second), minute(other.minute), hour(other.hour) {}


//   // std::string toString() 
//   // {
//   //   std::string ret = "[" + std::to_string(hour) + ":" + std::to_string(minute) + ":" + std::to_string(second) + "]";
//   //   return ret;
//   // }
// };

// class RestoringTimePickerComponent : public Component {
//  public:
//   explicit RestoringTimePickerComponent() = default;
//   explicit RestoringTimePickerComponent(Time initial_value) : value_(initial_value) {}

//   Time &value() { return this->value_; }

//   void setup() override {
//     this->rtc_ = global_preferences->make_preference<Time2>(1944399030U ^ this->name_hash_);
//     this->rtc_.load(&this->value_);
//     memcpy(&this->prev_value_, &this->value_, sizeof(Time));
//   }

//   float get_setup_priority() const override { return setup_priority::HARDWARE; }

//   void loop() override { store_value_(); }

//   void on_shutdown() override { store_value_(); }

//   void set_name_hash(uint32_t name_hash) { this->name_hash_ = name_hash; }

//  protected:
//   void store_value_() {
//     int diff = memcmp(&this->value_, &this->prev_value_, sizeof(Time));
//     if (diff != 0) {
//       this->rtc_.save(&this->value_);
//       memcpy(&this->prev_value_, &this->value_, sizeof(Time));
//     }
//   }

//   Time value_{};
//   Time prev_value_{};
//   uint32_t name_hash_{};
//   ESPPreferenceObject rtc_;
// };

// template<class C, typename... Ts> class TimePickerTimeSetAction : public Action<Ts...> {
//  public:
//   explicit TimePickerTimeSetAction(C *parent) : parent_(parent) {}


//   TEMPLATABLE_VALUE(esphome::time_picker::Time, value);

//   void play(Ts... x) override { this->parent_->value() = this->value_.value(x...); }

//  protected:
//   C *parent_;
// };

// Time &id(TimePicker *value) { return value->value(); }
// Time &id(RestoringTimePickerComponent *value) { return value->value(); }

}  // namespace time_picker
}  // namespace esphome
