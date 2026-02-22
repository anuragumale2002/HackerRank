#include <iostream>
#include <deque>
#include <vector>
using namespace std;

int main() {
    int T;
    cin >> T;

    while (T--) {
        int N, K;
        cin >> N >> K;

        vector<int> arr(N);
        for (int i = 0; i < N; i++)
            cin >> arr[i];

        deque<int> dq;  // stores indices

        for (int i = 0; i < N; i++) {

            // Remove elements out of this window
            if (!dq.empty() && dq.front() == i - K)
                dq.pop_front();

            // Remove smaller elements from back
            while (!dq.empty() && arr[dq.back()] < arr[i])
                dq.pop_back();

            dq.push_back(i);

            // Print max after first window is complete
            if (i >= K - 1)
                cout << arr[dq.front()] << " ";
        }

        cout << endl;
    }

    return 0;
}