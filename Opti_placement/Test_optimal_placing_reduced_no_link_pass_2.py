# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 09:23:34 2019

@author: othmane.mounjid
"""

### Load paths 
import os 
import sys
Path_parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,Path_parent_directory + "\\Plotting")

####### Import liraries 
import Optimal_placing_reduced_no_link_pass_2 as op_place_pass
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotting as pltg

###############################################################################
###############################################################################
########################################## End functions ######################
###############################################################################
###############################################################################

#### Compute the result
######### Initialize the parameters ::Intensity values
path = "Data\\"
filename = "Intens_val_qr.csv"
Intens_val = pd.read_csv(path + filename, index_col = 0)
Intens_val_bis = Intens_val[Intens_val['Spread'] == 1].groupby(['BB size']).agg({'Limit':'mean', 'Cancel': 'mean', 'Market': 'mean'}).loc[:10,:]
Intens_val_bis.reset_index(inplace = True)
Intens_val_bis.loc[0,['Cancel','Market']] = 0
    
######### Show the database
print(Intens_val_bis.head(10))

######### Theoretical solution :  numerical scheme
tol = 0.1
size_q = Intens_val_bis.shape[0]
nb_iter_scheme = 400
reward_exec_1 = lambda qsame,bb_pos: op_place_pass.reward_exec(qsame, bb_pos, gain = 6, cost_out = -0.6, cost_stay = -0.2)
df_bis = op_place_pass.Sol_num_scheme(nb_iter_scheme,size_q,Intens_val_bis,tol = tol,reward_exec_1 = reward_exec_1)


######### Simulation of the order book
##### Initialization of the parameters
qb_0 = 2# 4
bb_pos_0 = qb_0 -1
Lob_state_0 = [qb_0,bb_pos_0] 
write_option = True
nb_iter = 100
gamma = 0.1 ## learning rate
h_0_init = 5*np.ones((size_q,size_q+1))
h_0_Stay_init = np.ones((size_q,size_q+1))
h_0_Mkt_init = np.ones((size_q,size_q+1))
h_0 = np.array(h_0_init)
h_0_Stay = np.array(h_0_Stay_init)
h_0_Mkt = np.array(h_0_Mkt_init)
h_0_theo = op_place_pass.Read_h_0_theo(df_bis["Value_opt"].values,size_q,reward_exec_1)
Error = lambda x : op_place_pass.error_1(np.nan_to_num(h_0_theo),np.nan_to_num(x))

######### Test RL methods 
########### global parameters
nb_episode = 300 ## upper loop iterations
freq_print = 40
nb_iter = 100 ## inner loop iterations
qb_0 = 2 # 4
bb_pos_0 = qb_0 -1
Lob_state_0 = [qb_0,bb_pos_0] ## initial state
eta = 1 ## discount factor
write_option = False

########### Alg 2 : increase gamma same sign v2 : of the proximal gradient algorithm : 
h_0 = np.array(h_0_init)
h_0_Stay = np.array(h_0_Stay_init)
h_0_Mkt = np.array(h_0_Mkt_init)
inner_loop_func = op_place_pass.Lob_simu_inner_loop11
alpha_0 = 1
alpha_max = 3
r = 0.5
pctg_0 = 0.05
h_011,error_h011,nb_past_011,h_011_Stay,h_011_Mkt = op_place_pass.Lob_simu_super_Loop4(nb_episode,Intens_val_bis,nb_iter, inner_loop_func = inner_loop_func, gamma= gamma,Lob_state_0=Lob_state_0,freq_print=freq_print,size_q = size_q,Error=Error, write_option = write_option, h_0 = h_0, reward_exec = reward_exec_1, eta = eta, h_0_Stay = h_0_Stay, h_0_Mkt = h_0_Mkt, alpha_0 = alpha_0, alpha_max = alpha_max, r = r, pctg_0 = pctg_0)
print(error_h011)


###############################################################################
############################# Plot the improvement ############################
###############################################################################

###############################################################################
###############################################################################
###################### This is the first main plot ############################
###################### There is no other one below ############################
###############################################################################
###############################################################################


##### Plot v3
start = 0
end = 16
option_save = ""
path_Image = "Image"; ImageName = "\\improvement__optimal_placement_f"
df = [ [error_h011[start:end,0],np.log(error_h011[start:end,1])]]
labels = [" PASS "]
mark = ['o']
fig = plt.figure(figsize=(8,5))
pltg.Plot_plot(df,labels, xlabel ="Number of iterations", ylabel ="Log L2 - error",
               option=option_save, path =path_Image, ImageName=ImageName, Nset_tick_x = False, mark = mark)



###############################################################################
###############################################################################
############################# Plot the values #################################
###############################################################################
###############################################################################

###############################################################################
###############################################################################
###################### This is the second main plots ##########################
######################      value functions          ##########################
###############################################################################
###############################################################################



##### Plot the values
option=""; path = "Image"; ImageName="\\h___theo"; xtitle=""; figsize_=(8, 8)
a = 1; b = 1; subplot0 = 1; Nset_tick_x = False; annot =True; fmt = '.2g'; cbar = False; annot_size = 16
cmaps = [sns.diverging_palette(10,240,n=6)]; masks = [None]
tilde_size_q = size_q - 1
q_val_ = df_bis["Value_opt"]
x_val = np.arange(1,tilde_size_q+1)
y_val = np.arange(1,tilde_size_q+1)
nb_x = tilde_size_q
nb_y = tilde_size_q 
df_n_row = nb_x*nb_y
df = pd.DataFrame(np.zeros((df_n_row,3)),columns=['x','y','z'])
df['x'] = np.repeat(x_val,nb_y)
df['y'] = np.tile(y_val,nb_x)
df['z'] = q_val_#u_next_1
fig = plt.figure(figsize=figsize_)
pltg.Plot_sns_2(df.pivot("y", "x", "z"),option=option,path =path,ImageName=ImageName,xtitle=xtitle, xlabel = "", ylabel = "", annot = annot, fig = fig, a = a, b = b, subplot0 = subplot0, cbar = cbar, cmaps = cmaps, masks = masks, fmt = fmt, annot_size = annot_size )


##### Plot the result
option=""; path = "Image"; ImageName="\\h_011"; xtitle=""; figsize_=(8, 8)
a = 1; b = 1; subplot0 = 1; Nset_tick_x = False; annot =True; fmt = '.2g'; cbar = False; annot_size = 16
cmaps = [sns.diverging_palette(10,240,n=6)]; masks = [None]
q_val_ = np.around(h_011[1:,2:], decimals=1)
x_val = np.arange(1,size_q)
y_val = np.arange(1,size_q)
nb_x = size_q-1
nb_y = size_q-1
df_n_row = nb_x*nb_y
df = pd.DataFrame(np.zeros((df_n_row,3)),columns=['x','y','z'])
df['x'] = np.repeat(x_val,nb_y)
df['y'] = np.tile(y_val,nb_x)
df['z'] = q_val_.flatten()
fig = plt.figure(figsize=figsize_)
pltg.Plot_sns_2(df.pivot("y", "x", "z"),option=option,path =path,ImageName=ImageName,xtitle=xtitle, xlabel = "", ylabel = "", annot = annot, fig = fig, a = a, b = b, subplot0 = subplot0, cbar = cbar, cmaps = cmaps, masks = masks, fmt = fmt,annot_size=annot_size)



###############################################################################
###############################################################################
############################# Plot the ctrl ###################################
###############################################################################
###############################################################################

###############################################################################
###############################################################################
###################### This is the third main plots ###########################
######################      ctrl agents             ###########################
###############################################################################
###############################################################################




##### Plot the values
option=""; path =  "Image"; ImageName="\\ctrl_theo"; xtitle=""; figsize_=(8, 8)
a = 1; b = 1; subplot0 = 1; Nset_tick_x = False; annot =True; fmt = '.2g'; cbar = False; annot_size = 16
cmaps = [sns.diverging_palette(10,240,n=6)]; masks = [None]
tilde_size_q = size_q - 1
q_val_ = (df_bis["Limit"]>=df_bis["Market"]).astype(int)
for qsame in range(size_q-1): # qsame is the size
    q_val_[qsame*(size_q -1) + qsame +1: (qsame+1)*(size_q -1)] = np.nan
x_val = np.arange(1,tilde_size_q+1)
y_val = np.arange(1,tilde_size_q+1)
nb_x = tilde_size_q
nb_y = tilde_size_q 
df_n_row = nb_x*nb_y
df = pd.DataFrame(np.zeros((df_n_row,3)),columns=['x','y','z'])
df['x'] = np.repeat(x_val,nb_y)
df['y'] = np.tile(y_val,nb_x)
df['z'] = q_val_#u_next_1
fig = plt.figure(figsize=figsize_)
pltg.Plot_sns_2(df.pivot("y", "x", "z"),option=option,path =path,ImageName=ImageName,xtitle=xtitle, xlabel = "", ylabel = "", annot = annot, fig = fig, a = a, b = b, subplot0 = subplot0, cbar = cbar, cmaps = cmaps, masks = masks, fmt = fmt, annot_size = annot_size )


##### Plot the result
option=""; path = "Image"; ImageName="\\ctrl_h__011"; xtitle=""; figsize_=(8, 8)
a = 1; b = 1; subplot0 = 1; Nset_tick_x = False; annot =True; fmt = '.2g'; cbar = False; annot_size = 16
cmaps = [sns.diverging_palette(10,240,n=6)]; masks = [None]
q_val_ = (h_011_Stay >= h_011_Mkt)[1:,2:].astype(float)
for qsame in range(size_q-1): # qsame is the size
    q_val_[qsame,(qsame+1):] = np.nan
x_val = np.arange(1,size_q)
y_val = np.arange(1,size_q)
nb_x = size_q-1
nb_y = size_q-1
df_n_row = nb_x*nb_y
df = pd.DataFrame(np.zeros((df_n_row,3)),columns=['x','y','z'])
df['x'] = np.repeat(x_val,nb_y)
df['y'] = np.tile(y_val,nb_x)
df['z'] = q_val_.flatten()
fig = plt.figure(figsize=figsize_)
pltg.Plot_sns_2(df.pivot("y", "x", "z"),option=option,path =path,ImageName=ImageName,xtitle=xtitle, xlabel = "", ylabel = "", annot = annot, fig = fig, a = a, b = b, subplot0 = subplot0, cbar = cbar, cmaps = cmaps, masks = masks, fmt = fmt,annot_size=annot_size)