import pathlib
import os
python_path = pathlib.Path('.').absolute().parent.parent/'python'
os.sys.path.insert(1, str(python_path))

from sqp import SQP
from sqp_cpp import SQP_CPP
import numpy as np
import crocoddyl
import mim_solvers
from problems import create_lqr_problem


LINE_WIDTH = 100


print("TEST 1: python SQP = mim_solvers SQP".center(LINE_WIDTH, "-"))

problem, xs_init, us_init = create_lqr_problem()
ddp0 = SQP(problem)
ddp1 = SQP_CPP(problem)
ddp2 = mim_solvers.SolverSQP(problem)

ddp0.with_callbacks = True
ddp1.with_callbacks = True
ddp2.with_callbacks = True

ddp0.termination_tolerance = 1e-6
ddp1.termination_tolerance = 1e-6
ddp2.termination_tolerance = 1e-6



converged = ddp0.solve(xs_init, us_init, 10)
converged = ddp1.solve(xs_init, us_init, 10)
converged = ddp2.solve(xs_init, us_init, 10)

tol = 1e-4
assert np.linalg.norm(np.array(ddp0.xs) - np.array(ddp2.xs)) < tol, "Test failed"
assert np.linalg.norm(np.array(ddp0.us) - np.array(ddp2.us)) < tol, "Test failed"
assert np.linalg.norm(np.array(ddp1.xs) - np.array(ddp2.xs)) < tol, "Test failed"
assert np.linalg.norm(np.array(ddp1.us) - np.array(ddp2.us)) < tol, "Test failed"


assert ddp0.iter == 0
assert ddp1.iter == 0
assert ddp2.iter == 1


print("TEST PASSED".center(LINE_WIDTH, "-"))
print("\n")