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

    // Iterate every ing
    for(auto& [name, row] : jsonFile.items()) {
        // Iterate every value of the ing
        int step = 0;
        int tier;
        int level;
        int prof;
        ingModifiers ingMod;
        itemModifiers itMod;
        statuses stats;
        for(auto& [key, value] : row.items()) {
            switch (step++) {
                case 0:
                    tier = value;
                    break;
                case 1:
                    level = value;
                    break;
                case 2:
                    prof = value;
                    break;
                case 3:
                    ingMod.setValues(value);
                    break;
                case 4:
                    itMod.setValues(value);
                    break;
                case 5:
                    stats.setValues(value);
                    break;

            }
            cout << key << " " << value << "\n";
        }
    }

    /*
    */


    return 0;
}
