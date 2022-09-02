#include <string>
#include <utility>
#include <vector>
#include "ingModifiers.hpp"
#include "itemModifiers.hpp"
#include "statuses.hpp"

class ingridient {

public:
    std::string name;


    void setValue(std::string name, int tier, int level, std::vector<int> prof,
               ingModifiers ingModifiers, itemModifiers itemModifiers,
               statuses statuses) {
        this->name = std::move(name);
        this->tier = tier;
        this->level = level;
        this->prof = std::move(prof);
        this->ingModifiers = std::move(ingModifiers);
        this->itemModifiers = itemModifiers;
        this->statuses = std::move(statuses);
    }

private:
    int tier;
    int level;
    std::vector<int> prof;
    ingModifiers ingModifiers;
    itemModifiers itemModifiers;
    statuses statuses;
};

