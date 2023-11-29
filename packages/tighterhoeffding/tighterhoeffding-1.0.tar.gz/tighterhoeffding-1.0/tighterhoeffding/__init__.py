import numpy as np
import scipy as sp
import scipy.optimize

VERSION=1.0

def _check_arguments(s,a,mu=None,alpha=None):
    A=np.sum(a)
    assert (a>=0).all()
    assert 0 <= s <=A
    if mu is not None:
        assert 0 < mu < A
    if alpha is not None:
        assert 0 < alpha < 1

r'''

      _               _                            _ _
  ___| | __ _ ___ ___(_) ___   _ __ ___  ___ _   _| | |_ ___
 / __| |/ _` / __/ __| |/ __| | '__/ _ \/ __| | | | | __/ __|
| (__| | (_| \__ \__ \ | (__  | | |  __/\__ \ |_| | | |_\__ \
 \___|_|\__,_|___/___/_|\___| |_|  \___||___/\__,_|_|\__|___/

'''

def _hoeffding_thm1(s,n,mu):
    '''
    Let

        S = sum_i^n X_i
        X_i in [0,1]
        sum E[X_i] = mu

    Returns upper bound on log P(S>=s).
    '''

    if s<=mu:
        return 0.0
    elif s>n:
        return -np.inf

    hoeffding_mu = mu/n
    hoeffding_t = s/n - mu/n

    assert hoeffding_t>=0
    assert s<=n
    assert mu>=0
    assert mu<=n

    T1 = (hoeffding_mu/(hoeffding_mu+hoeffding_t))**(hoeffding_mu+hoeffding_t)

    if 1-hoeffding_mu-hoeffding_t!=0:
        T2 = ((1-hoeffding_mu)/(1-hoeffding_mu-hoeffding_t))**(1-hoeffding_mu-hoeffding_t)
    else:
        T2 = 1.0

    return n*np.log(T1*T2)

def hoeffding_thm1(s,n,mu,a=1):
    '''
    Let

        S = sum_i^n X_i
        X_i in [0,a]
        sum E[X_i] = mu

    Returns upper bound on log P(S>=s)
    '''

    '''
        P(S > s) = P(sum_i X_i > s)  subject to sum E[X_i] = mu
                 = P(sum_i X_i/a > s/a) subject to sum E[X_i/a] = mu/a
    '''

    a=float(a)

    if a<0:
        raise ValueError("a should be positive")

    return _hoeffding_thm1(s/a,n,mu/a)


def hoeffding_thm2(s,mu,a):
    '''
    Let

        S = sum_i^n X_i
        X_i in [0,a_i]
        sum E[X_i] = mu

    Returns upper bound on log P(S>=s)
    '''

    _check_arguments(s,a,mu=mu)

    hoeffding_t = s - mu

    if s<=mu:
        return 0.0
    else:
        hoeffding_t = s-mu
        return -2*hoeffding_t*hoeffding_t / np.sum(a**2)



r'''
 _   _       _     _          _                            __  __
| |_(_) __ _| |__ | |_    ___| |__   ___ _ __ _ __   ___  / _|/ _|
| __| |/ _` | '_ \| __|  / __| '_ \ / _ \ '__| '_ \ / _ \| |_| |_
| |_| | (_| | | | | |_  | (__| | | |  __/ |  | | | | (_) |  _|  _|
 \__|_|\__, |_| |_|\__|  \___|_| |_|\___|_|  |_| |_|\___/|_| |_|
       |___/
'''

def uniqify(a):
    a=a[a!=0]
    return np.unique(a,return_counts=True)

def _lamstar(mu,asrt,w,t):
    b=(np.exp(asrt*t) -1) / asrt

    def meandiff(lam):
        return np.sum(_taustar(asrt,b,lam)*w) - mu

    LB=np.min((np.exp(asrt*t)-1)/(np.exp(asrt*t)-1+asrt))
    UB=np.max(b)

    return sp.optimize.bisect(meandiff,LB,UB)

def _taustar(asrt,b,lam):
    tau = (b - lam)/(b*lam)
    tau = np.clip(tau,0,asrt)
    return tau

def _g_weighted(s,mu,asrt,w,t,lam):
    assert t>=0 and lam>=0

    if t==0:
        return lam*mu - s*t
    if lam==0:
        return (np.sum(asrt*w)-s)*t

    b=(np.exp(asrt*t) -1) / asrt
    tau = (b - lam)/(b*lam)
    tau = np.clip(tau,0,asrt)

    rez=np.sum(np.log(1+b*tau)*w) + lam*(mu - np.sum(tau*w)) - s*t

    return rez

def sharp_chernoff(s,mu,a):
    '''
    Let

        S = sum_i^n X_i
        X_i in [0,a_i]
        sum E[X_i] = mu

    Returns upper bound on log P(S>=s)
    '''
    _check_arguments(s,a,mu=mu)
    asrt,w=uniqify(a)

     # keep a in check to maintain numerical stability
    mx=asrt.max()
    s=s/mx
    mu=mu/mx
    asrt=asrt/mx

    return _sharp_chernoff_weighted(s,mu,asrt,w).fun

def _sharp_chernoff_weighted(s,mu,asrt,w):
    # find reasonable initialization
    t_init=.5
    lam_init=_lamstar(mu,asrt,w,t_init)

    rez=sp.optimize.minimize(
        lambda tlam: _g_weighted(s,mu,asrt,w,tlam[0],tlam[1]),
        (t_init,lam_init),
        bounds=[(0,np.inf),(0,np.inf)],
        method='nelder-mead'
    )
    if not rez.success:
        raise Exception("Minimization failed!")

    return rez
