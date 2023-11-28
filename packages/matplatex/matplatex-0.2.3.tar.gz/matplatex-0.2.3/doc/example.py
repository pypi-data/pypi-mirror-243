import matplatex

import matplotlib.pyplot as plt
import numpy as np

def main():
    x = np.linspace(0, 4*np.pi, 300)
    y = 0.1*x*np.sin(x)
    fig, ax = plt.subplots()
    ax.plot(x, y, label="increasing sine wave")
    ax.set_title("title")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc='upper left')
    ax.annotate('$\mathcal{O}$', (0,0), xycoords='figure fraction')
    ax.annotate('$\mathcal{C}$', (0.5,0.5), xycoords='figure fraction')
    ax.annotate('$\mathcal{I}$', (1,1), xycoords='figure fraction')

    matplatex.save(fig, "./example")
    plt.savefig("example_expected.pdf", format='pdf')
#    plt.show()

if __name__ == '__main__':
    main()
