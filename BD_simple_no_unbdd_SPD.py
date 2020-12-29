#instantiate parameters and sets
#first, instantiate abstract MP model
#then, instantiate abstract SPD, data will come from .dat file
#start loop
#   solve SPD via solver
#   set LB
#   add cut to MP
#   solve MP
#   update UB

#Where does u_star come from??? u_star is optimal solution of SPD
#Big question, how to set a variable to an optimal solution...?

from pyomo.environ import *

###########################################################################
#   Master problem set-up
###########################################################################

#initialize master problem
modelMP = AbstractModel(name = "Master problem")

#initialize parameters to be used
UB = 'inf'; LB = '-inf' #initial bounds
i = 0, N = [], a = {}, b = {} #used in refeshing optimality cuts for MP
modelMP.c = Param()
modelMP.d = Param()
modelMP.E = Param()
modelMP.F = Param()
modelMP.h = Param()
modelMP.eps = Param()
modelMP.y_star = Param(initialize = 10) #initial feasible integer solution

#initialize variables to be optimized
modelMP.y = Var(within = Integers, bounds = (-5, 4))
modelMP.z = Var(within = NonNegativeReals)

#initialize objective function
modelMP.obj = Objective(expr = modelMP.z, sense = maximize)

#optimality constraints to be called later
def optimality_cuts(model):
    return modelMP.z >= modelMP.d * modelMP.y + (modelMP.h - modelMP.F * modelMP.y) * u_star
            
###########################################################################
#   Sub problem dual set-up
###########################################################################

#initialize sub problem dual model
modelSPD = AbstractModel(name = "Sub problem dual")

#initialize parameters to be used
#all come from master problem

#initialize variables to be optimized
modelSPD.u = Var(within = NonNegativeReals)

#initialize objective function
def object_rule(model): #model arguement is necessary for using as a "rule"
    return (modelMP.h - (modelMP.F * modelMP.y_star)) * modelSPD.u
modelSPD.obj = Objective(rule = object_rule, sense = minimize)

#initialize constraints
def constraint_rule(model):
    return modelMP.E * modelSPD.u <= modelMP.c
#modelSPD.constraint = Constraint(modelMP.M, rule = constraint_rule)

###########################################################################
#   Algorithm
###########################################################################
while UB - LB < modelMP.eps:
    #solve SPD
    #set u_star = optimal sol
    LB = max(LB, (modelMP.d * modelMP.y_star) + /
             (modelMP.h - modelMP.F * modelMP.y_star) * u_star)
    
    #add another feasibility cut
    i++
    N = N.append(i)
    modelMP.optimality_cuts = Constraint(rule = optimality_cuts)
    
#     def optimality_cuts(model):
#     return modelMP.z >= modelMP.d * modelMP.y + 
# (modelMP.h - modelMP.F * modelMP.y) * u_star
for i in len(N):
    

    

