#include <iostream>
#include <string>
using namespace std;

int main() {
    string a, b;
    cin >> a >> b;

    // 1. Print lengths
    cout << a.length() << " " << b.length() << endl;

    // 2. Concatenate
    cout << a + b << endl;

    // 3. Swap first characters
    char temp = a[0];
    a[0] = b[0];
    b[0] = temp;

    cout << a << " " << b << endl;

    return 0;
}
