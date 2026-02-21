#include <iostream>
#include <vector>

using namespace std;

int main() {
    int n, q;
    cin >> n >> q;   // FIRST LINE HAS TWO VALUES

    vector<vector<int>> arr(n);

    // Read arrays
    for (int i = 0; i < n; i++) {
        int k;
        cin >> k;

        arr[i].resize(k);

        for (int j = 0; j < k; j++) {
            cin >> arr[i][j];
        }
    }

    // Process queries
    for (int i = 0; i < q; i++) {
        int x, y;
        cin >> x >> y;
        cout << arr[x][y] << endl;
    }

    return 0;
}
