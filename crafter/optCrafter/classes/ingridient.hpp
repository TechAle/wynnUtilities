#include <string>
#include <vector>
#include "ingModifiers.hpp"
#include "itemModifiers.hpp"
#include "statuses.hpp"

class ingridient {

public:
    int id;
    std::string name;
private:
    int tier;
    int level;
    int profession;
    std::vector<ingModifiers> ingModifiers;
    std::vector<itemModifiers> itemModifiers;
    std::vector<statuses> statuses;
};

