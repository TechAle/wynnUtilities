#include <string>

class statusItems{
public:
    std::string name;
    std::string type;
    int min, max;
    statusItems(std::string name, nlohmann::json values) {
        this->name = name;
        int idx = 0;
        for(auto& [key, val] : values.items()) {
            switch (idx++) {
                case 0:
                    max = val;
                    break;
                case 1:
                    min = val;
                    break;
                case 2:
                    type = val;
                    break;
            }

        }
    }

};

class statuses {
public:
    void setValues(nlohmann::json values) {
        for(auto& [key, val] : values.items()) {
            modifiers.emplace_back(key, val);
        }
    }
    std::vector<statusItems> modifiers;

private:

};