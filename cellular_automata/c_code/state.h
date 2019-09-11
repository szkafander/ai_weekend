#ifndef CA_STATE_H
#define CA_STATE_H

union Number32bit
{
    // TODO
    // what is c? 
    // c is the crystallographic orientation
	unsigned char c[4];
    // TODO
    // what is l?
    // array for the orientation (last 8 but is not used)
	unsigned long l;
};

struct State
{
    // TODO
    // please write down what each of these vars represent
	//P is for the phase, binary
	//D is deformed, binary
    // please write down the type of these vars - what values can they assume?
	
    // phase, this seems to be binary
    int P;
	
    // deformed, this seems to be binary
    int D;
	
    // orientation, this seems to be continuous
    Number32bit O;
};

#endif
