cmake_minimum_required(VERSION 3.17)
project(crafter)

set(CMAKE_CXX_STANDARD 17)

add_executable(crafter main.cpp classes/ingridient.hpp classes/statuses.hpp classes/itemModifiers.hpp classes/ingModifiers.hpp classes/ingredientMain.h utils/inputUtils.h classes/recipesMain.h)