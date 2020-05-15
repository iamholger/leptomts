# non-resonant leptogenesis with one decaying sterile neutrino using the density matrix equations. Equations from 1112.4528
import ulysses
import numpy as np
from odeintw import odeintw

from numba import jit
@jit
def fast_RHS(y0, d, w1, n1eq, epstt,epsmm,epsee,epstm,epste,epsme,c1t,c1m,c1e):

    N1      = y0[0]
    Ntt     = y0[1]
    Nmm     = y0[2]
    Nee     = y0[3]
    Nme     = y0[4]
    c1tc    = np.conjugate(c1t)
    c1mc    = np.conjugate(c1m)
    c1ec    = np.conjugate(c1e)


    #define the different RHSs for each equation
    rhs1 =      -d*(N1-n1eq)
    rhs2 = epstt*d*(N1-n1eq)-0.5*w1*(2*c1t*c1tc*Ntt               )
    rhs3 = epsmm*d*(N1-n1eq)-0.5*w1*(2*c1m*c1mc*Nmm + c1e*c1mc*Nme + np.conjugate(c1e*c1mc*Nme)                  )
    rhs4 = epsee*d*(N1-n1eq)-0.5*w1*(2*c1e*c1ec*Nee + c1e*c1mc*Nme + np.conjugate(c1e*c1mc*Nme)                  )
    rhs5 = epsme*d*(N1-n1eq)-0.5*w1*(  c1m*c1ec*Nee + c1e*c1ec*Nme + c1m*c1ec*Nmm  + c1m*c1mc*Nme)


    return [rhs1, rhs2, rhs3, rhs4, rhs5]

class EtaB_1BE2F(ulysses.ULSBase):
    """
    Density matrix equation (DME) with one decaying sterile. See arxiv:1112.4528.
    """

    def RHS(self, y0,z,epstt,epsmm,epsee,epstm,epste,epsme,c1t,c1m,c1e,k):

        if z != self._currz or z == self.zmin:
            self._d       = np.real(self.D1(k,z))
            self._w1      = np.real(self.W1(k,z))
            self._n1eq    = self.N1Eq(z)
            self._currz=z

        # thermal widths are set to zero such that we are in the "one-flavoured regime"
        return fast_RHS(y0,self._d, self._w1, self._n1eq,epstt,epsmm,epsee,epstm,epste,epsme,c1t,c1m,c1e)


    @property
    def EtaB(self):
        #Define fixed quantities for BEs
        epstt = np.real(self.epsilon1ab(2,2))
        epsmm = np.real(self.epsilon1ab(1,1))
        epsee = np.real(self.epsilon1ab(0,0))
        epstm =         self.epsilon1ab(2,1)
        epste =         self.epsilon1ab(2,0)
        epsme =         self.epsilon1ab(1,0)

        c1t   =                 self.c1a(2)
        c1m   =                 self.c1a(1)
        c1e   =                 self.c1a(0)

        k       = np.real(self.k1)
        y0      = np.array([0+0j,0+0j,0+0j,0+0j,0+0j], dtype=np.complex128)

        params  = np.array([epstt,epsmm,epsee,epstm,epste,epsme,c1t,c1m,c1e,k], dtype=np.complex128)

        ys, _      = odeintw(self.RHS, y0, self.zs, args = tuple(params), full_output=True)
        nb      = self.sphalfact*(ys[-1,1]+ys[-1,2]+ys[-1,3])

        self.ys  = np.real(ys[:, [1,2,3]])

        return np.real(nb)