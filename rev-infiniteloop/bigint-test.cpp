#include <iostream>
#include <algorithm>
#include "int2048.h"

using namespace std;

int main()
{
    bigint<8> a, b;
    a = b = 1000000000000ll;
    a *= b;
    string s;
    while(a != (bigint<8>)0)
    {
        s.push_back(((int)(a%(bigint<8>)10))+'0');
        a /= 10;
    }
    reverse(s.begin(), s.end());
    cout << s << endl;
    return 0;
}
