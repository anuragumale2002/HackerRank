#include<bits/stdc++.h>

using namespace std;

//Define the structs Workshops and Available_Workshops.
//Implement the functions initialize and CalculateMaxWorkshops
struct Workshop {
    int start_time;
    int duration;
    int end_time;
};

struct Available_Workshops {
    int n;
    Workshop* workshops;
};

Available_Workshops* initialize(int start_time[], int duration[], int n) {
    Available_Workshops* aw = new Available_Workshops;
    aw->n = n;
    aw->workshops = new Workshop[n];

    for (int i = 0; i < n; i++) {
        aw->workshops[i].start_time = start_time[i];
        aw->workshops[i].duration = duration[i];
        aw->workshops[i].end_time = start_time[i] + duration[i];
    }

    return aw;
}

bool compare(Workshop a, Workshop b) {
    return a.end_time < b.end_time;
}

int CalculateMaxWorkshops(Available_Workshops* ptr) {
    // Sort workshops by end time
    sort(ptr->workshops, ptr->workshops + ptr->n, compare);

    int count = 0;
    int current_end = 0;

    for (int i = 0; i < ptr->n; i++) {
        if (ptr->workshops[i].start_time >= current_end) {
            count++;
            current_end = ptr->workshops[i].end_time;
        }
    }

    return count;
}

int main(int argc, char *argv[]) {
    int n; // number of workshops
    cin >> n;
    // create arrays of unknown size n
    int* start_time = new int[n];
    int* duration = new int[n];

    for(int i=0; i < n; i++){
        cin >> start_time[i];
    }
    for(int i = 0; i < n; i++){
        cin >> duration[i];
    }

    Available_Workshops * ptr;
    ptr = initialize(start_time,duration, n);
    cout << CalculateMaxWorkshops(ptr) << endl;
    return 0;
}
