#ifndef CPROB_OBJECTDATA_H
#define CPROB_OBJECTDATA_H

class ObjectDescriptor
{
  public:
    ObjectDescriptor();

    void AllocateContur( void );
    void DeleteContur( void );

    int xmin;
    int xmax;
    int ymin;
    int ymax;
    int xid;
    int yid;

    int Nc;
    int *cx;
    int *cy;

    float A;
    float P;
    float D;

    int Dg;
    int Ph;
};

class ObjectData
{
  public:
    ObjectData( void );
    void Allocate( int );
    void Destroy( void );
    bool SaveFile( char * );

    ObjectDescriptor *data;
    int n;
};

#endif
