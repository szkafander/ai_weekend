#ifndef CA_STATE_H
#define CA_STATE_H

union Number32bit
{
	unsigned char c[4];
	unsigned long l;
};

struct State
{
    int P;
    int D;
    Number32bit O;
};

#endif
