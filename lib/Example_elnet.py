##########################################
# Sample caller code for elnet
# 

import scipy
import ctypes 
from glmnet import glmnet
from glmnetControl import glmnetControl
from glmnetSet import glmnetSet

glmlib = ctypes.cdll.LoadLibrary('./GLMnet.so') # this is a bit of a pain. 
                                                # unless a new python console is started
                                                # the shared library will persist in memory
# load data (identical to QuickStartExample.RData)
baseDataDir= '/home/bbalasub/Desktop/Summer2016/glmnet/glmnet_R/'
y = scipy.loadtxt(baseDataDir + 'QuickStartExampleY.dat')
x = scipy.loadtxt(baseDataDir + 'QuickStartExampleX.dat')
y = y.astype(dtype = scipy.float64, order = 'F', copy = True)
x = x.astype(dtype = scipy.float64, order = 'F', copy = True)
# call elnet directly
#      subroutine elnet  (ka,parm,no,ni,x,y,w,jd,vp,cl,ne,nx,nlam,flmin,u    787 
#     *lam,thr,isd,intr,maxit,  lmu,a0,ca,ia,nin,rsq,alm,nlp,jerr)
######################################
# --------- INPUTS -------------------
######################################
# ka
ka_r = ctypes.c_int(1) # naive algo
# parm
parm_r = ctypes.c_double(1.0)
# no
no = len(y)
no_r = ctypes.c_int(no)
# ni
ni = x.shape[1]
ni_r = ctypes.c_int(ni)
# x
x_r = x.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
# y
y_r = y.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
# w
w = scipy.ones([no, 1], dtype = scipy.float64)
w_r = w.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
# jd
jd = scipy.ones([1], dtype = scipy.int64)
jd_r = jd.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
# vp
vp = scipy.ones([ni, 1], dtype = scipy.float64)
vp_r = vp.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
# cl
options = glmnetSet()
inparms = glmnetControl()
cl = options['cl']
cl[0, cl[0, :] == scipy.double('-inf')] = -1.0*inparms['big']    
cl[1, cl[1, :] == scipy.double('inf')]  =  1.0*inparms['big']   
if cl.shape[1] < ni:
    if cl.shape[1] == 1:
        cl = cl*scipy.ones([1, ni], dtype = scipy.float64)
    else:
        raise ValueError('ERROR: Require length 1 or nvars lower and upper limits')
else:
    cl = cl[:, 0:ni-1]
cl_r = cl.ctypes.data_as(ctypes.POINTER(ctypes.c_double))    
# ne
ne = ni + 1    
ne_r = ctypes.c_int(ne)
# nx
nx = ni
nx_r = ctypes.c_int(nx)
# nlam
nlam = 100
nlam_r = ctypes.c_int(nlam)
# flmin
flmin = 1.0e-4
flmin_r = ctypes.c_double(flmin)
# ulam
ulam   = scipy.zeros([1], dtype = scipy.float64)
ulam_r = ulam.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
# thr
thr = 1.0e-7
thr_r = ctypes.c_double(thr)
# isd
isd = 0
isd_r = ctypes.c_int(isd)
# intr
intr = 1
intr_r = ctypes.c_int(intr)
# maxit
maxit = 100000
maxit_r = ctypes.c_int(maxit)
######################################
# --------- OUTPUTS -------------------
######################################
# lmu
lmu = 0
lmu_r = ctypes.c_int(lmu)
# a0
a0   = scipy.zeros([nlam, 1], dtype = scipy.float64)
a0_r = a0.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
# ca
ca   = scipy.zeros([nx, nlam], dtype = scipy.float64)
ca_r = ca.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
# ia
ia   = scipy.zeros([nx, 1], dtype = scipy.int64)
ia_r = ia.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
# nin
nin   = scipy.zeros([nlam, 1], dtype = scipy.int64)
nin_r = nin.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
# rsq
rsq   = scipy.zeros([nlam, 1], dtype = scipy.float64)
rsq_r = rsq.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
# alm
alm   = scipy.zeros([nlam, 1], dtype = scipy.float64)
alm_r = rsq.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
# nlp
nlp = -1
nlp_r = ctypes.c_int(nlp)
# jerr
jerr = -1
jerr_r = ctypes.c_int(jerr)
# elnet
glmlib.elnet_(ctypes.byref(ka_r), 
              ctypes.byref(parm_r), 
              ctypes.byref(no_r), 
              ctypes.byref(ni_r),
              x_r, 
              y_r, 
              w_r, 
              jd_r, 
              vp_r, 
              cl_r, 
              ctypes.byref(ne_r), 
              ctypes.byref(nx_r), 
              ctypes.byref(nlam_r), 
              ctypes.byref(flmin_r), 
              ulam_r, 
              ctypes.byref(thr_r), 
              ctypes.byref(isd_r), 
              ctypes.byref(intr_r), 
              ctypes.byref(maxit_r), 
              ctypes.byref(lmu_r),
              a0_r, 
              ca_r, 
              ia_r, 
              nin_r, 
              rsq_r, 
              alm_r, 
              ctypes.byref(nlp_r), 
              ctypes.byref(jerr_r))

print(a0)

