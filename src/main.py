import solver

def main():
    # Parsing arguments and all of that
    
    test = "53..7.... 6..195... .98....6. 8...6...3 4..8.3..1 7...2...6 .6....28. ...419..5 ....8..79"
    nyteasy = "...932186 2...683.. 68...7..9 ...65...1 .751..4.. 4.1..392. .48.7..1. .3....84. 1278.6..."
    nytmedium = "61...8... 4..3.21.9 ......2.. ...4...27 ..9...... 3..5.9..1 8.7.36... .6....... ...7...6."
    nythard = "...2...1. ...9..4.2 .9...7... .43..65.. 5...9...6 8..7..... 1.5...3.. .....1.9. .2.3...8."

    grid = solver.parse(nyteasy)
        
    print(solver.picture(grid))
    print()
    print(solver.picture(solver.constrain(grid)))
    
if __name__ == "__main__":
    main()