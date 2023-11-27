#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

#------------------------------------------------------------------
# Everything that can be visible to the world.
#  
__all__ = [ 'corigin' ]

#------------------------------------------------------------------
# Import from...
#  
from dataclasses import dataclass
from numpy import linalg as LA
from pyConics.tolerance import ctol

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
# Import as...
#  
import numpy as np

#------------------------------------------------------------------
# Data Class Origin.
#  
@dataclass
class Origin:
    x: float = 0.0
    y: float = 0.0

    def change_point( self, point: np.ndarray ) -> np.ndarray:
        return point - np.array( ( self.x, self.y, 0.0 ) )
    
    def change_line( self, line: np.ndarray ) -> np.ndarray:
        c = ( line[ 0 ] * self.x ) + ( line[ 1 ] * self.y )
        return line + np.array( ( 0.0, 0.0, c ) )

    def change_conic( self, conic: np.ndarray ) -> np.ndarray:
        from pyConics.point import CPoint

        # Get the matrices and vectors.
        ABC = conic[ 0 : 2, 0 : 2 ]
        DE = conic[ 2 : 3, 0 : 2 ].T
        
        # Get the center of the conic.
        xy_o = ( -1 * LA.inv( ABC ) ) @ DE

        # Create a point to shift origin.
        o = CPoint( ( xy_o[ 0 ] [ 0 ], xy_o[ 1 ][ 0 ] ) )
        o.update_origin()

        # Rebuild the matrix.
        o = np.array( [ o.x, o.y ] )[np.newaxis].T
        DE = ( -1 * ABC ) @ o
        F = ( o.T @ ABC @ o ) - 1

        # Build the matrix representation of a conic.
        return ctol.adjust2relzeros( np.block( [ [ ABC, DE ], [ DE.T, F ] ] ) )

    def reset( self ) -> None:
        self.x = 0.0
        self.y = 0.0

    @property
    def coord( self ) -> tuple[ float, float ]:
        return ( self.x, self.y )

    @coord.setter
    def coord( self, coord: tuple[ float, float ] ) -> None:
        self.x = coord[ 0 ]
        self.y = coord[ 1 ]

#--------------------------------------------------------------
# Global variable.
#
corigin = Origin()

#------------------------------------------------------------------
# For development and test.
#  
if __name__ == '__main__':
    o = Origin()
    print( o.coord )
    o.x = 1.0
    o.y = 2.0
    print( o.coord )
    o.coord = ( 0.0, 0.0 )
    print( o.coord )
