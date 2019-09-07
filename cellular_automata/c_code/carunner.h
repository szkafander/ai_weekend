#ifndef CA_RUNNER_H
#define CA_RUNNER_H

#include "automata.h"
#include "CprobImage.h"

#define TERMINATE_TIME  1
#define TERMINATE_RFULL 2
#define TERMINATE_AFULL 3
#define TERMINATE_BFULL 4

struct Results
{
    float Fr[3];
    float Fa[3];
    float T;
};

class CARunner
{
    public:
        void Init( int, int, int, int, int );
        void Destroy( void );

        void Run( char *, Material, Structure, char * );

        bool SaveMeasuredData( void );

    private:
        bool TermCriteria( int, int );
        bool SaveProject( void );

        Automata ca;

        float T;
        int steps;
        int sample;
        int termcrit;

        char proj[1024];
        char path[1024];
        char Tstr[1024];

        Results *res;

        CprobImage cimg;
};

#endif
