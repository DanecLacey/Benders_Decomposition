from pyomo.environ import *
########################################
## Loop Parameters and Initializations
########################################
LB = float("-inf")
UB = float("inf")
u_star, iter = 0, 0
eps = .1
i, y_bar = 0, []
########################################
## Master Problem Abstract Model
########################################
modelMP = AbstractModel(name = "Master problem")

modelMP.c = Param()
modelMP.d = Param()
modelMP.E = Param()
modelMP.F = Param()
modelMP.h = Param()

modelMP.y = Var(bounds = (-5,4), within = Integers)
modelMP.z_lower = Var()

modelMP.obj_master = Objective(
    expr = modelMP.z_lower, sense = minimize)

modelMP.cons_master = Constraint(
    expr = modelMP.z_lower >= modelMP.y)

#initialize value for y_bar (better way to do this?)
instanceMP = modelMP.create_instance('BD_parameters.dat')
solver = SolverFactory("glpk")
solver.solve(instanceMP)
a = value(instanceMP.y)
y_bar.append(a)
########################################
## Sub Problem Dual Abstract Model
########################################
modelSPD = AbstractModel(name = "Sub problem dual")
modelSPD.u = Var(within = NonNegativeReals)

modelSPD.c = Param()
modelSPD.d = Param()
modelSPD.E = Param()
modelSPD.F = Param()
modelSPD.h = Param()

modelSPD.constraint = Constraint(expr = modelSPD.E * modelSPD.u <= modelSPD.c)
modelSPD.obj = Objective(expr = (modelSPD.h - (modelSPD.F * y_bar[-1])) * modelSPD.u, sense = maximize)
########################################
## Utility functions
########################################
def solve_subproblem():
     instanceSPD = modelSPD.create_instance('BD_parameters.dat')

     solver = SolverFactory("glpk")
     solver.solve(instanceSPD)
     UB = value(instanceSPD.obj) + y_bar[-1]

     temp_u_star = (value(instanceSPD.u))
     return UB, temp_u_star

def add_cut(modelMP, u_star):
    exec(f'modelMP.cuts_add_{i} = Constraint( expr = modelMP.z_lower >= modelMP.d * modelMP.y + (modelMP.h - modelMP.F * modelMP.y) * u_star)')

def solve_masterproblem(u_star, lb):
    add_cut(modelMP, u_star)
    instanceMP = modelMP.create_instance('BD_parameters.dat')
    solver = SolverFactory("glpk")
    solver.solve(instanceMP)
    # instanceMP.pprint()
    a = value(instanceMP.y)
    y_bar.append(a)

    LB = max(lb, value(instanceMP.obj_master))
    return LB
########################################
## Algorithm
########################################
while (UB - LB > eps):

     LB = solve_masterproblem(u_star, LB)

     UB, u_star = solve_subproblem()

     print("Iteration: ", iter)
     print("UB: ",UB)
     print("LB: ",LB)
     print("u_star: ", u_star)
     print("y_bar: ", y_bar[-1])
     iter += 1; i += 1


print("Optimal value of the objective is: ", LB)
