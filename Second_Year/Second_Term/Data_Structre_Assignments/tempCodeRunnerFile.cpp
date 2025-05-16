#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
const long long MOD=1e9+7;



long long power(long long base,long long exp,long long mod){
    long long res=1;
    while(exp>0){
        if(exp%2==1){
            res=(res*base)%mod;
        }
        base=(base*base)%mod;
        exp=exp/2;
    }
    return res;
}

void solve(){
    long long n,k;
    cin>>n>>k;

    long long q=n/k;
    long long r=n%k;

    long long ans = (r * power(2, q + 1, MOD) % MOD );
    long long ans2 = (k - r) * power(2, q, MOD) % MOD;

    cout<<(ans+ans2) %MOD<<endl;
}

int main(){
    int t=1;
    while(t--){
        solve();
    }
}