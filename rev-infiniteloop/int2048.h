template<int WORDS>
struct bigint
{
    unsigned short data[WORDS];
    bigint(){}
    bigint& operator=(unsigned long long x)
    {
        static_assert(WORDS >= 4, "Ti obosralsya");
        data[0] = x;
        data[1] = x >> 16;
        data[2] = x >> 32;
        data[3] = x >> 48;
        for(int i = 4; i < WORDS; i++)
            data[i] = 0;
        return *this;
    }
#define FROM(tp)\
    bigint& operator=(tp x)\
    {\
        if(x >= 0)\
            *this = (unsigned long long)x;\
        else\
            *this = -(bigint)(unsigned long long)-x;\
        return *this;\
    }
    FROM(long long);
    FROM(unsigned int);
    FROM(int);
    FROM(unsigned short);
    FROM(short);
    FROM(unsigned char);
    FROM(char);
#undef FROM
    template<int WORDS2>
    bigint& operator=(const bigint<WORDS2>& x)
    {
        for(int i = 0; i < WORDS && i < WORDS2; i++)
            this->data[i] = x.data[i];
        for(int i = WORDS2; i < WORDS; i++)
            this->data[i] = 0;
    }
    template<class T>
    bigint(const T& x)
    {
        *this = x;
    }   
    bigint operator~() const
    {
        bigint ans;
        for(int i = 0; i < WORDS; i++)
            ans.data[i] = ~this->data[i];
        return ans;
    }
#define BITOP(x)\
    bigint& operator x(const bigint& other)\
    {\
        for(int i = 0; i < WORDS; i++)\
            this->data[i] x other.data[i];\
        return *this;\
    }
    BITOP(^=);
    BITOP(|=);
    BITOP(&=);
#undef BITOP
    bigint& operator<<=(int shift)
    {
        int a = shift / 16;
        int b = shift % 16;
        for(int i = WORDS - a - 1; i >= 0; i--)
            this->data[i + a] = this->data[i];
        for(int i = 0; i < a; i++)
            this->data[i] = 0;
        unsigned short carry = 0;
        for(int i = a; i < WORDS; i++)
        {
            unsigned short cur = this->data[i];
            this->data[i] = (cur << b) | carry;
            carry = cur >> (16 - b);
        }
        return *this;
    }
    bigint& operator>>=(int shift)
    {
        int a = shift / 16;
        int b = shift % 16;
        for(int i = 0; i + a < WORDS; i++)
            this->data[i] = this->data[i + a];
        for(int i = WORDS - a; i < WORDS; i++)
            this->data[i] = 0;
        unsigned short carry = 0;
        for(int i = WORDS - a - 1; i >= 0; i--)
        {
            unsigned short cur = this->data[i];
            this->data[i] = (cur >> b) | carry;
            carry = cur << (16 - b);
        }
        return *this;
    }
#define ADDOP(x)\
    bigint& operator x(const bigint& other)\
    {\
        short carry = 0;\
        for(int i = 0; i < WORDS; i++)\
        {\
            unsigned int cur = 0;\
            cur += this->data[i];\
            cur x other.data[i];\
            cur += carry;\
            carry = cur >> 16;\
            this->data[i] = cur;\
        }\
        return *this;\
    }
    ADDOP(+=);
    ADDOP(-=);
#undef ADDOP
private:
    void add_inplace(int word, unsigned short what)
    {
        unsigned short carry = what;
        while(carry && word < WORDS)
        {
            unsigned int cur = this->data[word];
            cur += carry;
            this->data[word++] = cur;
            carry = cur >> 16;
        }
    }
public:
    bigint operator*(const bigint& other) const
    {
        bigint ans = 0;
        for(int i = 0; i < WORDS; i++)
            for(int j = 0; i + j < WORDS; j++)
            {
                unsigned int cur = this->data[i];
                cur *= other.data[j];
                ans.add_inplace(i + j, cur);
                if(i + j + 1 < WORDS)
                    ans.add_inplace(i + j + 1, cur >> 16);
            }
        return ans;
    }
    inline bigint divmod(const bigint& other)
    {
        bigint ans = 0;
        for(int bit = 16 * WORDS - 1; bit >= 0; bit--)
        {
            if(other <= ((*this) >> bit))
            {
                ans |= bigint(1) << bit;
                *this -= (other << bit);
            }
        }
        return ans;
    }
    bigint operator/(const bigint& other) const
    {
        bigint self = *this;
        return self.divmod(other);
    }
    bigint& operator%=(const bigint& other)
    {
        this->divmod(other);
        return *this;
    }
#define COMPARATOR(op, op0, def)\
    bool operator op(const bigint& other) const\
    {\
        for(int i = WORDS - 1; i >= 0; i--)\
            if(this->data[i] op0 other.data[i])\
                return true;\
            else if(other.data[i] op0 this->data[i])\
                return false;\
        return def;\
    }
    COMPARATOR(>, >, false);
    COMPARATOR(>=, >, true);
    COMPARATOR(<, <, false);
    COMPARATOR(<=, <, true);
    COMPARATOR(!=, !=, false);
#undef COMPARATOR
    bool operator==(const bigint& other) const
    {
        return !(*this != other);
    }
#undef COMPARATOR
#define N2I0(x, y, at)\
    bigint operator y(at other) const\
    {\
        bigint ans = *this;\
        ans x other;\
        return ans;\
    }
#define N2I(x, y) N2I0(x, y, const bigint&)
    N2I(^=, ^);
    N2I(|=, |);
    N2I(&=, &);
    N2I0(<<=, <<, int);
    N2I0(>>=, >>, int);
    N2I(+=, +);
    N2I(-=, -);
    N2I(%=, %);
#undef N2I
#undef N2I0
#define I2N(x, y)\
    bigint& operator y(const bigint& other)\
    {\
        *this = *this x other;\
        return *this;\
    }
    I2N(*, *=);
    I2N(/, /=);
#undef I2N
    bigint& operator+() const
    {
        return *this;
    }
    bigint operator-()
    {
        bigint ans = 0;
        ans -= *this;
        return ans;
    }
    operator unsigned long long()
    {
        unsigned long long ans;
        for(int i = 3; i >= 0; i--)
            ans = (ans << 16) | data[i];
        return ans;
    }
#define CAST_TO(x)\
    operator x()\
    {\
        return (x)(unsigned long long)*this;\
    }
    CAST_TO(long long);
    CAST_TO(unsigned int);
    CAST_TO(int);
    CAST_TO(unsigned short);
    CAST_TO(short);
    CAST_TO(unsigned char);
    CAST_TO(char);
};
