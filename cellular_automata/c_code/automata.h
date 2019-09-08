#ifndef CA_AUTOMATA_H
#define CA_AUTOMATA_H

#include <cv.h>
#include <highgui.h>

#include "CprobImage.h"
#include "state.h"

struct Structure
{
    // TODO
    // please give the meaning of each term
    int   Gr;
    float q;
    float H;
    float V;
    int   Dg;
    int   Ph;
};

struct Material
{
    // TODO
    // please give the meaning of each term
    float Ta;
    float Qag;
    float Bag;
    float Es;

    float Qc[2];
    float Qrn[2];
    float Qrg[2];
    float Brn[2];
    float Brg[2];
    float Qan[2];
    float Ban[2];
    float Gg[2];
    float Kg[2];
};

struct Probability
{
    // TODO
    // please give the meaning of each term
    float Se;
    float Ag;
    float Abg;

    float Co[2];
    float Rn[2];
    float Rg[2];
    float Rbn[2];
    float Rbg[2];
    float An[2];
    float Abn[2];
};

class Automata
{
    public:
        void Init( int, int );
        void Destroy( void );

        void StructureCreate( Structure );
        void SetMaterial( Material );

        void Step( float );
        void SaveImage( char *, int, int );
        float MeasureRecrFraction( void );
        float MeasureAlphaFraction( void );

        State* GetUniverse( void );

        void CreateVideo( char*, int );
        void AddFrameVideo( void );
        void DestroyVideo( void );

        bool SaveStructureLog( char*, int );
        bool SaveMaterialLog( char * );

    private:
        State *oldarray;
        State *newarray;
        float *proarray;
        int width;
        int height;

        void BoundaryCondition( void );
        void Update( void );

        int C;
        int N;
        int S;
        int W;
        int E;

        void Position( int, int );

        float T;

        Material    mat;
        Probability pro;
        void Probabilities( void );

        void AllotropicNucleation( void );
        void AllotropicGrowth( void );
        void RecrystallisationNucleation( void );
        void RecrystallisationGrowth( void );
        void GrainCoarsening( void );

        int DeformedNeighbour( void );
        int DifferentNeighbour( void );
        int PhaseNeighbour( void );

        IplImage* ocvimage;
        CvVideoWriter *ocvvideo;

        void PlotImage( void );

        Structure str;
        void StructureInit( void );
        void StructureGrowth( void );
        int  StructureMeasure( void );
};

#endif
