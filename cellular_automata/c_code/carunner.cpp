#include <stdlib.h>
#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include <fparser.hh>

#include "carunner.h"

void CARunner::Init( int W = 512, int H = 512, int S = 10000, int A = 100, int C = 1 )
{
    // number of steps
    steps    = S;

    // TODO
    // number of samples??
    // the automaton has 10000 steps and measures every 100 step
    sample   = A;

    // TODO
    // termination criterion??
    termcrit = C;
    
    // init results struct - only holds some data
    res = new Results[steps+1];
    for( int i = 0; i < steps+1; i++ )
    {
        res[i].Fa[0] = 1.0;
        res[i].Fa[1] = 1.0;
        res[i].Fa[2] = 1.0;
        res[i].Fr[0] = 1.0;
        res[i].Fr[1] = 1.0;
        res[i].Fr[2] = 1.0;
        res[i].T = 0.0;
    }

    // inits the CA object
    // the CA object is probably the essence of this
    // investigation should focus on the workings of this object
    ca.Init( W, H );

    // inits the cprobimage
    // I think the cprobimage is only used to measure stuff in the universe 
    // caprobimage is not directly related to the CA
    cimg.Init( W, H );
}

// dispatch method to check which termination criterion is reached
bool CARunner::TermCriteria( int i, int s )
{
    bool re = false;
    switch( termcrit )
    {
        // reached the end of steps
        case TERMINATE_TIME:
            if( s < steps ) re = true;
            break;
        // TODO
        // if the universe is fully recrystallized then terminate
        case TERMINATE_RFULL:
            if( res[s].Fr[i] < 1.0 ) re = true;
            break;
        // TODO
        // if every cell is in phase A then terminate
        case TERMINATE_AFULL:
            if( res[s].Fa[i] < 1.0 ) re = true;
            break;
        // TODO
        // if every cell is in phase B then terminate
        case TERMINATE_BFULL:
            if( 1.0 - res[s].Fa[i] < 1.0 ) re = true;
            break;
    }
    return( re );
}

void CARunner::Run( char *name, Material M, Structure S, char *strt )
{
    mkdir( name );
    sprintf( path, "%s/%s", name, name );
    sprintf( proj, "%s", name );
    sprintf( Tstr, "%s", strt );
    //Tstr: you can add the temperature field to the automaton 

    ca.SetMaterial( M );
    ca.SaveMaterialLog( path );

    std::string function( Tstr );
    FunctionParser fparser;
    int rel = fparser.Parse( function, "t" );
    if( !(rel < 0) )
    {
        printf( "HIBA!\n\nA megadott hõmérséklet képlet nem megfelelõ formátumú!\n\n" );
        return;
    }
    double vals[1];
    int j;

    for( int i = 0; i < 5; i++ )
    {
        ca.CreateVideo( path, i );
        ca.StructureCreate( S );
        ca.AddFrameVideo();
        ca.SaveStructureLog( path, i );
        res[0].Fr[i] = ca.MeasureRecrFraction();
        res[0].Fa[i] = ca.MeasureAlphaFraction();
        j = 1;
        while( TermCriteria( i, j-1 ) )
        {
            vals[0] = (double)j;
            T = (float)fparser.Eval( vals );
            ca.Step( T );
            ca.AddFrameVideo();
            res[j].Fr[i] = ca.MeasureRecrFraction();
            res[j].Fa[i] = ca.MeasureAlphaFraction();
            res[j].T = T;
            if( j % sample == 0 )
            {
                ca.SaveImage( path, i, j );
                cimg.Measure( ca.GetUniverse(), path, i, j );
            }
            j++;
        }
        ca.DestroyVideo();
    }
    SaveProject();
}

void CARunner::Destroy( void )
{
    ca.Destroy();
    cimg.Destroy();
    delete []res;
}

bool CARunner::SaveMeasuredData( void )
{
    char text[1024];
    sprintf( text, "%s_data.txt", path );
    FILE *file = fopen( text, "wt" );
    if( !file ) return( false );
    fprintf( file, "steps:\t%d\n", steps );
    fprintf( file, "step\t" );
    fprintf( file, "Fr(1)\tFr(2)\tFr(3)\t" );
    fprintf( file, "Fr\t" );
    fprintf( file, "Fa(1)\tFa(2)\tFa(3)\t" );
    fprintf( file, "Fa\n" );
    for( int i = 0; i <= steps; i++ )
    {
        fprintf( file, "%d\t", i );
        fprintf( file, "%.6f\t%.6f\t%.6f\t", res[i].Fr[0], res[i].Fr[1], res[i].Fr[2] );
        fprintf( file, "%.6f\t", ( res[i].Fr[0] + res[i].Fr[1] + res[i].Fr[2] ) / 3.0 );
        fprintf( file, "%.6f\t%.6f\t%.6f\t", res[i].Fa[0], res[i].Fa[1], res[i].Fa[2] );
        fprintf( file, "%.6f\n", ( res[i].Fa[0] + res[i].Fa[1] + res[i].Fa[2] ) / 3.0 );
    }
    fclose( file );
    return( true );
}

bool CARunner::SaveProject( void )
{
    char filename[1024];
    sprintf( filename, "%s.prj", path );
    FILE *file = fopen( filename, "wt" );
    if( !file ) return( false );
    fprintf( file, "name\t%s\n", proj );
    fprintf( file, "steps\t%d\n", steps );
    fprintf( file, "sample\t%d\n", sample );
    fprintf( file, "termCriteria\t%d\n", termcrit );
    fprintf( file, "T\t%s\n", Tstr );
    fclose( file );
    return( true );
}
