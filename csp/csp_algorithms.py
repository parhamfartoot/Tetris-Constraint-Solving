from .csp import CSP
from .csp_util import CSPUtil
from .variable import Variable


class CSPAlgorithms:

    # Here you will implement all the Constraint Solving Algorithms. Below are functions we think
    # will be helpful in your implementations. Please read the handout for specific instructions
    # for each algorithm.

    # Helpful Functions:
    # CSP.unassigned_variables() --> returns a list of the unassigned variables left in the CSP
    # CSP.assignments() --> returns a dictionary which holds variable : value pairs
    # CSP.extract_unassigned() --> returns the next unassigned variable in line
    # CSP.assign(variable, value) --> assigns the given value to the given variable
    # CSP.unassign(variable) --> unassigns the given variable (value = None)
    # CSP.constraints() --> returns a list of constraints for the CSPa
    # CSP.num_unassigned() --> returns the number of unassigned variables
    # Variable.domain() --> returns the domain of the variable instance
    # Constraint.check(variables, assignments) --> returns True iff the given variables and their assignments
    #                                              satisfy the constraint instance

    @staticmethod
    def backtracking(csp):
        # Qustion 3, your backtracking algorithm goes here.

        # Returns an assignment of values to the variables such that the constraints are satisfied. None
        # if no assignment is found.

        if csp.num_unassigned() == 0:
            return csp.assignments()

        var = csp.extract_unassigned()
        for val in var.domain():
            csp.assign(var, val)
            constraint_bool = True
            for constraint in csp.constraints():
                if csp.num_unassigned() == 0:
                    if not constraint.check(csp.variables(), csp.assignments()):
                        constraint_bool = False
                        break
            if constraint_bool:
                res = CSPAlgorithms.backtracking(csp)
                if res is not None:
                    return res

        csp.unassign(var)
        return

    @staticmethod
    def forward_checking(csp):
        # Question 4, your forward checking algorithm goes here.

        # Returns an assignment of values to the variables such that the constraints are satisfied. None
        # if no assignment is found.

        # Helpful Functions:
        # CSPUtil.forward_check(csp, constraint, var) --> returns True iff there is no DWO when performing
        #                                                 a forward check on the given constraint and variable.
        # CSPUtil.undo_pruning_for(var) --> undoes all pruning that was caused by forward checking the given variable.

        if csp.num_unassigned() == 0:
            return csp.assignments()

        var = csp.extract_unassigned()
        for val in var.active_domain():
            csp.assign(var, val)
            noDWO = True
            for constraint in csp.constraints():
                if csp.num_unassigned() == 1:
                    if not (CSPUtil.forward_check(csp, constraint, var)):
                        noDWO = False
                        break
            if noDWO:
                res = CSPAlgorithms.forward_checking(csp)
                if res is not None:
                    return res
            CSPUtil.undo_pruning_for(var)
        csp.unassign(var)
        return

    @staticmethod
    def gac(csp):
        # Question 6, your gac algorithm goes here.

        # Returns an assignment of values to the variables such that the constraints are satisfied. None
        # if no assignment is found.

        # Helpful Functions:
        # CSPUtil.gac_enfore(csp, var) --> returns True iff there is no DWO when attempting to enforce consistency
        #                                  on the constraints of the csp for the given variable.
        # CSPUtil.undo_pruning_for(var) --> undoes all pruning that was caused by forward checking the given variable.

        if csp.num_unassigned() == 0:
            return csp.assignments()

        var = csp.extract_unassigned()
        for val in var.domain():
            csp.assign(var, val)
            noDWO = True
            if not CSPUtil.gac_enforce(csp, var):
                noDWO = False
            if noDWO:
                res = CSPAlgorithms.gac(csp)
                if res is not None:
                    return res
            CSPUtil.undo_pruning_for(var)

        csp.unassign(var)
        return
