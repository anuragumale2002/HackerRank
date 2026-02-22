#include <iostream>
#include <vector>

using namespace std;

class HotelRoom {
public:
    HotelRoom(int bedrooms, int bathrooms) {
        this->bedrooms = bedrooms;
        this->bathrooms = bathrooms;
    }

    // Make this virtual
    virtual int get_price() {
        return 50 * bedrooms + 100 * bathrooms;
    }

    // Always good practice with polymorphism
    virtual ~HotelRoom() {}

private:
    int bedrooms;
    int bathrooms;
};

class HotelApartment : public HotelRoom {
public:
    HotelApartment(int bedrooms, int bathrooms)
        : HotelRoom(bedrooms, bathrooms) {}

    int get_price() override {
        return HotelRoom::get_price() + 100;
    }
};

int main() {
    int n;
    cin >> n;
    vector<HotelRoom*> rooms;

    for (int i = 0; i < n; ++i) {
        string room_type;
        int bedrooms;
        int bathrooms;
        cin >> room_type >> bedrooms >> bathrooms;

        if (room_type == "standard") {
            rooms.push_back(new HotelRoom(bedrooms, bathrooms));
        } else {
            rooms.push_back(new HotelApartment(bedrooms, bathrooms));
        }
    }

    int total_profit = 0;
    for (auto room : rooms) {
        total_profit += room->get_price();
    }

    cout << total_profit << endl;

    for (auto room : rooms) {
        delete room;
    }

    return 0;
}