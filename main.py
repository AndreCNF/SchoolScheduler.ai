import csp

class Problem(csp.CSP):

    def __init__(self, input_file):
        # Place here your code to load problem from opened file object fh and
        # set variables, domains, graph, and constraint_function accordingly
        #super().__init__(variables, domains, graph, constraints_function)

        timetable = []
        weekly_class = []
        associations = []
        room = []
        student_class = []
        
        with open(input_file) as f:

            # Read initial line
            line = f.readline()

            # If the file is not empty keep reading one line at a time, till the file is empty
            while line:
                
                # Split line in pieces delimited by whitespace
                line = line.split()

                # For these 3 first cases go over one line, split each piece and store as tuple
                if line[0] == 'T':
                    for i in range(len(line)-1):
                        temp = tuple(line[i+1].split(",")) # Split again to make tuples
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
                line = f.readline()

        f.close()

        # Get the domain T x R
        domains = combine_output(timetable, room)

        # Variables are W
        variables = timetable

    # C1 to C3 -> returns true if constraint is verified, false if not
    # C1: Each room can only hold 1 class at a time
    def check_C1(self, A, a, B, b):
        if a[0] == b[0] and a[1] == b[1] and a[2] == b[2]:
            return False
        return True
        
    # C2: Each student (class) can only attend a class at a time
    def check_C2(self, A, a, B, b):
        for key in dict1:
            if dict2[key] == True:
                if a[0] == b[0] and a[1] == b[1]:
                    return False
        return True

    # C3: No two weekly class of the same course may occur on the same day 
    def check_C3(self, A, a, B, b):
        if a[0] == b[0] and A[0] == B[0] and A[1] == B[1]:
            return False
        return True

    # def dump_solution(self, fh):
    #     # Place here your code to write solution to opened file object fh

# Make the output domain by getting all possible combinations of timetables (T) with rooms (R)
def combine_output(T, R):
    output = []

    for t in T:
        for r in R:
            output_tuple = (t[0], t[1], r)
            output.append(output_tuple)

    return output
        
def solve(input_file, output_file):
    p = Problem(input_file)
    # Place here your code that calls function csp.backtracking_search(self, ...)
    p.dump_solution(output_file)

solve('example1.txt', 'random_output.txt')