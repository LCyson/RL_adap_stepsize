# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 23:24:35 2019

@author: othmane.mounjid
"""

####### Load paths 
import os 
import sys
Path_parent_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,Path_parent_directory + "\\Plotting")
sys.path.insert(0,Path_parent_directory + "\\Auxiliary")

####### Import liraries 
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import plotting as pltg
import Theo_sol_exec_cj as Thsolexecj
import Optimal_exe_cj_reduced_f_no_link_saga as opti_exe_saga


###############################################################################
###############################################################################
########################################## End functions ######################
###############################################################################
###############################################################################


#### Compute the result
######### Initialize the parameters 
A = 0.25
Q_max = 2
Q_min = -Q_max
T_max = 1
size_q = 80 ## always take it an even number : see size_nu
nb_iter = 100
Step_q = (2*Q_max)/size_q
Time_step = (T_max)/nb_iter
kappa = 0.1
phi = 1
alpha = 0.1
mu = 1
Step_x = 0.01
Step_s = 0.01
size_x = 10
size_s = 10
size_nu = size_q
x_min = -10
s_min = -10
sigma2 = 1 # 0.02 # 0.02
pdic = {  'A':A,
          'Q_max': Q_max,
          'Q_min': Q_min,
          'Step_q':Step_q,
          'Time_step':Time_step,
          'kappa':kappa,
          'phi':phi,
          'alpha':alpha,
          'mu':mu,
          'T_max':T_max,
          'Step_x':Step_x,
          'Step_s':Step_s,
          'Step_q':Step_q,
          'x_min':x_min,
          's_min':s_min,
          'q_min':Q_min ,
          'size_x':size_x,
          'size_s':size_s,
          'size_q':size_q,
          'size_nu':size_nu,
          'nb_iter':nb_iter,
          'sigma2':sigma2}
option_save = "" # "save"



######### Test (RL) methods
########### parameters initialization
gamma = 0.05 # 1/nb_episode #0.01#1/nb_episode
v_0_init = 1*np.ones(((pdic['nb_iter']+1),pdic['size_q']))
nb_episode = 5000 # 10000 # 5000 # 90000  #1200 # 2000 ## ## upper loop iterations
freq_print = 600 ## print frequency
########### Compute Theoretical values
v_theo = np.zeros(((pdic['nb_iter']+1),pdic['size_q']))
h_2 = Thsolexecj.Compute_h_2(pdic)
h_1 = Thsolexecj.Compute_h_1(100, h_2, pdic)
h_0 = Thsolexecj.Compute_h_0(100, h_1, pdic)
########### Compute Theoretical v_values 
q_values = np.arange(-pdic['Q_max'],pdic['Q_max'],pdic['Step_q'])
for i in range(nb_iter+1): # i = 0
    v_theo[i,:] = h_0[i] + h_1[i]*q_values - 0.5 * h_2[i] * q_values * q_values
Error = lambda x : opti_exe_saga.error_1(v_theo,x)



###############################################################################
############################# This one is longer ##############################
############################# To get the final function #######################
###############################################################################

########### Alg 2 :  SAGA:  test 2
v_0 = np.array(v_0_init) # 100*np.random.rand(pdic['nb_iter'])#
inner_loop_func = opti_exe_saga.Loop_within_episode_5_2
n_max =  1
_exp_mean = 1
pctg_0 = 0.001
v_07,error_v07,gamma_07 = opti_exe_saga.Loop_all_episode_2(nb_episode,pdic,  inner_loop_func= inner_loop_func, gamma= gamma,Error=Error,freq_print=freq_print,v_0 = v_0, n_max =  n_max, _exp_mean = _exp_mean, pctg_0 = pctg_0)
print(error_v07)
option_save = ""
if option_save == "save":
    pathfile = Path_parent_directory + "\\Data"; fileName_07 = "\\improvement__optimal_execution_v_07"
    fileName_07_v = "\\improvement__optimal_execution_values_07"
    np.save(pathfile + fileName_07, np.array(error_v07))
    np.save(pathfile + fileName_07_v, np.array(v_07))
option_load = "never"
if option_load == "load__carefully":
    error_v07_07 = np.load(pathfile + fileName_07 + '.npy')
    v07_07 = np.load(pathfile + fileName_07_v + '.npy')

###############################################################################
############################# Plot the improvement ############################
###############################################################################

##### Plot the improvement

##### Plot v2
start = 0
end = 170
end_1 = 300
option_save = ""
path_Image = Path_parent_directory + "\\Image"; ImageName = "\\improvement__optimal_execution_f_final_210000_iter_v2"
df = [ [error_v07[start:end,0],np.log(error_v07[start:end,1])]]
labels = ["SAGA"]
mark = ['']
bbox_to_anchor_0 = (0.05,.4)
fig = plt.figure(figsize=(8,5))
pltg.Plot_plot(df,labels, xlabel ="Number of iterations", ylabel ="Log L2 - error",
               option=option_save, path =path_Image, ImageName=ImageName, Nset_tick_x = False, mark = mark, bbox_to_anchor_0 = bbox_to_anchor_0)

###############################################################################
###############################################################################
############################# Plot the values #################################
###############################################################################
###############################################################################


##### Plot the values
option_save = ""
path_Image = Path_parent_directory + "\\Image"; ImageName = "\\improvement__optimal_execution_theo"; xtitle="theo values"
delta = 1
v_cj_rl = v_theo[:,delta:-delta].flatten() #v_reduced_bis.flatten()
#q_values = np.arange(-pdic['Q_max'],pdic['Q_max'],Step_q)
q_values = np.arange(Q_min + delta * Step_q,pdic['Q_max'] - delta * Step_q,Step_q)
time_values = np.arange(0,T_max+Time_step,Time_step)
bins = [time_values.shape[0],q_values.shape[0]]
pltg.Plot3D(time_values,q_values,v_cj_rl,bins,xlabel='time',ylabel='q values',zlabel='Value function',option=option_save,path =path_Image,ImageName=ImageName,xtitle=xtitle,
            elev0= 30, azim0=40, dist0= 12,optionXY =2, x_tickslabels =  False, x_ticksvalues = np.zeros(1))

##### Plot the values
option_save = ""
path_Image = Path_parent_directory + "\\Image" ; ImageName = "\\improvement__optimal_execution_07_210000_iter"; xtitle="v_07"
delta = 1
v_cj_rl = v_07[:,delta:-delta].flatten() #v_reduced_bis.flatten()
#v_cj_rl = v_05.flatten() #v_reduced_bis.flatten()
q_values = np.arange(Q_min + delta * Step_q,pdic['Q_max'] - delta * Step_q,Step_q)
#q_values = np.arange(Q_min ,pdic['Q_max'] ,Step_q)
time_values = np.arange(0,T_max+Time_step,Time_step)
bins = [time_values.shape[0],q_values.shape[0]]
pltg.Plot3D(time_values,q_values,v_cj_rl,bins,xlabel='time',ylabel='q values',zlabel='Value function',option=option_save,path =path_Image,ImageName=ImageName,xtitle=xtitle,
            elev0= 30, azim0=40, dist0= 12,optionXY =2, x_tickslabels =  False, x_ticksvalues = np.zeros(1))

