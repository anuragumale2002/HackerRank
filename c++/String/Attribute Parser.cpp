#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    unordered_map<string, string> mp;
    vector<string> tags;

    while (n--) {
        string line;
        getline(cin, line);

        // If closing tag
        if (line.substr(0, 2) == "</") {
            tags.pop_back();
        } else {
            // Remove '<' and '>'
            line.erase(remove(line.begin(), line.end(), '<'), line.end());
            line.erase(remove(line.begin(), line.end(), '>'), line.end());

            // Split into words
            stringstream ss(line);
            string tagName;
            ss >> tagName;

            // Add new tag
            tags.push_back(tagName);

            // Build fullTag
            string fullTag = tags[0];
            for (int i = 1; i < (int)tags.size(); i++) {
                fullTag += "." + tags[i];
            }

            while (ss) {
                string attr;
                ss >> attr;
                if (!ss || attr == "=") break; 
                string eq;
                string val;
                ss >> eq >> val;

                // remove quotes
                if (val.front() == '"') val.erase(0, 1);
                if (val.back() == '"') val.pop_back();

                mp[fullTag + "~" + attr] = val;
            }
        }
    }

    while (q--) {
        string query;
        cin >> query;
        if (mp.count(query)) {
            cout << mp[query] << "\n";
        } else {
            cout << "Not Found!\n";
        }
    }
    return 0;
}
