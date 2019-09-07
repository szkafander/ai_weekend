#include "CprobImage.h"

// this is probably irrelevant. we'll use some clever binary morphology tricks
// to do this. I'll skip for now.

void CprobImage::Init( int W, int H )
{
    width = W;
    height = H;

    bin = new int[ width * height ];
    obj = new int[ width * height ];

    cvInitFont( &font, CV_FONT_HERSHEY_SIMPLEX, 0.3, 0.3, 0, 1, 8 );
    cvNamedWindow( "CPROB", 1 );
    CvSize ocvsize;
    ocvsize.width = width;
    ocvsize.height = height;
    ocvimage = cvCreateImage( ocvsize, IPL_DEPTH_8U, 3 );
}

void CprobImage::Destroy( void )
{
    delete []bin;
    delete []obj;
    od.Destroy();
    cvReleaseImage( &ocvimage );
    cvDestroyWindow( "CPROB" );
}

void CprobImage::ConvertUniverse( State *carray )
{
    for( int i = 0; i < width * height; i++ ) bin[i] = 255;
    for( int y = 0; y < height - 1; y++ )
    {
        for( int x = 0; x < width - 1; x++ )
        {
            if( carray[y*width+x].O.l != carray[y*width+(x+1)].O.l )     bin[y*width+x] = 0;
            if( carray[y*width+x].O.l != carray[(y+1)*width+x].O.l )     bin[y*width+x] = 0;
            if( carray[y*width+x].O.l != carray[(y+1)*width+(x+1)].O.l ) bin[y*width+x] = 0;
            if( carray[y*width+x].O.l != carray[(y+1)*width+(x-1)].O.l ) bin[y*width+x] = 0;
        }
    }


    int position = 0;
    int keycode;
    unsigned char *ocvdata = (unsigned char *)ocvimage->imageData;
    for( int y = 0; y < height; y ++ )
    {
        for( int x = 0; x < width; x ++ )
        {
            if( bin[y*width+x] == 255 )
            {
                ocvdata[position++] = 255;
                ocvdata[position++] = 0;
                ocvdata[position++] = 0;
            }
            else
            {
                ocvdata[position++] = 0;
                ocvdata[position++] = 0;
                ocvdata[position++] = 0;
            }
        }
    }
    cvShowImage( "CPROB", ocvimage );
    keycode = (char)cvWaitKey( 1000 );
}

void CprobImage::LabelsFast( int areamin )
{
    int N = 0;
    for( int i = 0; i < width*height; i++ ) obj[i] = 0;
    for( int y = 1; y < height - 1; y++ )
    {
        for( int x = 1; x < width - 1; x++ )
        {
            if( obj[ y*width+x ] == 0 && bin[ y*width+x ] == 255 )
            {
                N++;
                obj[ y*width+x ] = N;
                while( bin[y*width+x] == 255 && x < width )
                {
                    obj[ y*width+x ] = N;
                    x++;
                }
            }
        }
    }
    N++;

    bool *neighbour = new bool[N*N];
    int *list = new int[N];
    int *T = new int[N];
    bool wr = true;
    bool event = true;

    while( wr )
    {
        wr = false;
        for( int i = 0; i < N*N; i++ ) neighbour[i] = false;
        for( int y = 1; y < height - 1; y++ )
        {
            for( int x = 1; x < width - 1; x++ )
            {
                neighbour[ obj[ y*width+(x+1) ] * N + obj[ y*width+x ] ] = true;
                neighbour[ obj[ y*width+x ] * N + obj[ y*width+(x+1) ] ] = true;
                neighbour[ obj[ y*width+(x-1) ] * N + obj[ y*width+x ] ] = true;
                neighbour[ obj[ y*width+x ] * N + obj[ y*width+(x-1) ] ] = true;
                neighbour[ obj[ (y+1)*width+x ] * N + obj[ y*width+x ] ] = true;
                neighbour[ obj[ y*width+x ] * N + obj[ (y+1)*width+x ] ] = true;
                neighbour[ obj[ (y-1)*width+x ] * N + obj[ y*width+x ] ] = true;
                neighbour[ obj[ y*width+x ] * N + obj[ (y-1)*width+x ] ] = true;
            }
        }
        for( int x = 0; x < N; x++ ) list[x] = x;
        for( int x = N - 1; x > 0; x-- )
        {
            for( int u = x - 1; u > 0; u-- )
            {
                if( neighbour[ x * N + u ] ) list[x] = u;
            }
        }
        event = true;
        while( event )
        {
            event = false;
            for( int x = N - 1; x > 0; x-- )
            {
                if( list[ list[x] ] < list[x] )
                {
                    list[x] = list[ list[x] ];
                    event = true;
                    wr = true;
                }
            }
        }
        for( int x = 0; x < N; x++ ) T[x] = 0;
        for( int y = 1; y < height - 1; y++ )
        {
            for( int x = 1; x < width - 1; x++ )
            {
                obj[ y*width+x ] = list[ obj[ y*width+x ] ];
                T[ obj[ y*width+x ] ]++;
            }
        }
    }

    for( int y = 1; y < height - 1; y++ )
    {
        if( obj[ y * width + 1 ] != 0 )         T[ obj[ y * width + 1 ] ] = 0;
        if( obj[ y * width + width - 2 ] != 0 ) T[ obj[ y * width + width - 2 ] ] = 0;
    }
    for( int x = 1; x < width - 1; x++ )
    {
        if( obj[ width + x ] != 0 )                  T[ obj[ width + x ] ] = 0;
        if( obj[ ( height - 2 ) * width + x ] != 0 ) T[ obj[ ( height - 2 ) * width + x ] ] = 0;
    }
    for( int y = 1; y < height - 1; y++ )
    {
        if( obj[ y * width + 2 ] != 0 )         T[ obj[ y * width + 2 ] ] = 0;
        if( obj[ y * width + width - 3 ] != 0 ) T[ obj[ y * width + width - 3 ] ] = 0;
    }
    for( int x = 1; x < width - 1; x++ )
    {
        if( obj[ 2 * width + x ] != 0 )              T[ obj[ 2 * width + x ] ] = 0;
        if( obj[ ( height - 3 ) * width + x ] != 0 ) T[ obj[ ( height - 3 ) * width + x ] ] = 0;
    }

    int max = 0;
    for( int x = 0; x < N; x++ ) list[x] = 0;
    for( int x = 1; x < N; x++ )
    {
        if( T[x] > areamin )
        {
            max++;
            list[x] = max;
        }
    }
    for( int y = 0; y < height; y++ )
    {
        for( int x = 0; x < width; x++ )
        {
            obj[ y*width+x ] = list[ obj[ y*width+x ] ];
            if( obj[ y*width+x ] == 0 && bin[ y*width+x ] == 255 ) bin[ y*width+x ] = 0;
        }
    }

    od.Destroy();
    od.Allocate( max + 1 );

    delete []neighbour;
    delete []list;
    delete []T;
}

void CprobImage::SearchObjects( void )
{
	for( int i = 0; i < od.n; i++ )
	{
		od.data[i].xmin = width;
		od.data[i].xmax = 0;
		od.data[i].ymin = height;
		od.data[i].ymax = 0;
	}
    for( int y = 0; y < height; y++ )
    {
        for( int x = 0; x < width; x++ )
        {
            if( x < od.data[ obj[ y*width+x ] ].xmin ) od.data[ obj[ y*width+x ] ].xmin = x;
            if( x > od.data[ obj[ y*width+x ] ].xmax ) od.data[ obj[ y*width+x ] ].xmax = x;
            if( y < od.data[ obj[ y*width+x ] ].ymin ) od.data[ obj[ y*width+x ] ].ymin = y;
            if( y > od.data[ obj[ y*width+x ] ].ymax ) od.data[ obj[ y*width+x ] ].ymax = y;
        }
    }

    int position = 0;
    int keycode;
    unsigned char *ocvdata = (unsigned char *)ocvimage->imageData;
    for( int y = 0; y < height; y ++ )
    {
        for( int x = 0; x < width; x ++ )
        {
            if( bin[y*width+x] == 255 )
            {
                ocvdata[position++] = 255;
                ocvdata[position++] = 0;
                ocvdata[position++] = 0;
            }
            else
            {
                ocvdata[position++] = 0;
                ocvdata[position++] = 0;
                ocvdata[position++] = 0;
            }
        }
    }
    char text[8];
    CvPoint p;
	for( int i = 1; i < od.n; i++ )
	{
        p.x = od.data[i].xmin + ( od.data[i].xmax - od.data[i].xmin ) / 2;
        p.y = od.data[i].ymin + ( od.data[i].ymax - od.data[i].ymin ) / 2;
        sprintf( text, "%d", i );
        cvPutText( ocvimage, text, p, &font, CV_RGB( 255, 0, 0 ) );
	}
    cvShowImage( "CPROB", ocvimage );
    keycode = (char)cvWaitKey( 1000 );
}

void CprobImage::MeasureArea( void )
{
    for( int i = 0; i < od.n; i++ ) od.data[i].A = 0;
    for( int i = 0; i < width*height; i++ ) od.data[ obj[i] ].A = od.data[ obj[i] ].A + 1.0;
}

bool CprobImage::IsConturPixel( int x, int y, int o )
{
    bool event;
    event = false;
    if( obj[y*width+x] == o )
    {
        if( obj[ (y-1)*width+x ] != o ) event = true;
        if( obj[ y*width+(x-1) ] != o ) event = true;
        if( obj[ y*width+(x+1) ] != o ) event = true;
        if( obj[ (y+1)*width+x ] != o ) event = true;
    }
    return( event );
}

void CprobImage::MeasurePerimeter( void )
{
    for( int i = 0; i < od.n; i++ )
    {
        od.data[i].P = 0;
        od.data[i].Nc = 0;
    }
    for( int i = 1; i < od.n; i++ )
    {
        od.data[i].DeleteContur();
        for( int y = od.data[i].ymin; y <= od.data[i].ymax; y++ )
        {
            for( int x = od.data[i].xmin; x <= od.data[i].xmax; x++ )
            {
                if( IsConturPixel( x, y, i ) )
                {
                    if( IsConturPixel( x-1, y-1, i ) ) od.data[i].P += sqrt( 2.0 );
                    if( IsConturPixel( x-1, y  , i ) ) od.data[i].P += 1.0;
                    if( IsConturPixel( x-1, y+1, i ) ) od.data[i].P += sqrt( 2.0 );
                    if( IsConturPixel( x  , y+1, i ) ) od.data[i].P += 1.0;
                    od.data[i].Nc++;
                }
            }
        }
        od.data[i].AllocateContur();
    }
    int j = 0;
    for( int i = 1; i < od.n; i++ )
    {
        j = 0;
        for( int y = od.data[i].ymin; y <= od.data[i].ymax; y++ )
        {
            for( int x = od.data[i].xmin; x <= od.data[i].xmax; x++ )
            {
                if( IsConturPixel( x, y, i ) )
                {
                    od.data[i].cx[j] = x;
                    od.data[i].cy[j] = y;
                    j++;
                }
            }
        }
    }
}

void CprobImage::MeasureDiameter( void )
{
    float max;
    float d;

    for( int o = 1; o < od.n; o++ )
    {
        if( od.data[o].Nc > 2 )
        {
            max = 1.0;
            od.data[o].D = 1.0;
            for( int i = 0; i < od.data[o].Nc - 1; i++ )
            {
                for( int j = i+1; j < od.data[o].Nc; j++ )
                {
                    d = ( od.data[o].cx[j] - od.data[o].cx[i] ) *
                        ( od.data[o].cx[j] - od.data[o].cx[i] ) +
                        ( od.data[o].cy[j] - od.data[o].cy[i] ) *
                        ( od.data[o].cy[j] - od.data[o].cy[i] );
                    if( d > max )
                    {
                        max = d;
                        od.data[o].D = sqrt( max );
                    }
                }
            }
        }
        else od.data[o].D = 1.0;
    }
}

void CprobImage::AddStateLabels( State *array )
{
    for( int i = 0; i < width*height; i++ )
    {
        od.data[ obj[i] ].Dg = array[i].D;
        od.data[ obj[i] ].Ph = array[i].P;
    }
}

void CprobImage::Measure( State *array, char *project, int ex, int step )
{
    ConvertUniverse( array );
    LabelsFast( 5 );
    SearchObjects();
    MeasureArea();
    MeasurePerimeter();
    MeasureDiameter();
    AddStateLabels( array );
    char filename[1024];
    sprintf( filename, "%s_%d_%d.txt", project, ex, step );
    if( !od.SaveFile( filename ) ) printf( "\tA mert adatok mentese nem sikerult!" );
}
