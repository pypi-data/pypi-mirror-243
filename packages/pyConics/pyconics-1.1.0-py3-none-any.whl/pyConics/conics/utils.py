#------------------------------------------------------------------
# Import it to be able to pass an object of same class as argument
# to a member function
from __future__ import annotations

# #------------------------------------------------------------------
# # Everything that can be visible to the world.
 
__all__ = [ 'create_conic_from_lines', 'create_conic', 'rank' ]

# #------------------------------------------------------------------
# # Import from...
# #
# from typing import Any
from numpy import linalg as LA

# #------------------------------------------------------------------
# # Import from...
# # We use here TYPE_CHECKING constant to avoid circular import  
# # exceptions.
# #
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     ... # Do nothing here, because there are no pyConics modules
#         # here to be imported.
        
# from pyConics.errors import CTypeError
from pyConics.tolerance import ctol
from pyConics.constants import cconst
from pyConics.point import CPoint
from pyConics.line import CLine

# #------------------------------------------------------------------
# # Import as...
# #
import numpy as np

def create_conic_from_lines( lines: tuple[ CLine, CLine ] ) -> np.ndarray:
    l1 = lines[ 0 ].gform[np.newaxis]
    l2 = lines[ 1 ].gform[np.newaxis].T
    M = ( l2 @ l1 )
    return ctol.adjust2relzeros( M + M.T )

def create_conic( a: float, c: float, center: CPoint, angle: float ) -> np.ndarray:
    # Get the minor axis.
    a2 = a * a
    c2 = c * c
    if ( a >= c ): # it is an ellipse.
        b2 = a2 - c2
    else: # it is a hyperbole.
        b2 = c2 - a2

    # Build a quadratic form for the conic with centered on ( 0, 0 )
    # and without rotation.
    if ( a >= c ): # it is an ellipse.
        C = np.array( [ [ 1.0 / a2, 0.0 ], [ 0.0, 1.0 / b2 ] ] )
    else:
        C = np.array( [ [ 1.0 / a2, 0.0 ], [ 0.0, 1.0 / -b2 ] ] )

    # Build the rotating matrix.
    R = np.array( [ [ np.cos( angle ), np.sin( angle ) ], [ -np.sin( angle ), np.cos( angle ) ] ] )

    # Get the center vector.
    xy_o = center.gform[ 0 : 2 ][np.newaxis].T

    # Create the matrices ABC, DE, and F.
    ABC = ctol.adjust2relzeros( R.T @ C @ R )
    DE = ( -1 * ABC ) @ xy_o
    F = ( xy_o.T @ ABC @ xy_o ) - 1

    # Build the matrix representation of a conic.
    return ctol.adjust2relzeros( np.block( [ [ ABC, DE ], [ DE.T, F ] ] ) )

def rank( M: np.ndarray ) -> int:
    # Determinant of M must be less that its dim.
    nrows, ncols = M.shape
    if ( nrows != ncols ):
        return 0

    n = LA.norm( M )
    if ( ctol.iszero( float( n ) ) ):
        return 0

    if ( not ctol.iszero( LA.det( M ) ) ):
        return nrows

    # Calc rank by using the eigenvalues.
    eigs = LA.eigvalsh( M )
    eigs = ctol.adjust2relzeros( eigs )
    rk: int = 0
    for ev in eigs:
        if ( ev != 0.0 ):
            rk += 1
    return rk

#------------------------------------------------------------------
# For development and test.
#  
if __name__ == '__main__':
    # Keep this imports even there is no test code.
    from pyConics.point import CPoint
    from pyConics.line import CLine
    from pyConics.conics.conic import CConic

    # Degenerate conic.
    f = CLine( ( 1, 0, 1 ) )    
    g = CLine( ( 1, 0, -1 ) )
    C0 = CConic( degenerate = ( f, g ), name = 'C0' )
    print( C0 )
    print( f'Rank of {C0.name}: {C0.rank}.' )
    print( f'Is {C0.name} full rank? {C0.is_fullrank()}' )
    print( f'Is {C0.name} degenerate? {C0.is_degenerate}.\n' )

    # Degenerate conic.
    f = CLine( ( 1, 0, -1 ) )    
    g = CLine( ( 1, 0, -3 ) )
    C1 = CConic( degenerate = ( f, g ), name = 'C1' )
    print( C1 )
    print( f'Rank of {C1.name}: {C1.rank}.' )
    print( f'Is {C1.name} full rank? {C1.is_fullrank()}' )
    print( f'Is {C1.name} degenerate? {C1.is_degenerate}.\n' )

    # Degenerate conic.
    f = CLine( ( 1, -1, -2 ) )    
    g = CLine( ( -1, -1, 2 ) )
    C2 = CConic( degenerate = ( f, g ), name = 'C2' )
    print( C2 )
    print( f'Rank of {C2.name}: {C2.rank}.' )
    print( f'Is {C2.name} full rank? {C2.is_fullrank()}' )
    print( f'Is {C2.name} degenerate? {C2.is_degenerate}.\n' )

    # Degenerate conic.
    f = CLine( ( 1, 0, -2 ) )    
    C3 = CConic( degenerate = ( f, f ), name = 'C3' )
    print( C3 )
    print( f'Rank of {C3.name}: {C3.rank}.' )
    print( f'Is {C3.name} full rank? {C3.is_fullrank()}' )
    print( f'Is {C3.name} degenerate? {C3.is_degenerate}.\n' )

    # Default nondegenerate conic.
    C4 = CConic( name = 'C4' )
    print( C4 )
    print( f'Rank of {C4.name}: {C4.rank}.' )
    print( f'Is {C4.name} full rank? {C4.is_fullrank()}' )
    print( f'Is {C4.name} degenerate? {C4.is_degenerate}.\n' )

    # Nondegenerate conic with a, c, center, and angle.
    C5 = CConic( 2.0, 0.5, 30.0 / 180 * cconst.pi, CPoint( ( 2, 1 ) ), 'C5' )
    print( C5 )
    print( f'Rank of {C5.name}: {C5.rank}.' )
    print( f'Is {C5.name} full rank? {C5.is_fullrank()}' )
    print( f'Is {C5.name} degenerate? {C5.is_degenerate}.\n' )

    # Nondegenerate conic with a, and foci.
    C6 = CConic( 2.0, name = 'C6', foci = ( CPoint( ( 0, 1 ) ), CPoint( ( 0, -1 ) ) ) )
    print( C6 )
    print( f'Rank of {C6.name}: {C6.rank}.' )
    print( f'Is {C6.name} full rank? {C6.is_fullrank()}' )
    print( f'Is {C6.name} degenerate? {C6.is_degenerate}.\n' )

    # Testing rank function.
    A = np.array( [ [ 0, 0, 0 ], [ 0, 0, 0 ], [ 0, 0, 0 ] ] )
    print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
    A = np.array( [ [ 1, 0, 0 ], [ 0, 0, 0 ], [ 0, 0, 0 ] ] )
    print(f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}')
    A = np.array( [ [ 1, 0, 0 ], [ 2, 0, 0 ], [ 0, 0, 0 ] ] )
    print(f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}')
    A = np.array( [ [ 1, 0, 0 ], [ 1, 0, 0 ], [ 1, 0, 0 ] ] )
    print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
    A = np.array( [ [ 1, 0, 0 ], [ 2, 0, 0 ], [ 3, 0, 0 ] ] )
    print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
    A = np.array( [ [ 0, 0, 1 ], [ 0, 0, 2 ], [ 0, 0, 3 ] ] )
    print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
    A = np.array( [ [ 1, 0, 0 ], [ 0, 2, 0 ], [ 0, 0, 3 ] ] )
    print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
    A = np.array( [ [ 0, 0, 1 ], [ 2, 0, 0 ], [ 3, 0, 0 ] ] )
    print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
    A = np.array( [ [ 1, 2, 0 ], [ 2, 4, 0 ], [ 3, 6, 0 ] ] )
    print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
    A = np.array( [ [ 1, 2, 0 ], [ 2, 4, 0 ], [ 0, 0, 5 ] ] )
    print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
    A = np.array( [ [ 1, 2, 0 ], [ 1, 3, 0 ], [ 0, 0, 5 ] ] )
    print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
    A = np.array( [ [ 0, 0, 1 ], [ 0, 0, 2 ], [ 4, 4, 0 ] ] )
    print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
    # A = np.array( [ [ 1, 2, 3 ], [ 4, 5, 6 ], [ 7, 8, 9 ] ] )
    # print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
    A = np.array( [ [ 40, -17, 166 ], [ -17, -20, -125 ], [ 166, -125, 580 ] ] )
    print( f'Rank of Matrix A: {rank( A )} --- Det of A: {LA.det( A )}' )
