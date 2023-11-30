import jax.numpy as np
from jax.lax import switch,cond
from jax import custom_jvp,jvp
from functools import partial

def fonction(func):
    return lambda _: func()

def vect_temporel(debut,fin,pas):
    return np.linspace(debut,fin,int((fin-debut)/pas))

def indice_t(t,pas,debut=0.):
    return ((t-debut)/pas).astype(int)

def Switch(etat,funcs):
    return switch(etat,[fonction(func) for func in funcs],None)

def Condition(conditions,functions,state):
    for i in range(len(conditions)):
        state=cond(conditions[i],functions[i],lambda state:state,state)
    return state


###################################################### integrale
@partial(custom_jvp,nondiff_argnums=(0,1,2,3))
def integrale(t0,tf,pas,f,*inputs):
    longueur=(tf-t0)/int(tf/pas)
    res=f(*inputs)
    S=2*np.sum(res)-res[0]-res[-1]
    S*=longueur*0.5
    return S

@integrale.defjvp
def integrale_jvp(t0,tf,pas,f,primals,tangents):
    longueur=(tf-t0)/int(tf/pas)
    primal_dot,tangent_dot=jvp(f,primals,tangents)
    S=2*np.sum(primal_dot)-primal_dot[0]-primal_dot[-1]
    S*=longueur*0.5
    dS = 2*np.sum(tangent_dot)-tangent_dot[0]-tangent_dot[-1]
    dS *= longueur * 0.5
    return S,dS
############################################################################

def vect_freq(t0,tf,Te):
    M=int((tf-t0)/Te)
    freq=np.where(M//2==0,np.linspace(0.,(M/2-1)/(M*Te),M//2),
                          np.linspace(0.,(M-1)/(2*M*Te),M//2))
    return freq

def get_indice(names,valeur,output):
    if len(output)==1:
        return valeur[names.index(output[0])]
    else:
        return (valeur[names.index(i)] for i in output)