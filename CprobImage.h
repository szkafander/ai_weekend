#ifndef CPROB_IMAGE_H
#define CPROB_IMAGE_H

#include <cv.h>
#include <highgui.h>

#include "ObjectData.h"
#include "state.h"

class CprobImage
{
  public:
    void Init( int, int );
    void Destroy( void );

    void Measure( State*, char*, int, int );

  private:
    bool IsConturPixel( int, int, int );

    void ConvertUniverse( State * );
    void LabelsFast( int );
    void SearchObjects( void );
    void MeasureArea( void );
    void MeasurePerimeter( void );
    void MeasureDiameter( void );
    void AddStateLabels( State * );

    int width;
    int height;
    int *bin;
    int *obj;

    ObjectData od;

    IplImage* ocvimage;
    CvFont font;
};

#endif
