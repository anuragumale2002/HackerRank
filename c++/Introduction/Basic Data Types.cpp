#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int i;
    long l;
    char c;
    float f;
    double d;

    // Read input values
    cin >> i >> l >> c >> f >> d;

    // Print each on its own line with correct precision
    cout << i << endl;
    cout << l << endl;
    cout << c << endl;
    cout << fixed << setprecision(3) << f << endl;
    cout << fixed << setprecision(9) << d << endl;

    return 0;
}
