# Convex Incremental Linear Programming solver
This is an implementation of a Convex Incremental Linear Programming solver for 2D and 3D problems, based on the theory presented in Chapter 4 of the book "Computational Geometry: Algorithms and Applications" (ISBN: 978-3-540-77974-2).

## How to use it?
To use the solver, you can clone the repository and use a recommended Python version of 3.10.10. It is recommended to use a virtual environment. After cloning, install the required dependencies by running the following command:

```
pip install -r requirement.txt
```
To start the command-line interface, run:

```
python runner.py -h
```
This will display the manual for the command-line interface. To test the performance of the program, you can run:

```
python runner.py test -t bounded -d 3
```
This will run a 3D program generator and solver and compare the results with Google's GLOP solver. The results will be returned in a CSV file, where the first column is n, the second column is the time used by the Convex solver, and the third column is the time used by GLOP solver.

## Limitations
Please note that there is currently an edge case and a similar class of problems that remain unsolvable by the three-dimensional solver. This is located in the "linear_program_data/gogogo" directory. However, I am actively investigating how we can solve this limitation.

If you encounter any issues or have any suggestions for improvement, please feel free to contact me.