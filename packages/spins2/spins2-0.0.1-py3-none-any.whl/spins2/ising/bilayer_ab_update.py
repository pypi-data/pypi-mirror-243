import time
import numpy as np
from numba import njit, prange
from spins2 import functions

def iteration3(latt, X_s, Y_s, Jh, Jv, J0, J1, val, nequilibrium, nworks):
    Nw = np.zeros((nworks, 8))
    Ew = np.zeros(nworks)
    t0 = time.time()
    for i in range(nequilibrium):
        randvals = np.random.rand(2, 2, 2, Y_s, X_s)
        E0 = update3(latt, randvals, X_s, Y_s, Jh, Jv, J0, J1, val)
    for i in range(nworks):
        randvals = np.random.rand(2, 2, 2, Y_s, X_s)
        E0 = update3(latt, randvals, X_s, Y_s, Jh, Jv, J0, J1, val)
        Ew[i] = E0 / 2
        Nw[i] = functions.Average(latt[0,0,0]), functions.Average(latt[0,1,0]), functions.Average(latt[0,0,1]), functions.Average(latt[0,1,1]),\
                functions.Average(latt[1,0,0]), functions.Average(latt[1,1,0]), functions.Average(latt[1,0,1]), functions.Average(latt[1,1,1])
    t = time.time() - t0
    return t, Nw, Ew

@njit(cache=True, parallel=True)
def update3(latt, randvals, X_s, Y_s, Jh, Jv, J0, J1, val):
    nn_sum = 0
    for h in prange(2):
        for g in range(2):
            for f in range(2):
                for j in range(Y_s):
                    for i in range(X_s):
                        ipp = (i + 1) if (i + 1) < X_s else 0
                        inn = (i - 1) if (i - 1) > -1  else (X_s - 1)
                        jpp = (j + 1) if (j + 1) < Y_s else 0
                        jnn = (j - 1) if (j - 1) > -1  else (Y_s - 1)
                        ho = 1 - h
                        go = 1 - g
                        fo = 1 - f
                        hx0 = inn if g == 0 else ipp
                        if f == 0:
                            vy0 = jnn
                            vx0 = inn if g == 0 else i
                        else:
                            vy0 = jpp
                            vx0 = i   if g == 0 else ipp
                        if h == 0:
                            x_0 = inn if g == 0 else i
                            if f == 0:
                                gp = go
                                y_0 = j
                                y_1 = jnn
                                x_1 = inn if g == 0 else i
                                y_2 = j
                            else:
                                gp  = g
                                y_0 = jpp
                                y_1 = j
                                x_1 = i
                                y_2 = jpp
                        else:
                            x_0 = i   if g == 0 else ipp
                            if f == 0:
                                gp  = g
                                y_0 = jnn
                                y_1 = j
                                x_1 = i
                                y_2 = jnn
                            else:
                                gp = go
                                y_0 = j
                                y_1 = jpp
                                x_1 = i   if g == 0 else ipp
                                y_2 = j

                        energy  = ( -Jh * ( latt[h ,go,f ,j  ,i  ] + latt[h ,go,f ,j  ,hx0] ) -

                                     Jv * ( latt[h ,g ,fo,j  ,i  ] + latt[h ,g ,fo,vy0,i  ] +
                                            latt[h ,go,fo,j  ,vx0] + latt[h ,go,fo,vy0,vx0] ) -

                                     J0 * ( latt[ho,g ,f ,j  ,i  ] + latt[ho,go,f ,j  ,x_0] +
                                            latt[ho,gp,fo,y_0,i  ] ) -

                                     J1 * ( latt[ho,gp,fo,y_1,x_1] +
                                            latt[ho,go,fo,y_2,i  ] + latt[ho,go,fo,y_2,hx0] ) )
                        energy *= latt[h,g,f,j,i]

                        if val == 0:
                            if energy < 0:
                                pass
                            else:
                                latt[h,g,f,j,i] *= -1
                        else:
                            if energy < 0:
                                if randvals[h,g,f,j,i] < np.exp( 2.0 * val * energy ):
                                    latt[h,g,f,j,i] *= -1
                            else:
                                latt[h,g,f,j,i] *= -1

                        nn_sum += energy
    return nn_sum
