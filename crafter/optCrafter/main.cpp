#include "utils/json.hpp"
#include <fstream>
#include <iostream>
#include <sstream>
#include "classes/ingridient.hpp"

using namespace std;
using json = nlohmann::json;

int main() {
    ifstream fJson("../../dataset/ings.json");
    stringstream buffer;
    buffer << fJson.rdbuf();
    json jsonFile = json::parse(buffer.str());
    ingridient ingsNow[jsonFile.size()];

    // Iterate every ing
    int idIngridients = 0;
    for(auto& [name, row] : jsonFile.items()) {
        // Iterate every value of the ing
        int step = 0;
        int tier;
        int level;
        vector<int> prof;
        ingModifiers ingMod;
        itemModifiers itMod;
        statuses stats;
        for(auto& [key, value] : row.items()) {
            int idx = 0;
            switch (step++) {
                case 0:
                    ingMod.setValues(value);
                    break;
                case 1:
                    itMod.setValues(value);
                    break;
                case 2:
                    level = value;
                    break;
                case 3:
                    for(int val : value) {
                        prof.push_back(val);
                    }
                    break;
                case 4:
                    stats.setValues(value);
                    break;
                case 5:
                    tier = value;
                    break;

            }
        }
        ingsNow[idIngridients++].setValue(name, tier, level, prof, ingMod, itMod, stats);
    }
    // There are some more ings that are powders



    return 0;
}
