import csp
from datetime import datetime
import copy

class Problem(csp.CSP):

    def __init__(self, input_file, boundary):
        # Place here your code to load problem from opened file object fh and
        # set variables, domains, graph, and constraint_function accordingly

        timetable = []
        weekly_class = []
        associations = []
        room = []
        student_class = []
        self.courses_dict = {}
        self.graph = {}
        self.result = None
        self.boundary = boundary

        if input_file is not None:
            # Read initial line
            line = input_file.readline()

            # If the file is not empty keep reading one line at a time, till the file is empty
            while line:
                
                # Split line in pieces delimited by whitespace
                line = line.split()

                # For these 3 first cases go over one line, split each piece and store as tuple
                if line[0] == 'T':
                    for i in range(len(line)-1):
                        temp = tuple(line[i+1].split(",")) # Split again to make tuples

                        # Only add timetable if it's earlier than the specified latest hour boundary
                        if int(temp[1]) < self.boundary:
                            timetable.append(temp)
                    del temp

                elif line [0] == 'W':
                    for i in range(len(line)-1):
                        temp = tuple(line[i+1].split(","))
                        weekly_class.append(temp)
                    del temp

                elif line [0] == 'A':
                    for i in range(len(line)-1):
                        temp = tuple(line[i+1].split(","))
                        associations.append(temp)

                        # Check if dictionary of current course exists
                        try:
                            self.courses_dict[temp[1]]
                        except:
                            self.courses_dict[temp[1]] = {}

                        self.courses_dict[temp[1]][temp[0]] = True
                    del temp

                # room is array of strings
                elif line [0] == 'R':
                    for i in range(len(line)-1):
                        room.append(line[i+1])

                # student_class is array of strings
                elif line [0] == 'S':
                    for i in range(len(line)-1):
                        student_class.append(line[i+1])

                # use realine() to read next line
                line = input_file.readline()

            # Get the domain T x R
            domains = self.combine_output(timetable, room, weekly_class)

            # Variables are W
            variables = weekly_class

            # The neighbors of each node are every other node 
            self.create_neighbors_dict(weekly_class)

            # Run CSP's innit
            super().__init__(variables, domains, self.graph, self.constraint_function)

        else:
            # Just leave domains and varibles as None, when no input_file is specified
            domains = None
            variables = None

    # C1 to C3 -> returns true if constraint is verified, false if not
    # C1: Each room can only hold 1 class at a time
    def check_C1(self, A, a, B, b):
        if a[0] == b[0] and a[1] == b[1] and a[2] == b[2]:
            return False
        return True
        
    # C2: Each student (class) can only attend a class at a time
    def check_C2(self, A, a, B, b):
        for key in self.courses_dict[A[0]].keys():
            # Check if the course of A is attended by a common class of B
            try:
                self.courses_dict[B[0]][key]

                # Check if both courses have a common schedule
                if a[0] == b[0] and a[1] == b[1]:
                    return False
            except:
                continue
        return True

    # C3: No two weekly class of the same course may occur on the same day 
    def check_C3(self, A, a, B, b):
        if a[0] == b[0] and A[0] == B[0] and A[1] == B[1]:
            return False
        return True

    # Check if all constraints are verified
    def constraint_function(self, A, a, B, b):
        return self.check_C1(A, a, B, b) and self.check_C2(A, a, B, b) and self.check_C3(A, a, B, b)

    def dump_solution(self, fh):
        # Place here your code to write solution to opened file object fh
        count = 0

        # Don't write the output if the solution is empty
        if self.result is None:
            return

        # Don't write the output if the solution is empty
        if self.result.keys() is None:
            return

        for key in self.result.keys():
            count = count + 1

            line = str(key[0]) + ',' + str(key[1]) + ',' + str(key[2]) + ' ' + str(self.result[key][0]) + ',' + str(self.result[key][1]) + ' ' + str(self.result[key][2])

            if count != len(self.result.keys()):
                line += '\n'
                
            fh.write(line)
        return

    # Make the output domain by getting all possible combinations of timetables (T) with rooms (R)
    def combine_output(self, T, R, W):
        output = {}

        for w in W:
            output[w] = {}
            output_list = []

            for t in T:
                for r in R:
                    output_tuple = (t[0], t[1], r)
                    output_list.append(output_tuple)
            
            output[w] = output_list

        return output

    # Create dictionary of neighbors of each node
    def create_neighbors_dict(self, W):
        for w in W:
            # Create a list of all the nodes except the current one
            tmp = list(W)
            tmp.remove(w)

            # Add list to neighbors of node w
            self.graph[w] = tmp
        
        return self.graph

    # Make an efficient copy of the Problem object
    def copy(self):
        problem_copy = Problem(None, None)
        problem_copy.courses_dict = self.courses_dict.copy()
        problem_copy.graph = self.graph.copy()
        problem_copy.domains = self.domains.copy()
        problem_copy.variables = self.variables.copy()
        problem_copy.boundary = self.boundary
        problem_copy.neighbors = self.neighbors.copy()
        problem_copy.initial = self.initial
        problem_copy.curr_domains = self.curr_domains.copy()
        problem_copy.nassigns = self.nassigns

        if self.result is not None:
            problem_copy.result = self.result.copy()

        return problem_copy

# Function to get the second element of a string, with values separated by comma, as an integer
def get_string_second_elem(stringX):
    return int(stringX.split(',')[1])

# Function to find the possible hours in a day that can be used to assign classes.
# This is useful for the list of boundary values, which are used to optimize the problem.
def get_possible_shift_hours(input_file):
    # Read initial line
    line = input_file.readline()

    # If the file is not empty keep reading one line at a time, till the file is empty
    while line:
        
        # Split line in pieces delimited by whitespace
        line = line.split()

        # For these 3 first cases go over one line, split each piece and store as tuple
        if line[0] == 'T':
            # Get a list of the hours of all shifts
            shift_hours = list(map(get_string_second_elem, line[1:]))

            # Earliest hour
            min_hour = min(shift_hours)

            # Latest hour
            max_hour = max(shift_hours)

            # List of all possible values, in an descending order, with no duplicates
            possible_hours = list(range(max_hour, min_hour, -1))

            break

        # If the line still isn't referent to the timetable slots set (T), continue searching
        line = input_file.readline()

    # Return the reading pointer to the beginning
    input_file.seek(0)

    return possible_hours
        
def solve(input_file, output_file):
    # Start counting the running time
    startTime = datetime.now()

    # Possible hours, in a descending order, in order to optimize the schedule for earliest timetable slots
    b_list = get_possible_shift_hours(input_file)

    for b in b_list:
        # Return the reading pointer to the beginning
        input_file.seek(0)
        
        p = Problem(input_file, b)

        p.result = csp.backtracking_search(p,
                                           select_unassigned_variable=csp.mrv,
                                           order_domain_values=csp.lcv,
                                           inference=csp.mac)

        # Try getting a solution
        if p.result == None:
            # Stop running the code when no solution is found for the current latest hour b
            break

        else:
            # Save a copy when a solution exists
            prev_p = p.copy()

    # Output the best working solution
    prev_p.dump_solution(output_file)

    # See how much time our code took to get the solution
    print(datetime.now() - startTime)

# Open the input and output files before entering in our functions, in order to be more similar to
# what the teacher's code does
input_file = open('examples/test_inventado.txt')
output_file = open('examples/test_inventado_output.txt', 'w')
solve(input_file, output_file)
output_file.close()