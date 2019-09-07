#include <stdlib.h>
#include <stdio.h>

#include "carunner.h"

struct Process
{
    int W;
    int H;
    char proj[1024];
    int steps;
    int sample;
    int termcrit;
    char T[1024];
};

bool LoadFile( char *, Material&, Structure&, Process& );

int main( void )
{
    // material data struct - this is just a struct that holds some numbers
    // implemented in automata.cpp
    Material mat;

    // structure data struct - just some constants
    // implemented in automata.cpp
    Structure str;

    // process struct - not quite sure yet what this holds
    // implemented here
    Process pro;

    // the CA object. this has methods for init, run, save, destroy, etc.
    // implemented in carunner.cpp
    CARunner car;

    // loads config
    if( !LoadFile( "material.txt", mat, str, pro ) )
    {
        printf( "Az adatfajl nem elerheto!\n" );
        return( 0 );
    }

    // initializes the CA runner
    car.Init( pro.W, pro.H, pro.steps, pro.sample, pro.termcrit );

    // runs the CA runner
    car.Run( pro.proj, mat, str, pro.T );

    // saves stuff
    car.SaveMeasuredData();

    // calls destructor
    car.Destroy();

	return 0;
}

// loads config file that sets up the material, structure and process
bool LoadFile( char *pFilename, Material &mat, Structure &str, Process &pro )
{
    FILE *file = fopen( pFilename, "rt" );
    if( !file ) return( false );
    char text[1024];

    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Ta = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Qag = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Bag = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Es = atof( text );

    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Qrn[0] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Brn[0] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Qrg[0] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Brg[0] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Qc[0] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Qan[0] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Ban[0] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Gg[0] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Kg[0] = atof( text );

    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Qrn[1] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Brn[1] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Qrg[1] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Brg[1] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Qc[1] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Qan[1] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Ban[1] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Gg[1] = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    mat.Kg[1] = atof( text );

    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    str.q = atof( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    str.Gr = atoi( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    str.Dg = atoi( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    str.Ph = atoi( text );

    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    pro.W = atoi( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    pro.H = atoi( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    sprintf( pro.proj, "%s", text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    pro.steps = atoi( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    pro.sample = atoi( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    pro.termcrit = atoi( text );
    fscanf( file, "%s", text );
    fscanf( file, "%s", text );
    sprintf( pro.T, "%s", text );

    fclose( file );
    return( true );
}
