#include <iostream>
#include <set>
using namespace std;

int main() {
    int Q;
    cin >> Q;

    set<int> s;

    while(Q--) {
        int type, x;
        cin >> type >> x;

        if(type == 1) {
            // Insert
            s.insert(x);
        }
        else if(type == 2) {
            // Erase (does nothing if not present)
            s.erase(x);
        }
        else if(type == 3) {
            // Find
            if(s.find(x) != s.end())
                cout << "Yes" << endl;
            else
                cout << "No" << endl;
        }
    }

    return 0;
}