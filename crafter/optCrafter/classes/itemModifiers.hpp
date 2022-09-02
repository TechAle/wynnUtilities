#include <string>
#include <utility>

class modifierItem {
public:
    int value, name;

    modifierItem(const std::string& name, int value) {
        this->name = std::stoi(name);
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