#include <iostream>
#include <string>
using namespace std;

struct Student {
    int age;
    string first_name;
    string last_name;
    int standard;
};

int main() {
    Student s;

    cin >> s.age;
    cin >> s.first_name;
    cin >> s.last_name;
    cin >> s.standard;

    cout << s.age << " "
         << s.first_name << " "
         << s.last_name << " "
         << s.standard;

    return 0;
}