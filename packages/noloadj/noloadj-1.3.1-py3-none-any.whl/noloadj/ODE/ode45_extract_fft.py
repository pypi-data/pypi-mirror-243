from noloadj.ODE.ode45_fft import odeint45_fft,odeint45_fft_etendu
from noloadj.ODE.ode_tools import *
from noloadj.ODE.ode45_extract import _odeint45_extract,odeint45_extract_etendu

def odeint45_extract_fft(f,x0,*P,M,T=0.,h0=1e-5,tol=1.48e-8):
    return _odeint45_extract_fft(f,h0,tol,M,x0,T,*P)


@partial(custom_jvp,nondiff_argnums=(0,1,2,3))
def _odeint45_extract_fft(f,h0,tol,M,x0,T,*P):

    freq_cstr=dict(zip(list(f.freq_constraints.keys()),
                                [0.] * len(f.freq_constraints)))

    tf,xf,yf,cstr,ifinal=_odeint45_extract(f,h0,tol,x0,T,*P)
    f.state=ifinal
    _,modX,phX,_,modY,phY=odeint45_fft(f,xf,np.linspace(tf,tf+T,M),*P,
                                    M=M,T=T,h0=h0)

    vect_freq=np.where(M//2==0,np.linspace(0.,(M/2-1)/T,M//2),
                          np.linspace(0.,(M-1)/(2*T),M//2))
    if hasattr(f,'freq_constraints'):
        for i in f.freq_constraints.keys():
            expression,_,name=f.freq_constraints[i]
            if name in f.xnames:
                ind = f.xnames.index(name)
                freq_cstr[i]=expression(modX[ind],phX[ind],vect_freq,1/T)
            else:
                ind=f.ynames.index(name)
                freq_cstr[i]=expression(modY[ind],phY[ind],vect_freq,1/T)

    return (tf,xf,yf,cstr,freq_cstr)


@_odeint45_extract_fft.defjvp
def _odeint45_fft_jvp(f,h0,tol,M, primals, tangents):
    x0,T, *P = primals
    dx0,dT, *dP = tangents
    nPdP = len(P)

    xf,yf,cstr,freq_cstr,tf,dtf,dxf,dyf,dcstr,dfreq_cstr=\
        odeint45_extract_fft_etendu(f,nPdP,h0,tol,M,x0,dx0,T,dT,
                                    *P,*dP)
    return (tf,xf,yf,cstr,freq_cstr),(dtf,dxf,dyf,dcstr,dfreq_cstr)


def odeint45_extract_fft_etendu(f,nPdP,h0,tol,M,x0,dx0,T,dT,*P_and_dP):

    freq_cstr=dict(zip(list(f.freq_constraints.keys()),
                       [0.]*len(f.freq_constraints)))
    dfreq_cstr=dict(zip(list(f.freq_constraints.keys()),
                             [0.]*len(f.freq_constraints)))

    xf,yf,cstr,ts,dts,dxf,dyf,dcstr,ifinal=odeint45_extract_etendu(f,
                            nPdP,h0,tol,x0,dx0,T,dT,*P_and_dP)
    f.state=ifinal
    _,_,modX,phX,dmodX,dphX,_,_,modY,phY,dmodY,dphY=odeint45_fft_etendu(f,
            nPdP,h0,tol,M,xf,dxf,np.linspace(ts,ts+T,M),T,*P_and_dP)

    vect_freq=np.where(M//2==0,np.linspace(0.,(M/2-1)/T,M//2),
                          np.linspace(0.,(M-1)/(2*T),M//2))
    if hasattr(f,'freq_constraints'):
        for i in f.freq_constraints.keys():
            _,der_expression,name=f.freq_constraints[i]
            if name in f.xnames:
                ind = f.xnames.index(name)
                freq_cstr[i],dfreq_cstr[i]=der_expression(modX[ind],
                phX[ind],dmodX[ind], dphX[ind],vect_freq,1//T)
            else:
                ind = f.ynames.index(name)
                freq_cstr[i],dfreq_cstr[i]=der_expression(modY[ind],
                phY[ind],dmodY[ind], dphY[ind],vect_freq,1//T)

    return xf,yf,cstr,freq_cstr,ts,dts,dxf,dyf,dcstr,dfreq_cstr


################################################################################

def Module_0Hz(name):
    def expression(module,phase,vect_freq,f):
        res=module[0]
        return res
    def der_expression(module,phase,dmodule,dphase,vect_freq,f):
        res=module[0]
        dres=dmodule[0]
        return res,dres
    return expression,der_expression,name

def Module_Fondamental(name):
    def expression(module,phase,vect_freq,f):
        indf=np.argmin(np.abs(vect_freq-f))
        res=module[indf]
        return res
    def der_expression(module,phase,dmodule,dphase,vect_freq,f):
        indf=np.argmin(np.abs(vect_freq-f))
        res=module[indf]
        dres=dmodule[indf]
        return res,dres
    return expression,der_expression,name

def Module_Harmoniques(name,number):
    def expression(module,phase,vect_freq,f):
        res=np.zeros(number)
        for j in range(len(res)):
            indf=np.argmin(np.abs(vect_freq-(j+2)*f))
            res=res.at[j].set(module[indf])
        return res
    def der_expression(module,phase,dmodule,dphase,vect_freq,f):
        res = np.zeros(number)
        dres=np.zeros(number)
        for j in range(len(res)):
            indf=np.argmin(np.abs(vect_freq-(j+2)*f))
            res=res.at[j].set(module[indf])
            dres=dres.at[j].set(dmodule[indf])
        return res,dres
    return expression,der_expression,name
