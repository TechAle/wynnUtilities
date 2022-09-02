#include <string>
#include <utility>

class modifierItem {
public:
    std::string name;
    int value;

    modifierItem(std::string name, int value) {
        this->name = std::move(name);
        this->value = value;
    }
};

class itemModifiers {
public:

    void setValues(const nlohmann::json& values) {
        for(auto& [key, val] : values.items()) {
            modifiers.emplace_back(key, val);
        }
    }

    std::vector<modifierItem> modifiers;
};