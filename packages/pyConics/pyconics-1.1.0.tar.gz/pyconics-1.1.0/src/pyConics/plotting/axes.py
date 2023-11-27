#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'CAxes' ]

#------------------------------------------------------------------
# Import from ...
#
from pyConics.constants import cconst
from pyConics.errors import CValueError, CTypeError
from matplotlib import pyplot as plt
from pyConics import CPoint, CLine
from pyConics.conics import CConic
from pyConics.plotting.utils import CPoint2CoordXY, CLine2MatrixXY
from pyConics.plotting.utils import CPointList2MatrixXY, CLineList2MatrixXY

#------------------------------------------------------------------
# Import from...
# We use here TYPE_CHECKING constant to avoid circular import  
# exceptions.
#
from typing import TYPE_CHECKING
if TYPE_CHECKING:
   ... # Do nothing here, because there are no pyConics modules
       # here to be imported.    

#------------------------------------------------------------------
# Import as ...
#  
import numpy as np

#------------------------------------------------------------------
# Class CFigure.
#  
class CAxes:
    def __init__( self, axes: plt.Axes ) -> None: #type: ignore
        self._axes = axes

    def __repr__( self ) -> str:
        _arts = self._axes.findobj( None )
        return f'{self.__class__.__name__} class with {len( _arts )} objects.'

    def get_pyplot_axes( self ) -> plt.Axes: #type: ignore
        return self._axes

    @property
    def xlim( self ) -> tuple[ float, float ]:
        return self._axes.get_xlim()
     
    @xlim.setter
    def xlim( self, xl: tuple[ float, float ] ) -> None:
        self._axes.set_xlim( xl )

    @property
    def ylim( self ) -> tuple[ float, float ]:
        return self._axes.get_ylim()
    
    @ylim.setter
    def ylim( self, yl: tuple[ float, float ] ) -> None:
        self._axes.set_ylim( yl )
    
    @property
    def xticks( self ) -> np.ndarray:
        return self._axes.get_xticks()
    
    @xticks.setter
    def xticks( self, xt: np.ndarray ) -> None:
        self._axes.tick_params( axis = 'x', labelsize = cconst.tickssize )
        self._axes.set_xticks( xt )

    @property
    def yticks( self ) -> np.ndarray:
        return self._axes.get_yticks()
    
    @yticks.setter
    def yticks( self, yt: np.ndarray ) -> None:
        self._axes.tick_params( axis = 'y', labelsize = cconst.tickssize )
        self._axes.set_yticks( yt )

    @property
    def title( self ) -> str:
        return self._axes.get_title()
    
    @title.setter
    def title( self, title: str ) -> None:
        self._axes.set_title( title, fontsize = cconst.titlesize )

    @property
    def xlabel( self ) -> str:
        return self._axes.get_xlabel()
    
    @xlabel.setter
    def xlabel( self, label: str ) -> None:
        self._axes.set_xlabel( label, fontsize = cconst.labelsize )

    @property
    def ylabel( self ) -> str:
        return self._axes.get_ylabel()
    
    @ylabel.setter
    def ylabel( self, label: str ) -> None:
        self._axes.set_ylabel( label, fontsize = cconst.labelsize )

    def text( self, x: float, y: float, txt: str, **kwargs ) -> None:
        if( not 'fontsize' in kwargs.keys() ):
            kwargs[ 'fontsize' ] = cconst.textsize

        # Call Axes.text() method.
        self._axes.text( x, y, txt, kwargs )
        
    def plot( self, *args,
              clinesamples: int = 11,
              cconicsamples: tuple[ int, int ] = ( 51, 51 ),
              **kwargs ) -> None:
        new_args = [] # new arguments to be passed into axes.plot.

        # Search for a CPoint, a CLine, a lists of them, or a CConic.
        for arg in args:
            if ( isinstance( arg, CPoint ) ):
                # Convert a CPoint to a XY-coord.
                xy = CPoint2CoordXY( arg )
                new_args.append( xy[ 0 ] )
                new_args.append( xy[ 1 ] )
                continue

            if ( isinstance( arg, CLine ) ):
                # Convert a CLine to a (nx2)-matrix.
                xy = CLine2MatrixXY( arg, self.xlim, self.ylim, clinesamples )
                new_args.append( xy[ :, 0 ] )
                new_args.append( xy[ :, 1 ] )
                continue

            if ( isinstance( arg, list ) ):
                # It is a list, but is it a list of CPoint or CLine?
                if ( not _is_cpoint_list( arg ) ) and ( not _is_cline_list( arg ) ):
                    new_args.append( arg )
                    continue

                # Yes. It is a list of CPoint or CLine.
                if ( _is_cpoint_list( arg ) ):
                    # convert the list to a (nx2)-matrix.
                    xy = CPointList2MatrixXY( arg )
                    new_args.append( xy[ :, 0 ] )
                    new_args.append( xy[ :, 1 ] )
                    continue

                if ( _is_cline_list( arg ) ):
                    # convert the list to a list of (nxm)-matrix.
                    xy = CLineList2MatrixXY( arg, self.xlim, self.ylim, clinesamples )
                    new_args.append( xy[ 0 ] )
                    new_args.append( xy[ 1 ] )
                    continue

            if ( isinstance( arg, CConic ) ):
                # Convert a CConic to a tuple of tuples.
                C: CConic = arg
                x = np.linspace( self.xlim[ 0 ], self.xlim[ 1 ], cconicsamples[ 0 ] )
                y = np.linspace( self.ylim[ 0 ], self.ylim[ 1 ], cconicsamples[ 1 ] )

                if ( C.is_degenerate ):
                    # Degenerate conic.
                    lp1, lp2 = C.sequence( list( x ) )

                    # Get the first list of points.
                    xy1 = CPointList2MatrixXY( list( lp1 ) )

                    # Get the second list of points.
                    xy2 = CPointList2MatrixXY( list( lp2 ) )

                    # Build the list of x and y.
                    x1 = xy1[ :, 0 ][np.newaxis].T
                    y1 = xy1[ :, 1 ][np.newaxis].T
                    x2 = xy2[ :, 0 ][np.newaxis].T
                    y2 = xy2[ :, 1 ][np.newaxis].T
                    dsize = np.abs( x1.size - x2.size )
                    dx = np.full( shape = ( dsize, 1 ), fill_value = cconst.inf )
                    if ( x1.size <= x2.size):
                        x1 = np.block( [ [ x1 ], [ dx ] ] )
                        y1 = np.block( [ [ y1 ], [ dx ] ] )
                    else:
                        x2 = np.block( [ [ x2 ], [ dx ] ] )
                        y2 = np.block( [ [ y2 ], [ dx ] ] )

                    X = list( np.block( [ x1, x2 ] ) )
                    Y = list( np.block( [ y1, y2 ] ) )

                    new_args.append( X )
                    new_args.append( Y )
                    continue
                else:
                    # Nondegenerate conic.
                    # Get the list of points.
                    lst_pts = C.sequence( list( x ), list( y ) )
                    lst_len = len( lst_pts )
                    
                    if ( lst_len == 0 ):
                        continue
                    elif ( lst_len == 1 ):
                        lp1 = lst_pts[ 0 ]
                        lp2 = tuple( [] )
                    else:
                        lp1 = lst_pts[ 0 ]
                        lp2 = lst_pts[ 1 ]

                    # Get the first list of points.
                    xy1 = CPointList2MatrixXY( list( lp1 ) )

                    # Get the second list of points.
                    xy2 = CPointList2MatrixXY( list( lp2 ) )

                    # List of points must exist.
                    if ( ( xy1.size == 0 ) and ( xy2.size == 0 ) ):
                        continue

                    # Build the list of x and y.
                    if ( xy2.size == 0 ):
                        X = list( xy1[ :, 0 ][np.newaxis].T )
                        Y = list( xy1[ :, 1 ][np.newaxis].T )
                    else:
                        x1 = xy1[ :, 0 ][np.newaxis].T
                        y1 = xy1[ :, 1 ][np.newaxis].T
                        x2 = xy2[ :, 0 ][np.newaxis].T
                        y2 = xy2[ :, 1 ][np.newaxis].T
                        dsize = np.abs( x1.size - x2.size )
                        dx = np.full( shape = ( dsize, 1 ), fill_value = cconst.inf )
                        if ( x1.size <= x2.size):
                            x1 = np.block( [ [ x1 ], [ dx ] ] )
                            y1 = np.block( [ [ y1 ], [ dx ] ] )
                        else:
                            x2 = np.block( [ [ x2 ], [ dx ] ] )
                            y2 = np.block( [ [ y2 ], [ dx ] ] )

                        X = list( np.block( [ x1, x2 ] ) )
                        Y = list( np.block( [ y1, y2 ] ) )
                        
                    new_args.append( X )
                    new_args.append( Y )
                    continue

            # It is not a pyConic object.
            new_args.append( arg )

        self._axes.plot( *tuple( new_args ), **kwargs ) # type: ignore

#------------------------------------------------------------------
# Internal functions.
#  
def _is_cpoint_list( arg: list ) -> bool:
    for p in arg:
        if ( not isinstance( p, CPoint ) ):
            return False
    return True

def _is_cline_list( arg: list ) -> bool:
    for l in arg:
        if ( not isinstance( l, CLine ) ):
            return False
    return True

#------------------------------------------------------------------
# For development and test.
#  
if ( __name__  == '__main__' ):
    ...
