#include <bits/stdc++.h>
#define speedup ios::sync_with_stdio(false); cin.tie(nullptr);
#define ll long long
#define fo(i,k,j) for(ll i = k; i < j; i++)
#define Y cout << "Yes" << endl;
#define N cout << "No" << endl;
#define so(a) sort(a.begin(),a.end());
#define even(x) if(x%2==0)
#define odd(x) if(x%2!=0)
using namespace std;

void solve() {
    int n, m;
    cin >> n >> m;
    vector<string> grid(n);
    vector<int> row_counts(n, 0);
    vector<int> col_counts(m, 0);

    // Read the grid and count 1s in each row and column
    for (int i = 0; i < n; ++i) {
        cin >> grid[i];
        for (int j = 0; j < m; ++j) {
            if (grid[i][j] == '1') {
                row_counts[i]++;
                col_counts[j]++;
            }
        }
    }

    // Check if any row or column is overfilled
    bool possible = true;
    for (int i = 0; i < n; ++i) {
        if (row_counts[i] > m) {
            possible = false;
            break;
        }
    }
    for (int j = 0; j < m; ++j) {
        if (col_counts[j] > n) {
            possible = false;
            break;
        }
    }

    if (possible) {
        cout << "YES" << endl;
    } else {
        cout << "NO" << endl;
    }

        
        
 

}

int main() {
    speedup;

    ll t = 1;
    cin >> t;

    while (t--) {
        solve();
    }

    return 0;
}
