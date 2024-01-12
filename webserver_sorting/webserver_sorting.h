#pragma once

#include "esphome/core/component.h"
#include "esphome/core/automation.h"
#include "esphome/core/helpers.h"
#include <cstring>

namespace esphome {
namespace webserver_sorting {

static const char *const TAG = "webserver_sorting";

struct Entry
{
    uint32_t objectId;
    uint32_t zIndex;
};

class SortingHandler
{
public:
    void Application::register_component_(Entry *entry) 
    {
        if (entry == nullptr) {
            ESP_LOGW(TAG, "Tried to register null Entry!");
            return;
        }

        for (auto *c : this->entries) {
            if (entry == c) {
            ESP_LOGW(TAG, "Entry %s already registered! (%p)", c->get_component_source(), c);
            return;
            }
        }
        this->entries.push_back(comp);
    }

private:
      std::vector<Entry *> entries{};
};


}  // namespace webserver_sorting
}  // namespace esphome