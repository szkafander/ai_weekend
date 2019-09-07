#ifndef CA_STATE_H
#define CA_STATE_H

union Number32bit
{
	unsigned char c[4];
	unsigned long l;
};

struct State
{
    // TODO
    // please write down what each of these vars represent
    // please write down the type of these vars - what values can they assume?
    int P;
    int D;
    Number32bit O;
};

#endif
