class ingMod {
public:
    int id, value;
    ingMod(int id, int value) {
        this->id = id;
        this->value = value;
    }
};

class ingModifiers {
public:

    void setValues(nlohmann::json values) {
        for(auto& [key, val] : values.items()) {
            modifiers.emplace_back(std::stoi(key), val);
        }
    }

    std::vector<ingMod> modifiers;


};