#include <iostream>
#include <iomanip> 
using namespace std;

int main() {
	int T; cin >> T;
	cout << setiosflags(ios::uppercase);
	cout << setw(0xf) << internal;
	while(T--) {
		double A; cin >> A;
		double B; cin >> B;
		double C; cin >> C;
        cout << setw(0); // cancel previous width
        cout << nouppercase << showbase << hex
             << (long long)A << endl;
        cout << right; // override internal alignment
        cout << dec << fixed << setprecision(2)
             << showpos << setfill('_') << setw(15)
             << B << endl;
        cout << noshowpos << uppercase
             << scientific << setprecision(9)
             << C << endl;
	}
	return 0;

}