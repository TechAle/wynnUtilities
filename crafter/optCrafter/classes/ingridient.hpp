#include <string>
#include <vector>
#include "ingModifiers.hpp"
#include "itemModifiers.hpp"
#include "statuses.hpp"

class ingridient {

public:
    const int id;
    const std::string name;
private:
    const int tier;
    const int level;
    const int profession;
    std::vector<ingModifiers> ingModifiers;
    std::vector<itemModifiers> itemModifiers;
    std::vector<statuses> statuses;
};

