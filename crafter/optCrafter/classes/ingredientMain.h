#include "../utils/json.hpp"
#include <fstream>
#include <iostream>
#include <sstream>
#include "../classes/ingridient.hpp"

using namespace std;
using json = nlohmann::json;

class ingredientMain {

public:
    ingredientMain() { // NOLINT(cppcoreguidelines-pro-type-member-init)
        loadDataset();
    }

    int nameToId(const std::string& name) {
        for(int i = 0; i < maxItems; i++) {
            if(ingridients[i].name == name) {
                return i;
            }
        }
        return -1;
    }

    vector<ingridient*> getProfItems(int id) {
        vector<ingridient*> output;
        for(int i = 0; i < maxItems; i++) {
            if(std::find(ingridients[i].prof.begin(), ingridients[i].prof.end(), id) != ingridients[i].prof.end()) {
                output.push_back(&ingridients[i]);
            }

        }
        return output;
    }

    void prettyPrint(int id) {
        prettyPrint(ingridients[id]);
    }

    static void prettyPrint(const ingridient& ing) {
        cout << ing.name << " Level: " << ing.level << " Tier: " << ing.tier << endl << "Prof:";
        for(int prof : ing.prof) {
            cout << prof << " ";
        }
        cout << endl << "Ing mod: ";
        for(ingMod mod : ing.ingModifiers.modifiers) {
            cout << "id: " << mod.id << " value: " << mod.value << " ";
        }
        cout << endl << "Statuses: ";
        for(statusItems stats : ing.statuses.modifiers) {
            cout << "id: " << stats.id << " Type: " << stats.type << " Min: " << stats.min << "Max: " << stats.max << " ";
        }
        cout << endl << "Item mod: ";
        for(modifierItem iMod : ing.itemModifiers.modifiers) {
            cout << "id: " << iMod.id << " Value" << iMod.value << " ";
        }
        cout << endl;
    }

    // I dont think that we are ever going to get more then 1500 ingridients, *please*
    ingridient ingridients[1500];
    int maxItems;

private:

    void loadDataset() {
        ifstream fJson("../../dataset/ings.json");
        stringstream buffer;
        buffer << fJson.rdbuf();
        json jsonFile = json::parse(buffer.str());
        maxItems = (int) jsonFile.size();

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
            ingridients[idIngridients++].setValue(name, tier, level, prof, ingMod, itMod, stats);
        }
    }
};
