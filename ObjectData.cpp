#include <stdlib.h>
#include <stdio.h>

#include "ObjectData.h"

//---------------------------------------------------------------
// Object descriptor

ObjectDescriptor::ObjectDescriptor()
{
    Nc = 0;
    cx = NULL;
    cy = NULL;
}

void ObjectDescriptor::DeleteContur( void )
{
    if( cx ) delete []cx;
    cx = NULL;
    if( cy ) delete []cy;
    cy = NULL;
}

void ObjectDescriptor::AllocateContur( void )
{
    cx = new int[ Nc ];
    cy = new int[ Nc ];
}

//---------------------------------------------------------------
// Object data

ObjectData::ObjectData( void )
{
    n = 0;
    data = NULL;
}

void ObjectData::Allocate( int cnt )
{
    n = cnt;
    Destroy();
    data = new ObjectDescriptor[ n ];
}

void ObjectData::Destroy( void )
{
    if( data )
    {
        for( int i = 0; i < n; i++ ) data[i].DeleteContur();
        delete []data;
    }
    data = NULL;
}

bool ObjectData::SaveFile( char *pFilename )
{
    FILE *file = fopen( pFilename, "wt" );
    if( !file ) return( false );
    fprintf( file, "szemcsszam:\t%d", n - 1 );
    fprintf( file, "szemcse\tA\tD\tP\tdef\tphase\n" );
    for( int i = 1; i < n; i++ )
    {
        fprintf( file, "%d\t%.2f\t%.2f\t%.2f\t%d\t%d\n", i, data[i].A, data[i].D, data[i].P, data[i].Dg, data[i].Ph );
    }
    fclose( file );
    return( true );
}
