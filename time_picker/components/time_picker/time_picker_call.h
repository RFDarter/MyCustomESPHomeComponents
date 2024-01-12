#pragma once

#include "esphome/core/helpers.h"
//#include "text_traits.h"

namespace esphome {
namespace time_picker {

class TimePicker;

struct Time
{
  /** seconds after the minute [0-60]
   * @note second is generally 0-59; the extra range is to accommodate leap seconds.
   */
  uint8_t second;
  /// minutes after the hour [0-59]
  uint8_t minute;
  /// hours since midnight [0-23]
  uint8_t hour;

  // Time(const uint8_t second_, const uint8_t minute_, const uint8_t hour_) : second(second_), minute(minute_), hour(hour_) {}
  // // Standardkonstruktor hinzufügen (default-constructible)
  // Time() : second(0), minute(0), hour(0) {}

  // // Kopierkonstruktor hinzufügen (copyable)
  // Time(const Time& other) : second(other.second), minute(other.minute), hour(other.hour) {}


  std::string toString() 
  {
    std::string ret = "[" + std::to_string(hour) + ":" + std::to_string(minute) + ":" + std::to_string(second) + "]";
    return ret;
  }
};

class TimePickerCall {
 public:
  explicit TimePickerCall(TimePicker *parent) : parent_(parent) {}
  void perform();

  TimePickerCall &set_value(const Time &value);

 protected:
  TimePicker *const parent_;
  optional<Time> value_;
  void validate_();
};

}  // namespace time_picker
}  // namespace esphome
