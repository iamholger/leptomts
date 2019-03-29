import leptocalc
import numpy as np
from odeintw import odeintw

# from numba import jit
# @jit
def fast_RHS(y0,eps1tt,eps1mm,eps1ee,eps1tm,eps1te,eps1me,eps2tt,eps2mm,eps2ee,eps2tm,eps2te,eps2me,eps3tt,eps3mm,eps3ee,eps3tm,eps3te,eps3me, C, W, d1,d2,d3,w1,w2,w3,n1eq,n2eq,n3eq):
    N1, N2, N3, Ntt, Nmm, Nee, Ntm, Nte, Nme, Ntr = y0

    c1t,c1m,c1e,c2t,c2m,c2e,c3t,c3m,c3e = C
    widtht,widthm = W
    c1tc    = np.conjugate(c1t)
    c1mc    = np.conjugate(c1m)
    c1ec    = np.conjugate(c1e)

    c2tc    = np.conjugate(c2t)
    c2mc    = np.conjugate(c2m)
    c2ec    = np.conjugate(c2e)

    c3tc    = np.conjugate(c3t)
    c3mc    = np.conjugate(c3m)
    c3ec    = np.conjugate(c3e)

    #define the different RHSs for each equation
    rhs1    =      - d1 * (N1-n1eq)

    rhs2    =      - d2 * (N2-n2eq)

    rhs3    =      - d3 * (N3-n3eq)

    rhs4    = (eps1tt * d1 * (N1-n1eq) + eps2tt * d2 * (N2-n2eq) + eps3tt * d3 * (N3-n3eq)
      - 0.5 * w1 * (2 * c1t * c1tc * Ntt + c1m * c1tc * Ntm + c1e * c1tc * Nte + np.conjugate(c1m * c1tc * Ntm + c1e * c1tc * Nte))
      - 0.5 * w2 * (2 * c2t * c2tc * Ntt + c2m * c2tc * Ntm + c2e * c2tc * Nte + np.conjugate(c2m * c2tc * Ntm + c2e * c2tc * Nte))
      - 0.5 * w3 * (2 * c3t * c3tc * Ntt + c3m * c3tc * Ntm + c3e * c3tc * Nte + np.conjugate(c3m * c3tc * Ntm + c3e * c3tc * Nte))
              - 2 * widtht * Ntt + 4 * widtht * Ntr)

    rhs5    = (eps1mm * d1 * (N1-n1eq) + eps2mm * d2 * (N2-n2eq) + eps3mm * d3 * (N3-n3eq)
      - 0.5 * w1 * (2 * c1m * c1mc * Nmm + c1m * c1tc * Ntm + c1e * c1mc * Nme + np.conjugate(c1m * c1tc * Ntm + c1e * c1mc * Nme))
      - 0.5 * w2 * (2 * c2m * c2mc * Nmm + c2m * c2tc * Ntm + c2e * c2mc * Nme + np.conjugate(c2m * c2tc * Ntm + c2e * c2mc * Nme))
      - 0.5 * w3 * (2 * c3m * c3mc * Nmm + c3m * c3tc * Ntm + c3e * c3mc * Nme + np.conjugate(c3m * c3tc * Ntm + c3e * c3mc * Nme)))

    rhs6    = (eps1ee * d1 * (N1-n1eq) + eps2ee * d2 * (N2-n2eq) + eps3ee * d3 * (N3-n3eq)
      - 0.5 * w1 * (2 * c1e * c1ec * Nee + c1e * c1mc * Nme + c1e * c1tc * Nte + np.conjugate(c1e * c1mc * Nme + c1e * c1tc * Nte))
      - 0.5 * w2 * (2 * c2e * c2ec * Nee + c2e * c2mc * Nme + c2e * c2tc * Nte + np.conjugate(c2e * c2mc * Nme + c2e * c2tc * Nte))
      - 0.5 * w3 * (2 * c3e * c3ec * Nee + c3e * c3mc * Nme + c3e * c3tc * Nte + np.conjugate(c3e * c3mc * Nme + c3e * c3tc * Nte)))

    rhs7    = (eps1tm * d1 * (N1-n1eq) + eps2tm * d2 * (N2-n2eq) + eps3tm * d3 * (N3-n3eq)
      - 0.5 * ((w1 * c1t * c1mc + w2 * c2t * c2mc + w3 * c3t * c3mc) * Nmm
      +        (w1 * c1e * c1mc + w2 * c2e * c2mc + w3 * c3e * c3mc) * Nte
      +        (w1 * c1m * c1mc + w2 * c2m * c2mc + w3 * c3m * c3mc) * Ntm
      +        (w1 * c1mc * c1t + w2 * c2mc * c2t + w3 * c3mc * c3t) * Ntt
      +        (w1 * c1t * c1tc + w2 * c2t * c2tc + w3 * c3t * c3tc + 2 * widtht + 2 * widthm) * Ntm
      +        (w1 * c1t * c1ec + w2 * c2t * c2ec + w3 * c3t * c3ec) * np.conjugate(Nme)))

    rhs8    = (eps1te * d1 * (N1-n1eq) + eps2te * d2 * (N2-n2eq) + eps3te * d3 * (N3-n3eq)
      - 0.5 * ((w1 * c1t * c1ec + w2 * c2t * c2ec + w3 * c3t * c3ec) * Nee
      +        (w1 * c1e * c1ec + w2 * c2e * c2ec + w3 * c3e * c3ec) * Nte
      +        (w1 * c1m * c1ec + w2 * c2m * c2ec + w3 * c3m * c3ec) * Ntm
      +        (w1 * c1t * c1ec + w2 * c2t * c2ec + w3 * c3t * c3ec) * Ntt
      +        (w1 * c1t * c1mc + w2 * c2t * c2mc + w3 * c3t * c3mc) * Nme
      +        (w1 * c1t * c1tc + w2 * c2t * c2tc + w3 * c3t * c3tc + 2 * widtht) * Nte))

    rhs9    = (eps1me * d1 * (N1-n1eq) + eps2me * d2 * (N2-n2eq) + eps3me * d3 * (N3-n3eq)
      - 0.5 * ((w1 * c1m * c1ec + w2 * c2m * c2ec + w3 * c3m * c3ec) * Nee
      +        (w1 * c1e * c1ec + w2 * c2e * c2ec + w3 * c3e * c3ec + 2 * widthm) * Nme
      +        (w1 * c1m * c1ec + w2 * c2m * c2ec + w3 * c3m * c3ec) * Nmm
      +        (w1 * c1t * c1ec + w2 * c2t * c2ec + w3 * c3t * c3ec) * np.conjugate(Ntm)
      +        (w1 * c1m * c1mc + w2 * c2m * c2mc + w3 * c3m * c3mc) * Nme
      +        (w1 * c1m * c1tc + w2 * c2m * c2tc + w3 * c3m * c3tc) * Nte))

    rhs10   = 2 * widtht * (Ntt - 2 * Ntr)

    RHStemp = [rhs1, rhs2, rhs3, rhs4, rhs5, rhs6, rhs7, rhs8, rhs9, rhs10]
    return RHStemp

class EtaB_3DS_Scattering_OOEtauR(leptocalc.LeptoCalc):
    def RHS(self, y0, zzz, ETA, C, K, W):
        N1, N2, N3, Ntt, Nmm, Nee, Ntm, Nte, Nme, Ntr = y0
        (eps1tt,eps1mm,eps1ee,eps1tm,eps1te,eps1me,eps2tt,eps2mm,eps2ee,eps2tm,eps2te,eps2me,eps3tt,eps3mm,eps3ee,eps3tm,eps3te,eps3me) = ETA
        k1term,k2term,k3term = K
        d1      = np.real(self.DS(k1term, zzz))
        w1      = self.j(zzz)*np.real(self.W1(k1term, zzz))
        d2      = np.real(self.D2(k2term, zzz))
        w2      = np.real(self.W2(k2term, zzz))
        d3      = np.real(self.D3(k3term, zzz))
        w3      = np.real(self.W3(k3term, zzz))
        n1eq    = self.N1Eq(zzz)
        n2eq    = self.N2Eq(zzz)
        n3eq    = self.N3Eq(zzz)

        return fast_RHS(y0,eps1tt,eps1mm,eps1ee,eps1tm,eps1te,eps1me,eps2tt,eps2mm,eps2ee,eps2tm,eps2te,eps2me,eps3tt,eps3mm,eps3ee,eps3tm,eps3te,eps3me, C, W, d1,d2,d3,w1,w2,w3,n1eq,n2eq,n3eq)

    @property
    def EtaB(self):

        #Define fixed quantities for BEs
        _ETA = [
            np.real(self.epsilon1ab(2,2)),
            np.real(self.epsilon1ab(1,1)),
            np.real(self.epsilon1ab(0,0)),
                    self.epsilon1ab(2,1) ,
                    self.epsilon1ab(2,0) ,
                    self.epsilon1ab(1,0) ,
            np.real(self.epsilon2ab(2,2)),
            np.real(self.epsilon2ab(1,1)),
            np.real(self.epsilon2ab(0,0)),
                    self.epsilon2ab(2,1) ,
                    self.epsilon2ab(2,0) ,
                    self.epsilon2ab(1,0) ,
            np.real(self.epsilon3ab(2,2)),
            np.real(self.epsilon3ab(1,1)),
            np.real(self.epsilon3ab(0,0)),
                    self.epsilon3ab(2,1) ,
                    self.epsilon3ab(2,0) ,
                    self.epsilon3ab(1,0)]

        _C =   [self.c1a(2), self.c1a(1), self.c1a(0),
                self.c2a(2), self.c2a(1), self.c2a(0),
                self.c3a(2), self.c3a(1), self.c3a(0)]

        _K      = [np.real(self.k1), np.real(self.k2), np.real(self.k3)]
        _W      = [ 485e-10*self.MP/self.M1, 1.7e-10*self.MP/self.M1]

        y0      = np.array([0+0j,0+0j,0+0j,0+0j,0+0j,0+0j,0+0j,0+0j,0+0j,0+0j], dtype=np.complex128)

        zcrit   = 1e100
        ys, _   = odeintw(self.RHS, y0, self.xs, args = tuple([_ETA, _C , _K, _W]), full_output=1)
        nb      = np.real(self.sphalfact*(ys[-1,3]+ys[-1,4]+ys[-1,5]))

        return np.real(nb)

if __name__ == "__main__":
    pars = {
            'delta'  :270,
            'a'      :0,
            'b'      :0,
            'theta23':48.7,
            'theta12':33.63,
            'theta13': 8.52,
            'x1'    :45,
            'y1'    :45,
            'x2'    :45,
            'y2'    :45,
            'x3'    :45,
            'y3'    :45,
            'ordering':0,
            'm1'     :-0.60206,
            'M1'     :8,
            'M2'     :9,
            'M3'     :11
            }
    ETA = EtaB_3DS_Scattering_OOEtauR()
    # for _ in range(100):
        # ETA(pars)

    print(ETA(pars))

    import leptomts
    L=leptomts.LeptoCalc(nds=4)
    L.setParams(pars)
    print("Previous code gives etab = ",np.real(L.EtaB))