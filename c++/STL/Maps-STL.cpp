#include <iostream>
#include <map>
using namespace std;

int main() {
    int Q;
    cin >> Q;

    map<string, int> m;

    while(Q--) {
        int type;
        cin >> type;

        string name;
        cin >> name;

        if(type == 1) {
            int marks;
            cin >> marks;
            m[name] += marks;   // add marks (creates key if not present)
        }
        else if(type == 2) {
            m.erase(name);      // remove student completely
        }
        else if(type == 3) {
            cout << m[name] << endl;  
            // if name not present, m[name] creates it with value 0
        }
    }

    return 0;
}