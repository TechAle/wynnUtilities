#include "./classes/ingredientMain.h"
#include "./utils/inputUtils.h"

int main() {

    ingredientMain dataset = ingredientMain();

    bool loop = true;
    while (loop) {
        int choose = requestInt("1) id->ing\n2) prof->ids\n3) name->id", 5);
        int temp;
        switch (choose) {
            case 0:
                loop = false;
                break;
            case 1:
                temp = requestInt("Id: (max: " + std::to_string(dataset.maxItems) + ")" , dataset.maxItems);
                dataset.prettyPrint(temp);
                break;
            case 2:
                temp = requestInt("Prof: " , 15);
                std::cout << "Results: ";
                for(ingridient* value : dataset.getProfItems(temp)) {
                    std::cout << value->name << "|";
                }
                std::cout << endl;
                break;
            case 3:
                std::cout << "Output: " << dataset.nameToId(requestString("Name: ")) << endl;
                break;
            default:
                break;
        }
    }

    return 0;
}
