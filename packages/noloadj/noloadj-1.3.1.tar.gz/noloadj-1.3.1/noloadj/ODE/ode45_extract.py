import jax.numpy as np
from jax.lax import *
from jax import custom_jvp,jvp
from functools import partial
from noloadj.ODE.ode45 import next_der_step_simulation,next_step_simulation,\
    compute_new_point,interpolation

def odeint45_extract(f,x0,*P,T=0.,h0=1e-5,tol=1.48e-8):
    return _odeint45_extract(f,h0,tol,x0,T,*P)


@partial(custom_jvp,nondiff_argnums=(0,1,2))
def _odeint45_extract(f,h0,tol,x0,T,*P):
    type,cond_stop=f.stop

    def cond_fn(state):
        x_prev2,x_prev,t_prev,_,h_prev,cstr,_,_=state
        if type=='threshold':
            val,seuil=cond_stop(x_prev,f.xnames)
            valp,_=cond_stop(x_prev2,f.xnames)
            return (h_prev>0) & (np.sign(val-seuil)==np.sign(valp-seuil))
        else:
            return (h_prev > 0) & cond_stop(t_prev,t_prev+h_prev,cstr)


    def body_fn(state):
        _,x_prev,t_prev,y_prev,h_prev,cstr,i_prev,c_prev=state

        x_now,t_now,y_now,h_now,i_now,c_now=next_step_simulation(x_prev,t_prev,
                                    y_prev,i_prev,c_prev,h_prev,f,tol,T,*P)

        if type=='threshold':
            output,seuil=cond_stop(x_now,f.xnames)
            outputprev,_=cond_stop(x_prev,f.xnames)
            condition=np.sign(output-seuil)!=np.sign(outputprev-seuil)
            x_now,h_prev,t_now,y_now=cond(condition,lambda state:
                compute_new_point(x_now,x_prev,t_prev,t_now,y_prev,y_now,
                output-seuil,outputprev-seuil),lambda state:state,(x_now,h_prev,
                                                                   t_now,y_now))
            x_now,t_now,y_now,h_now,i_now,c_now=cond(condition,lambda state:
                next_step_simulation(x_prev,t_prev,y_prev,i_prev,c_prev,h_prev,
                f,tol,T,*P),lambda state:state,(x_now,t_now,y_now,h_now,i_now,
                                                c_now))

        elif isinstance(type,float):
            x_now,y_now=cond(t_now>type,lambda state:interpolation(x_prev,y_prev,
                t_prev,x_now,y_now,t_now,type),lambda state:state,(x_now,y_now))
            t_now=np.where(t_now>type,type,t_now)
            h_prev=np.where(t_now>type,type-t_prev,h_prev)

        if hasattr(f,'constraints'):
            for i in f.constraints.keys():
                if isinstance(f.constraints[i][1],tuple):
                    test_exp,(_,expression,_,_,_,_,name)=f.constraints[i]
                else:
                    (_,expression,_,_,_,_,name)=f.constraints[i]
                    test_exp = lambda t: True
                if name in f.xnames:
                    ind=f.xnames.index(name)
                    cstr[i]=np.where(test_exp(t_now),expression(t_prev,
                        x_prev[ind],t_now,x_now[ind],cstr[i],h_prev,T),cstr[i])
                else:
                    ind=f.ynames.index(name)
                    cstr[i]=np.where(test_exp(t_now),expression(t_prev,
                        y_prev[ind],t_now,y_now[ind],cstr[i],h_prev,T),cstr[i])

        return x_prev,x_now,t_now,y_now,h_now,cstr,i_now,c_now

    cstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))# INITIALISATION
    if hasattr(f,'state'):
        i0=f.state
    else:
        i0=0
    if hasattr(f,'commande'):
        _,c0=f.commande(0.,T)
    else:
        c0=0
    tempP=None
    if hasattr(f,'initialize'):
        tempP=P
        P=f.initialize(*P)
    y0=f.output(x0,0.,*P)
    if hasattr(f,'initialize'):
        P=tempP
    if hasattr(f,'constraints'):
        for i in f.constraints.keys():
            if isinstance(f.constraints[i][1],tuple):
                test_exp,(init,_,_,_,_,_,name)=f.constraints[i]
            else:
                (init,_,_,_,_,_,name)=f.constraints[i]
                test_exp=lambda t:True
            if name in f.xnames:
                ind=f.xnames.index(name)
                cstr[i]=np.where(test_exp(0.),init(x0[ind],0.,h0),cstr[i])
            else:
                ind=f.ynames.index(name)
                cstr[i]=np.where(test_exp(0.),init(y0[ind],0.,h0),cstr[i])

    _,xf,tf,yf,hf,cstr,ifinal,_=while_loop(cond_fn,body_fn,
                                         (x0,x0,0.,y0,h0,cstr,i0,c0))
    if hasattr(f,'state'):
        f.state=ifinal
    if hasattr(f,'constraints'):
        for i in f.constraints.keys():
            if isinstance(f.constraints[i][1],tuple):
                _,(_,_,fin,_,_,_,_)=f.constraints[i]
            else:
                (_,_,fin,_,_,_,_)=f.constraints[i]
            cstr[i]=fin(tf,cstr[i],T)

    if hasattr(f,'state'):
        return (tf,xf,yf,cstr,ifinal)
    else:
        return (tf,xf,yf,cstr)


@_odeint45_extract.defjvp
def _odeint45_extract_jvp(f,h0,tol, primals, tangents):
    x0,T, *P = primals
    dx0,dT, *dP = tangents
    nPdP = len(P)

    if hasattr(f,'state'):
        xf,yf,cstr,tf,dtf,dxf,dyf,dcstr,states=odeint45_extract_etendu(f,
                        nPdP,h0, tol, x0,dx0,T,dT, *P, *dP)
        return (tf,xf,yf,cstr,states),(dtf,dxf,dyf,dcstr,states)
    else:
        xf,yf,cstr,tf,dtf,dxf,dyf,dcstr=odeint45_extract_etendu(f,
            nPdP,h0,tol, x0,dx0,T,dT, *P, *dP)
        return (tf,xf,yf,cstr),(dtf,dxf,dyf,dcstr)


def odeint45_extract_etendu(f,nPdP,h0,tol,x0,dx0,T,dT,*P_and_dP):
    P,dP = P_and_dP[:nPdP],P_and_dP[nPdP:]
    type,cond_stop=f.stop

    def cond_fn(state):
        x_prev2,x_prev,_,_,_,t_prev, h_prev,cstr,_,_,_ = state
        if type=='threshold':
            val,seuil=cond_stop(x_prev,f.xnames)
            valp,_ = cond_stop(x_prev2,f.xnames)
            return (h_prev>0) & (np.sign(val-seuil)==np.sign(valp-seuil))
        else:
            return (h_prev > 0) & cond_stop(t_prev,t_prev+h_prev,cstr)


    def body_fn(state):
        _,x_prev,dx_prev,y_prev,dy_prev,t_prev, h_prev,cstr,\
                dcstr,i_prev,c_prev= state

        x_now,t_now,y_now,h_now,i_now,c_now=next_step_simulation(x_prev,t_prev,
                                        y_prev,i_prev,c_prev,h_prev,f,tol,T,*P)
        dx_now,dy_now=next_der_step_simulation(x_prev,t_prev,dx_prev,x_now,
                                    t_now,h_prev,f, nPdP,*P_and_dP)

        if type=='threshold':
            output,seuil=cond_stop(x_now,f.xnames)
            outputprev,_=cond_stop(x_prev,f.xnames)
            condition=np.sign(output-seuil)!=np.sign(outputprev-seuil)
            x_now,h_prev,t_now,y_now=cond(condition,lambda state:
                compute_new_point(x_now,x_prev,t_prev,t_now,y_prev,y_now,
                output-seuil,outputprev-seuil),lambda state:state,(x_now,h_prev,
                                                                t_now,y_now))
            x_now,t_now,y_now,h_now,i_now,c_now=cond(condition,lambda state:
                next_step_simulation(x_prev,t_prev,y_prev,i_prev,c_prev,h_prev,
                f,tol,T,*P),lambda state:state,(x_now,t_now,y_now,h_now,i_now,
                                                c_now))
            dx_now,dy_now=cond(condition,lambda state:next_der_step_simulation
                (x_prev,t_prev,dx_prev,x_now,t_now,h_prev,f, nPdP,*P_and_dP),
                               lambda state:state,(dx_now,dy_now))

        elif isinstance(type,float):
            x_now,y_now=cond(t_now>type,lambda state:interpolation(x_prev,y_prev,
                t_prev,x_now,y_now,t_now,type),lambda state:state,(x_now,y_now))
            t_now=np.where(t_now>type,type,t_now)
            h_prev=np.where(t_now>type,type-t_prev,h_prev)


        if hasattr(f,'constraints'):
            for i in f.constraints.keys():
                if isinstance(f.constraints[i][1], tuple):
                    test_exp,(_,expression,_,_,der_expression,_,name)=\
                        f.constraints[i]
                else:
                    (_,expression,_,_,der_expression,_,name)=f.constraints[i]
                    test_exp = lambda t: True
                if name in f.xnames:
                    ind=f.xnames.index(name)
                    cstr[i] =np.where(test_exp(t_now),expression(t_prev,
                        x_prev[ind],t_now,x_now[ind], cstr[i],h_prev,T),cstr[i])
                    dcstr[i]= np.where(test_exp(t_now),der_expression(
                        t_prev,x_prev[ind],dx_prev[ind],t_now,x_now[ind],dx_now
                        [ind],cstr[i],dcstr[i],h_prev,T),dcstr[i])
                else:
                    ind=f.ynames.index(name)
                    cstr[i] =np.where(test_exp(t_now),expression(t_prev,
                        y_prev[ind],t_now,y_now[ind],cstr[i],h_prev,T),cstr[i])
                    dcstr[i]= np.where(test_exp(t_now),der_expression(
                        t_prev,y_prev[ind],dy_prev[ind],t_now,y_now[ind],dy_now
                        [ind],cstr[i],dcstr[i],h_prev,T),dcstr[i])

        return x_prev,x_now,dx_now,y_now,dy_now,t_now,h_now,cstr,dcstr,i_now,\
               c_now

    cstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))#INITIALISATION
    dcstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))

    for element in f.__dict__.keys(): # pour eviter erreurs de code
        if hasattr(f.__dict__[element],'primal'):
            f.__dict__[element]=f.__dict__[element].primal
    if hasattr(f,'state'):
        i0=f.state
    else:
        i0=0
    if hasattr(f,'commande'):
        _,c0=f.commande(0.,T)
    else:
        c0=0
    tempP,tempdP=None,None
    if hasattr(f,'initialize'):
        tempP,tempdP=P,dP
        P,dP=jvp(f.initialize,(*P,),(*dP,))
    y0=f.output(x0,0.,*P)
    dy0=jvp(f.output,(x0,0.,*P),(dx0,0.,*dP))[1]
    if hasattr(f,'initialize'):
        P,dP=tempP,tempdP
    if hasattr(f,'constraints'):
        for i in f.constraints.keys():
            if isinstance(f.constraints[i][1], tuple):
                test_exp,(init,_,_,dinit,_,_,name) = f.constraints[i]
            else:
                (init,_,_,dinit,_,_,name) = f.constraints[i]
                test_exp = lambda t: True
            if name in f.xnames:
                ind=f.xnames.index(name)
                cstr[i]=np.where(test_exp(0.),init(x0[ind],0.,h0),
                             cstr[i])
                dcstr[i]=np.where(test_exp(0.),dinit(x0[ind],dx0[ind],
                                    0.,h0),dcstr[i])
            else:
                ind=f.ynames.index(name)
                cstr[i]=np.where(test_exp(0.),init(y0[ind],0.,h0),
                             cstr[i])
                dcstr[i]=np.where(test_exp(0.),dinit(y0[ind],dy0[ind],
                                    0.,h0),dcstr[i])

    xfm1,xf,dxf,yf,dyf,tf,hf,cstr,dcstr,ifinal,_= while_loop(cond_fn,body_fn,
                            (x0,x0,dx0,y0,dy0,0.,h0,cstr,dcstr,i0,c0))
    if hasattr(f,'state'):
        f.state=ifinal
    if hasattr(f,'initialize'):
        P=f.initialize(*P)
    if hasattr(f,'constraints'):
        for i in f.constraints.keys():
            if isinstance(f.constraints[i][1],tuple):
                _,(_,_,fin,_,_,der_fin,name)=f.constraints[i]
            else:
                (_,_,fin,_,_,der_fin,name)=f.constraints[i]
            if name in f.xnames:
                ind = f.xnames.index(name)
                cstr[i]=fin(tf,cstr[i],T)
                dcstr[i]=der_fin(tf,cstr[i],T,dcstr[i],dT,xf[ind])
            else:
                ind = f.ynames.index(name)
                cstr[i]=fin(tf,cstr[i],T)
                dcstr[i]=der_fin(tf,cstr[i],T,dcstr[i],dT,yf[ind])

    if type=='threshold': # partial derivatives of ts
        dout,_=cond_stop(dxf,f.xnames)
        xseuil,_=cond_stop(f.derivative(xf,tf,*P),f.xnames)
        dtf=-(1/xseuil)*dout
    elif type=='steady_state':
        ind_rp=f.xnames.index(f.last_var_bf_rp)
        xseuil=f.derivative(xf,tf,*P)[ind_rp]
        dtf=-(1/xseuil)*dxf[ind_rp]
    else:
        dtf=0.
    if hasattr(f,'state'):
        return xf,yf,cstr,tf,dtf,dxf,dyf,dcstr,ifinal
    else:
        return xf,yf,cstr,tf,dtf,dxf,dyf,dcstr


################################################################################
def T_pair(T):
    return lambda t:(t//T)%2==0

def T_impair(T):
    return lambda t:(t//T)%2!=0

def T_numero(T,n,i):
    return lambda t:(t//T)%n!=i

def Min(name):
    def init(x0,t0,h0):
        return x0
    def expression(t_prev,x_prev,t_now,x_now,cstr,h_prev,_):
        return np.minimum(x_now,cstr)
    def fin(tf,cstr,_):
        return cstr
    def dinit(x0,dx0,t0,h0):
        return dx0
    def dexpression(t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,_):
        return np.where(np.minimum(cstr,x_now)==x_now,dx_now,dcstr)
    def dfin(tf,cstr,_,dcstr,dT,xf):
        return dcstr
    return init,expression,fin,dinit,dexpression,dfin,name

def Max(name):
    def init(x0,t0,h0):
        return x0
    def expression(t_prev,x_prev,t_now,x_now,cstr,h_prev,_):
        return np.maximum(x_now,cstr)
    def fin(tf, cstr, _):
        return cstr
    def dinit(x0, dx0, t0, h0):
        return dx0
    def dexpression(t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,_):
        return np.where(np.maximum(cstr,x_now)==x_now,dx_now,dcstr)
    def dfin(tf, cstr, _, dcstr, dT, xf):
        return dcstr
    return init, expression, fin, dinit, dexpression, dfin,name

def moy(name):
    def init(x0,t0,h0):
        return 0.
    def expression(t_prev,x_prev,t_now,x_now,cstr,h_prev,_):
        return cstr+0.5*h_prev*(x_prev+x_now)
    def fin(tf,cstr,_):
        return cstr/tf
    def dinit(x0,dx0,t0,h0):
        return 0.
    def dexpression(t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,_):
        return dcstr+0.5*h_prev*(dx_prev+ dx_now)
    def dfin(tf,cstr,_,dcstr,dT,xf):
        return dcstr/tf
    return init, expression, fin, dinit, dexpression, dfin,name

def eff(name):
    def init(x0,t0,h0):
        return 0.
    def expression(t_prev,x_prev,t_now,x_now,cstr,h_prev,_):
        return cstr+0.5*h_prev*(x_prev**2+x_now**2)
    def fin(tf,cstr,_):
        return np.sqrt(cstr/tf)
    def dinit(x0,dx0,t0,h0):
        return 0.
    def dexpression(t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,_):
        return dcstr+0.5*h_prev*(2*x_prev*dx_prev+2*x_now* dx_now)
    def dfin(tf,cstr,_,dcstr,dT,xf):
        return dcstr/(2*tf*cstr)
    return init, expression, fin, dinit, dexpression, dfin,name

def min_T(T,name):
    def init(x0,t0,h0):
        return x0
    def expression(t_prev,x_prev,t_now,x_now,cstr,h_prev,_):
        return np.where((t_prev//T)==(t_now//T),np.minimum(x_now,cstr),x_now)
    def fin(tf,cstr,_):
        return cstr
    def dinit(x0,dx0,t0,h0):
        return dx0
    def dexpression(t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,_):
        return jvp(expression,(t_prev,x_prev,t_now,x_now,cstr,h_prev,_),
                   (0.,dx_prev,0.,dx_now,dcstr,0.,0.))[1]#np.where((t_prev//T)==(t//T),np.where(np.minimum(cstr,
                #x)==x,dx,dcstr),dx)#
    def dfin(tf,cstr,_,dcstr,dT,xf):
        return dcstr
    return init, expression, fin, dinit, dexpression, dfin,name

def max_T(T,name):
    def init(x0,t0,h0):
        return x0
    def expression(t_prev,x_prev,t_now,x_now,cstr,h_prev,_):
        return np.where((t_prev//T)==(t_now//T),np.maximum(x_now,cstr),x_now)
    def fin(tf,cstr,_):
        return cstr
    def dinit(x0,dx0,t0,h0):
        return dx0
    def dexpression(t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,_):
        return jvp(expression,(t_prev,x_prev,t_now,x_now,cstr,h_prev,_),
                   (0.,dx_prev,0.,dx_now,dcstr,0.,0.))[1]#np.where((t_prev//T)==(t//T),np.where(np.maximum(cstr,
                #x)==x,dx,dcstr),dx)#
    def dfin(tf,cstr,_,dcstr,dT,xf):
        return dcstr
    return init, expression, fin, dinit, dexpression, dfin,name

def moy_T(name):
    def init(x0,t0,h0):
        return 0.
    def expression(t_prev,x_prev,t_now,x_now,cstr,h_prev,T):
        return np.where((t_prev//T)==(t_now//T),cstr+0.5*h_prev*(x_prev+x_now),
                        0.)
    def fin(tf,cstr,T):
        return cstr/T
    def dinit(x0,dx0,t0,h0):
        return 0.
    def dexpression(t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,T):
        return np.where((t_prev//T)==(t_now//T),dcstr+0.5*h_prev*(dx_prev+
                                                                  dx_now),0.)
    def dfin(tf,cstr,T,dcstr,dT,xf):
        return dcstr/T+((xf-cstr)/T)*dT
    return init, expression, fin, dinit, dexpression, dfin,name

def eff_T(name):
    def init(x0,t0,h0):
        return 0.
    def expression(t_prev,x_prev,t_now,x_now,cstr,h_prev,T):
        return np.where((t_prev//T)==(t_now//T),cstr+0.5*h_prev*(x_prev**2+
                                                                 x_now**2),0.)
    def fin(tf,cstr,T):
        return np.sqrt(cstr/T)
    def dinit(x0,dx0,t0,h0):
        return 0.
    def dexpression(t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,T):
        return np.where((t_prev//T)==(t_now//T),dcstr+0.5*h_prev*(2*x_prev*
                                    dx_prev+2*x_now*dx_now),0.)
    def dfin(tf,cstr,T,dcstr,dT,xf):
        return dcstr/(2*T*cstr)+(xf**2-cstr**2)/(2*cstr*T)*dT
    return init, expression, fin, dinit, dexpression, dfin,name


def steady_state(T,nbT,names_var,a=1e-5):
    constr = {}
    for i in range(len(names_var)):
        constr[names_var[i]+'_min']=(T_pair(nbT * T),
                                     min_T(nbT * T, names_var[i]))
        constr[names_var[i]+'_minimp']=(T_impair(nbT * T),
                                     min_T(nbT * T, names_var[i]))
        constr[names_var[i]+'_max']=(T_pair(nbT * T),
                                     max_T(nbT * T, names_var[i]))
        constr[names_var[i]+'_maximp']=(T_impair(nbT * T),
                                     max_T(nbT * T, names_var[i]))
    def regime_perm(t_prev,t,cstr):
        vectp,vectimp=np.zeros(2*len(names_var)),np.zeros(2*len(names_var))
        for i in range(len(names_var)):
            vectp=vectp.at[i].set(cstr[names_var[i]+'_min'])
            vectp=vectp.at[2*i+1].set(cstr[names_var[i]+'_max'])
            vectimp=vectimp.at[i].set(cstr[names_var[i]+'_minimp'])
            vectimp=vectimp.at[2*i+1].set(cstr[names_var[i]+'_maximp'])
        return np.bitwise_not(np.bitwise_and(np.allclose(vectp,vectimp,atol=a),
                    np.not_equal(t_prev//T,t//T)))
    return ('steady_state',regime_perm),constr

def threshold(ind,threshold_=0.):
    return ('threshold', lambda x,names: (x[names.index(ind)], threshold_))

def final_time(tf):
    return (tf,lambda t_prev,t,cstr:t_prev<tf)

