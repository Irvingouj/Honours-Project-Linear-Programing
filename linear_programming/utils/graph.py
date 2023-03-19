from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
from linear_programming.classes.constraints import Constraints
from linear_programming.classes.vector import Vector
# plot the feasible region
def to_evaluate_string(constraints: Constraints):
    return f"({constraints.a}*x + {constraints.b}*y <= {constraints.c})"

def evaluate_y(constraints: Constraints, x: np.ndarray)->Tuple[np.ndarray, str]:
    constraints_str = str(constraints)
    return (constraints.c - constraints.a*x)/constraints.b,constraints_str

def show_feasible_region(constraints: List[Constraints],x_left=-100, x_right=100, y_bottom=-100, y_top=100):

    d = np.linspace(x_left,x_right,(x_right-x_left)*10)
    x,y = np.meshgrid(d,d)
    region = []
    for con in constraints:
        print(con)
        region.append(con.a*x + con.b*y <= con.c)
    graph = np.logical_and.reduce(region)
    plt.imshow( graph.astype(int) , 
                    extent=(x.min(),x.max(),y.min(),y.max()),origin="lower", cmap="Greys", alpha = 0.3);


    # plot the lines defining the constraints
    x = np.linspace(-100, 100, 2000)
    y_list = [evaluate_y(constraint, x) for constraint in constraints]

    for y, label in y_list:
        plt.plot(x, y, label=label)
    plt.xlim(x_left,x_right)
    plt.ylim(y_bottom,y_top)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')
    plt.show()
    
    
def show_vectors(vectors: List[Vector], names: List[str]):
    fig, ax = plt.subplots(figsize=(200,200))
    fig.set_size_inches(60, 40)
    for vector, label in zip(vectors, names):
        ax.quiver(0, 0, vector.get(0), vector.get(1), angles='xy', scale_units='xy', scale=1, label=label,color = np.random.rand(3,))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)

    # Adjust the figure and margins to prevent label overlap
    fig.set_size_inches(6, 4)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.6, top=0.9)
    

    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=5)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    plt.show()