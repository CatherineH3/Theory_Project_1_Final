# -*- coding: utf-8 -*-
"""code_2SAT_chealy5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18wG-WeNkK0eH_LR3_6X0lQf1oujgD_m3
"""

#!/usr/bin/env python3

# Catherine Healy
# Theory of Computing Project 1
# Polynomial Time 2SAT solver using DPLL Algorithm
# To run in terminal: ./code_2SAT_chealy5.py
# I assumed the test files are properly formatted.
# I will run the test file that was provided.
import time
import csv
import dataclasses
import matplotlib.pyplot as plt
import numpy as np

@dataclasses.dataclass
class WFF:
    problem_number: int # Problem Number
    n_variables:    int # Number of variables
    satisfiability: str # S for satisfieable, U for unsatisfiable, ? for unknown
    all_clauses:     list[list[int]] # store the clauses as a list of ints
    n_clauses:      int = 0 # Number of clauses (initialized ot 0)
    time_to_solve:   int  = 0 # Keep track of how long it took to solve
    n_literals:     int = 0 # number of literals is number of clauses * 2
# Note: I used a dataclass because it seemed like the best way to store information
# about a variety of types.

# Simplify the clause based on the literal assignment.
def unit_propagate(literal, clauses):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue  # If the literal is in the clause, it is satisfied (they are ORed
            # together). Remove the clause (skip adding it to new clause) because it is ANDing a true
            # clause, so it can be removed
        new_clause = [x for x in clause if x != -literal] # Create a new clause. We exclude
        # the negation of the literal because it is like ORing a false so it is not needed.
        new_clauses.append(new_clause)
    return new_clauses # Return a new simplified clause after the propogation.

# Pure literals can be removed. Pure literals are literals that appear without their negation
def remove_pure_literal(clauses):
    # Count the number of literals using a dict
    literal_count = {}
    for clause in clauses:
        for literal in clause:
            if literal not in literal_count:
                literal_count[literal] = 0
            literal_count[literal] += 1
    # Actually identify the pure literals.
    pure_literals = []
    for lit, count in literal_count.items():
        if -lit not in literal_count: # If their negation is not found, it is a pure literal
            pure_literals.append(lit)
    # propogate on the pure literal
    for lit in pure_literals:
        clauses = unit_propagate(lit, clauses) # We want to propogate the pure literal
    return clauses

# Polynomial time solution: DPLL algorithm
def dpll(clauses):
    # Unit propagation: Check for clause with only 1 literal! Keep calling unit propogation
    # until there are no more unit clauses
    unit_clause_exists = True
    while unit_clause_exists:
        unit_clause_exists = False
        for clause in clauses:
            if len(clause) == 1: # Identify until clauses (clause of len 1)
                found_unit_clause = True
                unit_clause = clause
                # Send the literal to function. Unit clause only has one literal so unit_clause[0]
                clauses = unit_propagate(unit_clause[0], clauses)
                break

    # Remove the pure literals:
    # Pure literals are literals that appear without their negation.
    # If CNF clause has pure literal that is T, all those clauses are
    # satisfied and we can remove it. It will internally call unit_propogate to remove.
    clauses = remove_pure_literal(clauses)

    # Recursion Base case
    if not clauses: # No more clauses- all satisfied, satisfiable
        return True
    # If there is an empty clause, this is unsatisfiable because we want
    # the literal to be true, but no clauses remain.
    for clause in clauses: # Empty clause is unsatisfiable.
        if len(clause) == 0:
            return False

    # Choose a literal
    literal = None
    for clause in clauses:
        for item in clause:
            literal = item  # Choose the first literal found
            break
        if literal is not None:
            break  # if a valid literal, break out of loop

    if literal is None: # If no literals left to choose, all clauses must be satisfied
        return True  # All clauses are satisfied

    # Two recrusive calls: In one case, assume the literal is true and progogate. In the other, assume it is false
    # and propogate.
    return dpll(unit_propagate(literal, clauses)) or dpll(unit_propagate(-literal, clauses))


# This funciton calls dpll function to solve 2SAT in polynomial time. It also
# times the SATSOLVER.
def solveSAT(my_wffs: list[WFF]):
    for wff in my_wffs:
        start = time.time() # Start Timer
        if(dpll(wff.all_clauses)== True):
            wff.satisfiability = "S" # Satisfiable
        else:
            wff.satisfiability = "U" # unsatisfiable
        end = time.time() # Stop Timer
        wff.time_to_solve = int((end-start)*1e6) # Time should be in micrseconds

# This function generates the output in a csv file format. The CSV includes information about
# how long the operation took and and whether the wff is unsatisfiable or not.
def generate_csv_output(my_wffs):
    with open('output_chealy5.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        csv_entry = []
        for wff in my_wffs:
            # Add the number of literals and time (graphing time) and satisfiability
            mylist = [
                wff.n_literals, # n_clauses * 2 is actually # of literals in 2SAT
                wff.time_to_solve,
                wff.satisfiability
            ]
            csv_entry.append(mylist)
        header = ['Number of Literals', 'Execution Time', 'Satisfiability']
        writer.writerow(header)

        writer.writerows(csv_entry)  # Write multiple rows

# This function generates the plot for the timing analysis
def make_plot(my_wffs):
    n_literals = [wff.n_literals for wff in my_wffs] # X is a list of the n_literals for each wff
    time_to_solve = [wff.time_to_solve for wff in my_wffs] # Y is the list of the time for each wff

    plt.figure(figsize=(10, 6))
    plt.title('Solution Computation Time vs. Problem Size')
    plt.xlabel('Problem Size (Number of Literals)')
    plt.ylabel('Time to Solve (microseconds)')
    plt.grid(True)
    colors = []
    # Color the graph so that satisfiable points are green and unsatisfiable points
    # are read
    for wff in my_wffs:
        if wff.satisfiability == 'S':
            colors.append('green')  # Satisfiable
        elif wff.satisfiability == 'U':
            colors.append('red')    # Unsatisfiable
    plt.scatter(n_literals, time_to_solve, color=colors, alpha=0.5) # x=n_literals, y=time_to_solve

    # For the trend line, I will use polynomial because we are trying to
    # implement the 2SAT in polynomial time. I looked at some online documentation because
    # I am not very familiar with this: https://numpy.org/doc/2.0/reference/routines.polynomials-package.html#module-numpy.polynomial
    degree = 2 # Initially assign degree to 2. Not sure if I should change.
    coeffs = np.polynomial.polynomial.Polynomial.fit(n_literals, time_to_solve, degree)

    # Get the values for x in the trend line
    x_fit = np.linspace(min(n_literals), max(n_literals), 100)
    y_fit = coeffs(x_fit)

    # Plot the trend line
    plt.plot(x_fit, y_fit, color='blue', label=f'Polynomial fit (degree {degree})')
    plt.legend()
    plt.savefig('plots_chealy5.png') # Save the file for submission
    plt.show() # Actually show the plot

def main():
    add_clauses = 0 # initialize
    my_wffs = []
    one_clause = []
    all_clauses = []
    n_clauses = 0
    problem_number = 0
    n_variables = 0
    satisfiability = 'S'
    file_name = "data_cnf_chealy5.csv" # Provided test file

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
                n_literals = n_clauses * 2 # This is true because it is fof 2SAT
                add_clauses = 0
                continue
            # Actually create the list of clauses for the wff
            if n_clauses > add_clauses:
                for term in lines: # Convert to int
                    if term == "": #skip empty string
                        continue
                    if term == "0":
                        continue
                    one_clause.append(int(term)) # Create clause
                all_clauses.append(one_clause) # Add clause ot list
                add_clauses += 1
                one_clause = [] # clear the clause holder

            if n_clauses == add_clauses:
                # Actually create the wff dataclass
                created_wff = WFF(
                    problem_number=problem_number,
                    n_variables=n_variables,
                    satisfiability=satisfiability,
                    all_clauses=all_clauses,
                    n_clauses=n_clauses,
                    n_literals = n_clauses * 2
                )
                my_wffs.append(created_wff)
                all_clauses = [] # Reset list

    # Actually call the SAT solver
    solveSAT(my_wffs) # Solve the wff

    # Generate the output file with the times and whether Satisfiable or not
    generate_csv_output(my_wffs)

    # Plot the timing analysis
    make_plot(my_wffs)


if __name__ == '__main__':
    main()