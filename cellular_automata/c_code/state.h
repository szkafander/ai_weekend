#ifndef CA_STATE_H
#define CA_STATE_H

union Number32bit
{
    // TODO
    // what is c?
	unsigned char c[4];
    // TODO
    // what is l?
	unsigned long l;
};

struct State
{
    // TODO
    // please write down what each of these vars represent
    // please write down the type of these vars - what values can they assume?
    // phase, this seems to be binary
    int P;
    // deformed, this seems to be binary
    int D;
    // orientation, this seems to be continuous
    Number32bit O;
};

#endif
