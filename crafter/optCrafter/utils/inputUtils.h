#include <iostream>

using namespace std;

// Request a number
static int requestInt(const string& text, int length) {
    int temp;
    do {
        cout    << text << endl
                << "Choose: ";
        cin >> temp;
    }while (temp < 0 || temp > length);
    return temp;
}

// Request a string
static string requestString(const string& text) {
    cout << text;
    string output;
    while( getline( cin, output ) ) {
        if (!output.empty())
            return output;
    }
    return output;
}