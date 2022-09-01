#include <string>

class statuses {
public:
    statuses() {
        name = "";
        min = 0;
        max = 0;
        type = 0;
    }

    void setValues(json values) {

    }

    const std::string name;
private:
    const int min;
    const int max;
    const int type;
};