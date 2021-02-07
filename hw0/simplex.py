"""A simplex implementation for Advanced Algorithms '21

author: awenstrup
"""

ex_c = [3, 2, 0, 0]
ex_A = [[1,  2,  1,  0],
     [1, -1,  0,  1]]
ex_b = [4, 1]

hw_c = [8, -6, 4, 0, 0, 0]
hw_A = [
    [1, 1, 1, 1, 0, 0],
    [5, 3, 0, 0, 1, 0],
    [0, 9, 2, 0, 0, 1]
]
hw_b = [12, 20, 15]
MAX_IMPROVES = 5

def simplex(c, A, b):
    """The main simplex algorithm. Takes a system
    defined with c, A, and b.

    :param list c: The coefficients of x in the value we are maximizing for
    :param list A: The coefficients of x in each constraint equation
    :param list b: The values on the other side of each inequality

    :rtype: float
    :returns: The optimized value of the objective function
    """
    tableau = initial_tableau(c, A, b)
    count = 0
    print(tableau)
    while can_improve(tableau) and count < MAX_IMPROVES:
        print("Improving...")
        r, c = find_pivot(tableau)
        print(f"Pivoting on ({r}, {c})")
        pivot(r, c, tableau)
        count += 1
        print(tableau)

    return -(tableau[-1][-1])

def initial_tableau(c, A, b) -> list:
    """Get the initial tableau. In this case, get the
    trivial initial tableau

    :param list c: The coefficients of x in the value we are maximizing for
    :param list A: The coefficients of x in each constraint equation
    :param list b: The values on the other side of each inequality

    :rtype: list
    :returns: The 2D list representing the tableau
    """
    out = []
    for x, y in zip(A, b):
        out.append(x[:] + [y])
    out.append(c)
    out[-1].append(0)
    return out

def can_improve(tab) -> bool:
    """Check if the tableau is optimized. It is optimized
    if every value in the bottom row is <= 0.

    :param list tab: The current tableau

    :rtype: bool
    :returns: Whether the tableau can improve. It can improve
    if it is not optimized yet.
    """
    for x in tab[-1]:
        if x > 0: return True

    return False

def find_pivot(tab) -> tuple:
    """Find an index to pivot about

    :param list tab: The current tableau

    :rtype: tuple
    :returns: The index (row, column) to pivot about
    """
    # Find the smallest positive coefficient of the bottom row 
    # (the variable we are going to swap in)
    column_min = None
    column_min_index = None
    for i in range(len(tab[-1])):
        if tab[-1][i] > 0:
            # No min found yet
            if column_min == None:
                column_min = tab[-1][i]
                column_min_index = i
            # Current value is smaller than current min
            if tab[-1][i] < column_min:
                column_min = tab[-1][i]
                column_min_index = i

    # Find the smallest quotient (which variable to swap out)
    quotients = [(i, tab[i][-1] / tab[i][column_min_index]) for i in range(len(tab) - 1) if tab[i][column_min_index] > 0]
    row_min_index = min(quotients, key=lambda x: x[1])[0]

    # Return the index
    return row_min_index, column_min_index

def pivot(r, c, tab):
    """Given a tableau and a pivot point, perform a pivot. 
    Alters the tableau in place, and returns it.

    :param int c: The column of the pivot point
    :param int r: The row of the pivot point
    :param list tab: The current tableau

    :rtype: list
    :returns: The new, altered tableau
    """
    # Divide the row of the pivot point by the pivot value
    pivot_val = tab[r][c]
    for i in range(len(tab[0])):
        tab[r][i] /= pivot_val

    for i in range(len(tab)):
        if i != r:
            mults = []
            for j in range(len(tab[0])):
                mults.append(tab[i][c] * tab[r][j])
            
            # print(f"Mults: {mults}")

            for j in range(len(tab[0])):
                tab[i][j] -= mults[j]

print(simplex(hw_c, hw_A, hw_b))