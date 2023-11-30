import argparse, os, numba, platform
import numpy as np
from spins2 import __version__

def main():
    parser = argparse.ArgumentParser(description='spins2: A Monte Carlo Simulation Code for the Phase Transition in 2D/3D Materials',
                                     epilog='''
configurations:       init:                             parameters:         model:
bilayer-ab            fm, afm1, afm2, afm3, afm4        Jh, Jv, J0, J1      ising, single, mae

default values:
x, y, z = 64, 64, 64
iterations for equilibrium, works = 64, 64
exchange coupling (meV) = 1.0
single-ion anisotropy (meV) = 0.1
temperatures = 0 15 5 16 60

Example:
spin -n 4 -x 100 -y 100 -e 200 -w 1000 -n 2 -t 35 -r
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version", action="version", version="spins2 "+__version__+" from "+os.path.dirname(__file__)+' (python'+platform.python_version()+')')
    parser.add_argument('-n', "--np",           type=int,   default=4 )
    parser.add_argument('-x', "--length",       type=int,   default=64)
    parser.add_argument('-y', "--width",        type=int,   default=64)
    parser.add_argument('-z', "--height",       type=int,   default=64)
    parser.add_argument('-e', "--equilibrium",  type=int,   default=64)
    parser.add_argument('-w', "--works",        type=int,   default=64)
    parser.add_argument('-a', "--single",       type=float, default=[0.1], nargs='+')
    parser.add_argument('-p', "--parameters",   type=float, default=[1.0], nargs='+')
    parser.add_argument('-j', "--parametersX",  type=float, default=[], nargs='+')
    parser.add_argument('-k', "--parametersY",  type=float, default=[], nargs='+')
    parser.add_argument('-t', "--temperatures", type=float, default=[0, 15, 5, 16, 60], nargs='+')
    parser.add_argument('-l', "--label",        type=str,   default='', help='label of the figures')
    parser.add_argument('-r', "--export", action='store_true', help="plot figures after iterations")
    parser.add_argument('-o', "--plot",   type=str, help="plot figures from .log file")
    parser.add_argument('-f', "--format", default="png",        type=str.lower, choices=['png', 'pdf', 'svg', 'jpg', 'tif'])
    parser.add_argument('-m', "--model",  default="ising",      type=str.lower, choices=['ising', 'single', 'mae'])
    parser.add_argument('-i', "--init",   default="fm",         type=str.lower, choices=['fm', 'afm1', 'afm2','afm3', 'afm4', 'afm5', 'random'])
    parser.add_argument('-c', "--config", default="bilayer-ab", type=str.lower, choices=['bilayer-ab'])
    args = parser.parse_args()

    NP = args.np
    numba.set_num_threads(NP)

    X = check(args.length)
    Y = check(args.width)
    Z = check(args.height)
    config = args.config
    init = args.init

    arrays_temperatures = temperatures(args.temperatures)

    nequilibrium = args.equilibrium
    nworks = args.works
    J = args.parameters
    A = args.single
    JX = args.parametersX
    JY = args.parametersY
    format = args.format
    legend = args.label

    if args.plot and os.path.exists(args.plot):
        from spins2 import plots
        plots.main(args.plot, format, legend)
    else:
        if args.model == "ising":
            if config == "bilayer-ab":
                file = '{}_{}_{}.log'.format(config, X, Y)
                from spins2.ising import bilayer_ab
                bilayer_ab.run(file, init, X, Y, J, arrays_temperatures, nequilibrium, nworks)
            else:
                print("Inconsistent parameters...")
        elif args.model == "single":
            if config == "bilayer-ab":
                file = '{}_single_{}_{}.log'.format(config, X, Y)
                from spins2.single import bilayer_ab
                bilayer_ab.run(file, init, X, Y, J, A, arrays_temperatures, nequilibrium, nworks)
            else:
                print("Inconsistent parameters...")
        elif args.model == "mae":
            if config == "bilayer-ab":
                file = '{}_mae_{}_{}.log'.format(config, X, Y)
                from spins2.mae import bilayer_ab
                bilayer_ab.run(file, init, X, Y, J, JX, JY, A, arrays_temperatures, nequilibrium, nworks)
            else:
                print("Inconsistent parameters...")
        else:
            print("Inconsistent parameters...")

        if args.export and os.path.exists(file):
            from spins2 import plots
            plots.main(file, format, legend)

def check(num):
    if num < 10:
        num = 10
    if num % 2 != 0:
        num += 1
    if num % 4 != 0:
        num += 2
    return num

def temperatures(arr_temperatures):
    i = len(arr_temperatures)
    if i == 1:
        return np.arange(arr_temperatures[0]+1)
    elif i == 2:
        return np.arange(arr_temperatures[0], arr_temperatures[1]+1)
    else:
        k = i // 3
        l = i % 3
        j = 0
        while j < k:
            if j == 0:
                arrays_temperatures = np.arange(arr_temperatures[0], arr_temperatures[1], arr_temperatures[2])
            else:
                arrays_temperatures=np.concatenate((arrays_temperatures,
                    np.arange(arr_temperatures[j * 3], arr_temperatures[j * 3 + 1], arr_temperatures[j * 3 + 2])))
            if arrays_temperatures[-1] != arr_temperatures[j * 3 + 1]:
                arrays_temperatures = np.append(arrays_temperatures, arr_temperatures[j * 3 + 1])
            j += 1
        if l == 2:
            arrays_temperatures=np.concatenate((arrays_temperatures,
                np.arange(arr_temperatures[j * 3], arr_temperatures[j * 3 + 1]+1)))
        return arrays_temperatures
