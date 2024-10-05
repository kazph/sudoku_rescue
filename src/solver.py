import utils
import re
from typing import Optional

# Constants
COLUMNS   = "123456789"
ROWS      = "ABCDEFGHI"
SQUARES   = utils.cross(ROWS, COLUMNS)
UNITLIST  = (
    [ utils.cross(ROWS, c) for c in COLUMNS ] +
    [ utils.cross(r, COLUMNS) for r in ROWS  ] +
    [ utils.cross(rs, cs) for rs in ["ABC", "DEF", "GHI"] for cs in ["123", "456", "789"]]
)
UNITS     = dict((s, [u for u in UNITLIST if s in u]) for s in SQUARES)
PEERS     = dict((s, set(sum(UNITS[s], [])) - set([s])) for s in SQUARES)

# Types
Digit    = str
DigitSet = str
Square   = str
Grid     = dict[Square, DigitSet]
Picture  = str

def is_solution(solution: Grid, puzzle: Grid) -> bool:
    """To check wheater the given solution is valid"""
    return (solution is not None and
            all(solution[s] in puzzle[s] for s in SQUARES) and
            all({solution[s] for s in unit} == set(COLUMNS) for unit in UNITLIST))

def parse(picture) -> Grid:
    """Parse picture to grid"""
    vals = re.findall(r"[.1-9]|[{][1-9]+[}]", picture)
    assert len(vals) == 81
    return {s: COLUMNS if v == '.' else re.sub(r"[{}]", '', v) 
            for s, v in zip(SQUARES, vals)}

def picture(grid) -> Picture:
    """Convert a Grid to a Picture string, one line at a time."""
    if grid is None: 
        return "None"
    def val(d: DigitSet) -> str: return '.' if d == COLUMNS else d if len(d) == 1 else '{' + d + '}'
    maxwidth = max(len(val(grid[s])) for s in grid)
    dash1 = '-' * (maxwidth * 3 + 2)
    dash3 = '\n' + '+'.join(3 * [dash1])
    def cell(r, c): return val(grid[r + c]).center(maxwidth) + ('|'  if c in '36' else ' ')
    def line(r): return ''.join(cell(r, c) for c in COLUMNS)    + (dash3 if r in 'CF' else '')
    return '\n'.join(map(line, ROWS))


## -- SOLVERS -- ##

# (1) If a square has only one possible digit, then eliminate that digit as a possibility for each of the square's peers.
# (2) If a unit has only one possible squares that can hold that digit, then fill the square with that digit


def constrain(grid) -> Grid:
    "Propagate constraints on a copy of grid to yield a new constrained Grid."
    result: Grid = {s: COLUMNS for s in SQUARES}
    for s in grid:
        if len(grid[s]) == 1:
            fill(result, s,  grid[s])
    return result

def fill(grid: Grid, s: Square, d: Digit) -> Optional[Grid]:
    """Eliminate all the digits except d from grid[s]."""
    if grid[s] == d or all(eliminate(grid, s, d2) for d2 in grid[s] if d2 != d):
        return grid
    else:
        return None

def eliminate(grid: Grid, s: Square, d: Digit) -> Optional[Grid]:
    """Eliminate d from grid[s]; implement the two constraint propagation strategies."""
    if d not in grid[s]:
        return grid        ## Already eliminated
    grid[s] = grid[s].replace(d, '')
    if not grid[s]:
        return None        ## None: no legal digit left
    elif len(grid[s]) == 1:
        # 1. If a square has only one possible digit, then eliminate that digit as a possibility for each of the square's peers.
        d2 = grid[s]
        if not all(eliminate(grid, s2, d2) for s2 in PEERS[s]):
            return None    ## None: can't eliminate d2 from some square
    for u in UNITS[s]:
        dplaces = [s for s in u if d in grid[s]]
        # 2. If a unit has only one possible square that can hold a digit, then fill the square with the digit.
        if not dplaces or (len(dplaces) == 1 and not fill(grid, dplaces[0], d)):
            return None    ## None: no place in u for d
    return grid