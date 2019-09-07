#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include "automata.h"

void Automata::Init( int iW, int iH )
{
    srand( time( NULL ) );

    width  = iW;
    height = iH;

    oldarray = new State[width*height];
    newarray = new State[width*height];
    proarray = new float[width*height];

    cvNamedWindow( "CA", 1 );

    CvSize ocvsize;
    ocvsize.width = width;
    ocvsize.height = height;
    ocvimage = cvCreateImage( ocvsize, IPL_DEPTH_8U, 3 );
}

void Automata::Destroy( void )
{
    delete []oldarray;
    delete []newarray;
    delete []proarray;

    cvReleaseImage( &ocvimage );
    cvDestroyWindow( "CA" );
}

void Automata::BoundaryCondition( void )
{
    for( int i = 0; i < height; i++ )
    {
        newarray[ i*width ] = newarray[ i*width + ( width-2 ) ];
        newarray[ i*width + ( width-1 ) ] = newarray[ i*width + 1   ];
        proarray[ i*width ] = proarray[ i*width + ( width-2 ) ];
        proarray[ i*width + ( width-1 ) ] = proarray[ i*width + 1   ];
    }
    for( int i = 0; i < width; i++ )
    {
        newarray[ i ] = newarray[ ( height-2 )*width + i ];
        newarray[ ( height-1 )*width + i ] = newarray[ width + i ];
        proarray[ i ] = proarray[ ( height-2 )*width + i ];
        proarray[ ( height-1 )*width + i ] = proarray[ width + i ];
    }
}

void Automata::Update( void )
{
    for( int i = 0; i < width*height; i++ ) oldarray[i] = newarray[i];
}

void Automata::Position( int x, int y )
{
    C = y*width+x;
    N = (y-1)*width+x;
    S = (y+1)*width+x;
    W = y*width+(x-1);
    E = y*width+(x+1);
}

void Automata::SetMaterial( Material im )
{
    mat = im;
}

void Automata::Probabilities( void )
{
    int B = 0;

    pro.Se = exp( -mat.Es/8.314/(T+273.0) );
    pro.Ag = exp( -mat.Qag/8.314/(T+273.0) );
    pro.Abg = exp( -mat.Bag/8.314/(T+273.0) );

    pro.Rn[0] = exp( -mat.Qrn[0]/8.314/(T+273.0) );
    pro.Rg[0] = exp( -mat.Qrg[0]/8.314/(T+273.0) );
    pro.Co[0] = exp( -mat.Qc[0]/8.314/(T+273.0) );
    pro.Rbn[0] = exp( -mat.Brn[0]/8.314/(T+273.0) );
    pro.Rbg[0] = exp( -mat.Brg[0]/8.314/(T+273.0) );
    pro.An[0] = exp( -mat.Qan[0]/8.314/(T+273.0) );
    pro.Abn[0] = exp( -mat.Ban[0]/8.314/(T+273.0) );

    pro.Rn[1] = exp( -mat.Qrn[1]/8.314/(T+273.0) );
    pro.Rg[1] = exp( -mat.Qrg[1]/8.314/(T+273.0) );
    pro.Co[1] = exp( -mat.Qc[1]/8.314/(T+273.0) );
    pro.Rbn[1] = exp( -mat.Brn[1]/8.314/(T+273.0) );
    pro.Rbg[1] = exp( -mat.Brg[1]/8.314/(T+273.0) );
    pro.An[1] = exp( -mat.Qan[1]/8.314/(T+273.0) );
    pro.Abn[1] = exp( -mat.Ban[1]/8.314/(T+273.0) );

    for( int y = 1; y < height-1; y++ )
    {
        for( int x = 1; x < width-1; x++ )
        {
            Position( x, y );
            B = 0;
            if( oldarray[C].O.l != oldarray[N].O.l ) B++;
            if( oldarray[C].O.l != oldarray[S].O.l ) B++;
            if( oldarray[C].O.l != oldarray[W].O.l ) B++;
            if( oldarray[C].O.l != oldarray[E].O.l ) B++;
            proarray[C] = ( (float)rand() / (float)RAND_MAX ) * pow( pro.Rbg[oldarray[C].P], (float)B );
        }
    }
}

int Automata::DifferentNeighbour( void )
{
    int count = 0;
    if( oldarray[C].O.l != oldarray[N].O.l ) count++;
    if( oldarray[C].O.l != oldarray[S].O.l ) count++;
    if( oldarray[C].O.l != oldarray[W].O.l ) count++;
    if( oldarray[C].O.l != oldarray[E].O.l ) count++;
    return( count );
}

int Automata::DeformedNeighbour( void )
{
    int count = 0;
    if( oldarray[N].D == 1 ) count++;
    if( oldarray[S].D == 1 ) count++;
    if( oldarray[W].D == 1 ) count++;
    if( oldarray[E].D == 1 ) count++;
    return( count );
}

int Automata::PhaseNeighbour( void )
{
    int count = 0;
    if( oldarray[C].P == oldarray[N].P ) count++;
    if( oldarray[C].P == oldarray[S].P ) count++;
    if( oldarray[C].P == oldarray[W].P ) count++;
    if( oldarray[C].P == oldarray[E].P ) count++;
    return( count );
}

void Automata::AllotropicNucleation( void )
{
    float GE;
    if( T <= mat.Ta && oldarray[C].P == 0 ) GE = 0;
    if( T <= mat.Ta && oldarray[C].P == 1 ) GE = mat.Gg[0] * ( 1.0 - exp( - mat.Kg[0] * ( mat.Ta - T ) ) );
    if( T >  mat.Ta && oldarray[C].P == 1 ) GE = 0;
    if( T >  mat.Ta && oldarray[C].P == 0 ) GE = mat.Gg[1] * ( 1.0 - exp( - mat.Kg[1] * ( T - mat.Ta ) ) );
    float Pdf = exp( -GE/8.314/(T+273.0) );

    float P = ( (float)rand() / (float)RAND_MAX ) *
              Pdf *
              pow( pro.Abn[oldarray[C].P], (float)DifferentNeighbour() );
    if( oldarray[C].D == 1 ) P = P * pro.Se;

    if( GE > 0.0 && PhaseNeighbour() == 4 && pro.An[oldarray[C].P] > P )
    {
        newarray[C].O.c[0] = 1 + rand() % 255;
        newarray[C].O.c[1] = 1 + rand() % 255;
        newarray[C].O.c[2] = 1 + rand() % 255;
        newarray[C].D = 0;
        if( oldarray[C].P == 0 ) newarray[C].P = 1;
        if( oldarray[C].P == 1 ) newarray[C].P = 0;
    }
}

void Automata::RecrystallisationNucleation( void )
{

    float P = ( (float)rand() / (float)RAND_MAX ) * pro.Se * pow( pro.Rbn[oldarray[C].P], (float)DifferentNeighbour() );
    if( oldarray[C].D == 1 && DeformedNeighbour() == 4 && PhaseNeighbour() == 4 && pro.Rn[oldarray[C].P] > P )
    {
        newarray[C].O.c[0] = 1 + rand() % 255;
        newarray[C].O.c[1] = 1 + rand() % 255;
        newarray[C].O.c[2] = 1 + rand() % 255;
        newarray[C].D = 0;
        newarray[C].P = oldarray[C].P;
    }
}

void Automata::AllotropicGrowth( void )
{
    float GE;
    if( T <= mat.Ta && oldarray[C].P == 0 ) GE = 0;
    if( T <= mat.Ta && oldarray[C].P == 1 ) GE = mat.Gg[0] * ( 1.0 - exp( - mat.Kg[0] * ( mat.Ta - T ) ) );
    if( T >  mat.Ta && oldarray[C].P == 1 ) GE = 0;
    if( T >  mat.Ta && oldarray[C].P == 0 ) GE = mat.Gg[1] * ( 1.0 - exp( - mat.Kg[1] * ( T - mat.Ta ) ) );
    float Pdf = exp( -GE/8.314/(T+273.0) );

    float P = ( (float)rand() / (float)RAND_MAX ) *
              Pdf *
              pow( pro.Abg, (float)(4-PhaseNeighbour()) );
    if( oldarray[C].D == 1 ) P = P * pro.Se;

    float max = 0.0;
    if( GE > 0.0 && PhaseNeighbour() < 4 && pro.Ag > P )
    {
        if( proarray[N] > max && oldarray[N].D == 0 && oldarray[N].P != oldarray[C].P )
        {
            newarray[C] = oldarray[N];
            max = proarray[N];
        }
        if( proarray[S] > max && oldarray[S].D == 0 && oldarray[S].P != oldarray[C].P )
        {
            newarray[C] = oldarray[S];
            max = proarray[S];
        }
        if( proarray[W] > max && oldarray[W].D == 0 && oldarray[W].P != oldarray[C].P )
        {
            newarray[C] = oldarray[W];
            max = proarray[W];
        }
        if( proarray[E] > max && oldarray[E].D == 0 && oldarray[E].P != oldarray[C].P )
        {
            newarray[C] = oldarray[E];
            max = proarray[E];
        }
    }
}

void Automata::RecrystallisationGrowth( void )
{
    float P = proarray[C] * pro.Se;
    float max = 0.0;
    if( oldarray[C].D == 1 && DeformedNeighbour() < 4 && pro.Rg[oldarray[C].P] > P )
    {
        if( proarray[N] > max && oldarray[N].D == 0 && oldarray[N].P == oldarray[C].P )
        {
            newarray[C] = oldarray[N];
            max = proarray[N];
        }
        if( proarray[S] > max && oldarray[S].D == 0 && oldarray[S].P == oldarray[C].P )
        {
            newarray[C] = oldarray[S];
            max = proarray[S];
        }
        if( proarray[W] > max && oldarray[W].D == 0 && oldarray[W].P == oldarray[C].P )
        {
            newarray[C] = oldarray[W];
            max = proarray[W];
        }
        if( proarray[E] > max && oldarray[E].D == 0 && oldarray[E].P == oldarray[C].P )
        {
            newarray[C] = oldarray[E];
            max = proarray[E];
        }
    }
}

void Automata::GrainCoarsening( void )
{
    float max = proarray[C];
    if( DeformedNeighbour() == 0 && oldarray[C].D == 0 && PhaseNeighbour() == 4 && pro.Co[oldarray[C].P] > proarray[C] )
    {
        if( oldarray[C].O.l != oldarray[N].O.l && proarray[N] > max )
        {
            newarray[C] = oldarray[N];
            max = proarray[N];
        }
        if( oldarray[C].O.l != oldarray[S].O.l && proarray[S] > max )
        {
            newarray[C] = oldarray[S];
            max = proarray[S];
        }
        if( oldarray[C].O.l != oldarray[W].O.l && proarray[W] > max )
        {
            newarray[C] = oldarray[W];
            max = proarray[W];
        }
        if( oldarray[C].O.l != oldarray[E].O.l && proarray[E] > max )
        {
            newarray[C] = oldarray[E];
            max = proarray[E];
        }
    }
}

void Automata::Step( float Ti )
{
    T = Ti;
    Probabilities();
    BoundaryCondition();
    for( int y = 1; y < height-1; y++ )
    {
        for( int x = 1; x < width-1; x++ )
        {
            Position( x, y );
            GrainCoarsening();
        }
    }
    Update();
    Probabilities();
    BoundaryCondition();
    for( int y = 1; y < height-1; y++ )
    {
        for( int x = 1; x < width-1; x++ )
        {
            Position( x, y );
            RecrystallisationGrowth();
            RecrystallisationNucleation();
        }
    }
    Update();

    Probabilities();
    BoundaryCondition();
    for( int y = 1; y < height-1; y++ )
    {
        for( int x = 1; x < width-1; x++ )
        {
            Position( x, y );
            AllotropicGrowth();
            AllotropicNucleation();
        }
    }
    Update();
    PlotImage();
}

void Automata::PlotImage( void )
{
    int position = 0;
    int keycode;
    unsigned char *ocvdata = (unsigned char *)ocvimage->imageData;
    for( int y = 0; y < height; y ++ )
    {
        for( int x = 0; x < width; x ++ )
        {
            ocvdata[position++] = oldarray[y*width+x].O.c[0];
            ocvdata[position++] = oldarray[y*width+x].O.c[1];
            ocvdata[position++] = oldarray[y*width+x].O.c[2];
        }
    }
    cvShowImage( "CA", ocvimage );
    keycode = (char)cvWaitKey( 100 );
}

void Automata::SaveImage( char *path, int cycle, int step )
{
    char text[1024];
    sprintf( text, "%s_%d_%d.bmp", path, cycle, step );
    cvSaveImage( text, ocvimage );
}

void Automata::StructureInit( void )
{
    int x, y;
    for( int i = 0; i < width * height; i++ )
    {
        newarray[i].O.c[0]  = 0;
        newarray[i].O.c[1]  = 0;
        newarray[i].O.c[2]  = 0;
        newarray[i].D = 0;
        newarray[i].P = 0;
    }
    for( int i = 0; i < str.Gr; i++ )
    {
        x = 1 + rand() % ( width - 1 );
        y = 1 + rand() % ( height - 1 );
        newarray[y*width+x].O.c[0] = 1 + rand() % 255;
        newarray[y*width+x].O.c[2] = 1 + rand() % 255;
        newarray[y*width+x].D = 1;
    }
}

void Automata::StructureGrowth( void )
{
    float P;
    int neighbor;
    if( oldarray[C].D == 0 )
    {
        P = 0;
        if( oldarray[N].D == 1 )
        {
            P = str.V;
            neighbor = N;
        }
        if( oldarray[S].D == 1 )
        {
            P = str.V;
            neighbor = S;
        }
        if( oldarray[E].D == 1 )
        {
            P = str.H;
            neighbor = E;
        }
        if( oldarray[W].D == 1 )
        {
            P = str.H;
            neighbor = W;
        }
        if( ( (float)rand() / (float)RAND_MAX ) < P )
        {
            newarray[C] = oldarray[neighbor];
        }
    }
}

int Automata::StructureMeasure( void )
{
    int F = 0;
    for( int i = 0; i < width*height; i++ )
    {
        if( oldarray[i].D == 1 ) F++;
    }
    return( F );
}

void Automata::StructureCreate( Structure istr )
{
    str = istr;
    StructureInit();
    str.H = 0.9;
    str.V = exp( -12.77 * str.q + 3.4134 );
    while( StructureMeasure() < width*height )
    {
        for( int y = 1; y < height-1; y++ )
        {
            for( int x = 1; x < width-1; x++ )
            {
                Position( x, y );
                StructureGrowth();
            }
        }
        BoundaryCondition();
        Update();
        PlotImage();
    }
    for( int i = 0; i < width*height; i++ )
    {
        oldarray[i].D = str.Dg;
        oldarray[i].P = str.Ph;
        newarray[i].D = str.Dg;
        newarray[i].P = str.Ph;
    }
}

float Automata::MeasureRecrFraction( void )
{
    int F = 0;
    for( int y = 0; y < height; y ++ )
    {
        for( int x = 0; x < width; x ++ )
        {
            if( oldarray[y*width+x].D == 0 ) F++;
        }
    }
    return( (float)F / (float)( width*height ) );
}

float Automata::MeasureAlphaFraction( void )
{
    int F = 0;
    for( int y = 0; y < height; y ++ )
    {
        for( int x = 0; x < width; x ++ )
        {
            if( oldarray[y*width+x].P == 0 ) F++;
        }
    }
    return( (float)F / (float)( width*height ) );
}

State* Automata::GetUniverse( void )
{
    return( oldarray );
}

void Automata::CreateVideo( char *path, int ex )
{
    char text[1024];
    sprintf( text, "%s_%d.avi", path, ex );
    CvSize ocvsize;
    ocvsize.width = width;
    ocvsize.height = height;
    ocvvideo = cvCreateVideoWriter( text, CV_FOURCC( 'x', 'v', 'i', 'd'), 10, ocvsize, 1 );
}

void Automata::AddFrameVideo( void )
{
    cvWriteFrame( ocvvideo, ocvimage );
}

void Automata::DestroyVideo( void )
{
    cvReleaseVideoWriter( &ocvvideo );
}

bool Automata::SaveStructureLog( char *path, int i )
{
    char filename[1024];

    sprintf( filename, "%s_%d_structure.log", path, i );
    FILE *file = fopen( filename, "wt" );
    if( !file ) return( false );
    fprintf( file, "width\t%d\n", width );
    fprintf( file, "height\t%d\n", height );
    fprintf( file, "grains\t%d\n", str.Gr );
    fprintf( file, "deformation\t%.2f\n", str.q );
    fprintf( file, "Is deformed\t%d\n", str.Dg );
    fprintf( file, "Phase\t%d\n", str.Ph );
    fclose( file );
    return( true );
}

bool Automata::SaveMaterialLog( char *path )
{
    char filename[1024];

    sprintf( filename, "%s_material.log", path );
    FILE *file = fopen( filename, "wt" );
    if( !file ) return( false );
    fprintf( file, "Tall\t%.2f\n", mat.Ta );
    fprintf( file, "Qallgrowth\t%.2f\n", mat.Qag );
    fprintf( file, "Ballgrowth\t%.2f\n", mat.Bag );
    fprintf( file, "Estored\t%.2f\n", mat.Es );
    fprintf( file, "Phase 0 (T<Tall)\n");
    fprintf( file, "\tQallnucleation\t%.2f\n", mat.Qan[0] );
    fprintf( file, "\tBallnucleation\t%.2f\n", mat.Ban[0] );
    fprintf( file, "\tQrexnucleation\t%.2f\n", mat.Qrn[0] );
    fprintf( file, "\tBrexnucleation\t%.2f\n", mat.Brn[0] );
    fprintf( file, "\tQrexgrowth\t%.2f\n", mat.Qrg[0] );
    fprintf( file, "\tBrexgrowth\t%.2f\n", mat.Brg[0] );
    fprintf( file, "\tQcoarsening\t%.2f\n", mat.Qc[0] );
    fprintf( file, "\tGgibbs\t%.2f\n", mat.Gg[0] );
    fprintf( file, "\tKgibbs\t%.2f\n", mat.Kg[0] );
    fprintf( file, "Phase 1 (T>Tall)\n");
    fprintf( file, "\tQallnucleation\t%.2f\n", mat.Qan[1] );
    fprintf( file, "\tBallnucleation\t%.2f\n", mat.Ban[1] );
    fprintf( file, "\tQrexnucleation\t%.2f\n", mat.Qrn[1] );
    fprintf( file, "\tBrexnucleation\t%.2f\n", mat.Brn[1] );
    fprintf( file, "\tQrexgrowth\t%.2f\n", mat.Qrg[1] );
    fprintf( file, "\tBrexgrowth\t%.2f\n", mat.Brg[1] );
    fprintf( file, "\tQcoarsening\t%.2f\n", mat.Qc[1] );
    fprintf( file, "\tGgibbs\t%.2f\n", mat.Gg[1] );
    fprintf( file, "\tKgibbs\t%.2f\n", mat.Kg[1] );
    fclose( file );
    return( true );
}
