# -*- coding: utf-8 -*-
"""check_dumbsat_chealy5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1r3_pNKtJt_nAjuxWrm5OJbBdLm75vUs4
"""

#!/usr/bin/env python3

# Catherine Healy
# This file solves the input files for 2SAT using dumbsat to verify the accuracy.

import time
import csv
import dataclasses
import numpy as np
import matplotlib.pyplot as plt

@dataclasses.dataclass
class WFF:
    problem_number: int # Problem Number
    n_variables:    int # Number of variables
    satisfiability: str # S for satisfieable, U for unsatisfiable, ? for unknown
    all_clauses:     list[list[int]] # store the clauses as a list of ints
    n_clauses:      int = 0 # Number of clauses (initialized ot 0)
    time_to_solve:   int  = 0 # Keep track of how long it took to solve
    n_literals: int = 0 # Equal to n_clauses * 2


# This function solves a 2-SAT in polynomial time
def solveSAT(my_wffs: list[WFF]):
    for wff in my_wffs:
        start = time.time()
        if(dumbSAT(wff)==True):
            wff.satisfiability = "S"
        else:
            wff.satisfiability = "U"
        end = time.time()
        wff.time_to_solve = int((end-start)*1e6)

        # This function generates the output in a csv file format. The CSV includes information about
# how long the operation took and and whether the wff is unsatisfiable or not.
def generate_csv_output(my_wffs):
    with open('test_dumbsat_chealy5.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        master_list = []
        for wff in my_wffs:
            mylist = [
                (wff.n_clauses * 2), # n_clauses * 2 is actually # of literals in 2SAT
                wff.time_to_solve,
                wff.satisfiability
            ]
            master_list.append(mylist)
        writer.writerows(master_list)  # Write multiple rows

# This function generates the plot for the timing analysis
def make_plot(my_wffs):
    n_literals = [wff.n_literals for wff in my_wffs]
    time_to_solve = [wff.time_to_solve for wff in my_wffs]

    plt.figure(figsize=(10, 6))
    plt.title('DumbSAT Time Analysis')
    plt.xlabel('Problem Size (Number of Literals)')
    plt.ylabel('Time to Solve (microseconds)')
    plt.grid(True)
    colors = []
    # Color the graph so that satisfiable points are greeen and unsatisfiable points
    # are read.
    for wff in my_wffs:
        if wff.satisfiability == 'S':
            colors.append('green')  # Satisfiable
        elif wff.satisfiability == 'U':
            colors.append('red')    # Unsatisfiable


    plt.scatter(x, y, color=colors, alpha=0.5)

    plt.legend()
    plt.savefig('plots_DUMBSAT_chealy5.png') # Save the file for submission
    plt.show() # Actually show the plot

# Dumbsat function that was provided wiht slight modifications
def dumbSAT(wff):
    Wff = wff.all_clauses
    Nvars = wff.n_variables
    Nclauses = wff.n_clauses
    Assignment=list(0 for x in range(wff.n_variables+2))
    # Adding a print statement because it is SO slow
    print(f"Parsing WFF number {wff.problem_number} with {Nvars} variables and {Nclauses} clauses.")
# Run thru all possibilities for assignments to wff
# Starting at a given Assignment (typically array of Nvars+1 0's)
# At each iteration the assignment is "incremented" to next possible
# At the 2^Nvars+1'st iteration, stop - tried all assignments
    Satisfiable=False
    while (Assignment[Nvars+1]==0):
        # Iterate thru clauses, quit if not satisfiable
        for i in range(0,Nclauses): #Check i'th clause
            Clause=Wff[i]
            Satisfiable=False
            for j in range(0,len(Clause)): # check each literal
                Literal=Clause[j]
                if Literal>0: Lit=1
                else: Lit=0
                VarValue=Assignment[abs(Literal)] # look up literal's value
                if Lit==VarValue:
                    Satisfiable=True
                    break
            if Satisfiable==False: break
        if Satisfiable==True: break # exit if found a satisfying assignment
        # Last try did not satisfy; generate next assignment)
        for i in range(1,Nvars+2):
            if Assignment[i]==0:
                Assignment[i]=1
                break
            else: Assignment[i]=0
    return Satisfiable

def main():
    add_clauses = 0 # initialize
    my_wffs = []
    one_clause = []
    all_clauses = []
    n_clauses = 0
    problem_number = 0
    n_variables = 0
    satisfiability = 'S'
    #file_name = "2SAT.cnf.csv" # Provided test file
    file_name = "data_2SAT_chealy5.csv"
    # Parse the provided test file into a list of WFFs
    with open(file_name, mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            # Create wffs based on the format. If c detected assign problem
            if lines[0]=='c':
                problem_number = int(lines[1])
                satisfiability = lines[3]
                continue

            if lines[0]=='p':
                n_variables = int(lines[2])
                n_clauses = int(lines[3])
                add_clauses = 0
                continue
            # Actually create the list of clauses for the wff
            if n_clauses > add_clauses:
                for term in lines: # Convert to int
                    if term == "": #skip empty string
                        continue
                    if term == "0":
                        continue
                    one_clause.append(int(term))
                all_clauses.append(one_clause)
                add_clauses += 1
                one_clause = []

            if n_clauses == add_clauses:
                # Actually create the wff
                created_wff = WFF(
                    problem_number=problem_number,
                    n_variables=n_variables,
                    satisfiability=satisfiability,
                    all_clauses=all_clauses,
                    n_clauses = n_clauses,
                    n_literals = n_clauses *2
                )
                my_wffs.append(created_wff)
                all_clauses = [] # Reset list

    solveSAT(my_wffs) # call the sat solver

    make_plot(my_wffs)

    generate_csv_output(my_wffs)


if __name__ == '__main__':
    main()