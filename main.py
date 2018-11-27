import csp

class Problem(csp.CSP):

    def __init__(self, input_file):
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
                line = f.readline()

        f.close()

        # Get the domain T x R
        domains = self.combine_output(timetable, room, weekly_class)

        # Variables are W
        variables = weekly_class

        # The neighbors of each node are every other node (is this stupid?)
        self.create_neighbors_dict(weekly_class)

        # Run CSP's innit
        super().__init__(variables, domains, self.graph, self.constraint_function)

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
        with open(fh, 'w+') as f:
            for key in self.result.keys():
                count = count + 1

                line = str(key[0]) + ',' + str(key[1]) + ',' + str(key[2]) + ' ' + str(self.result[key][0]) + ',' + str(self.result[key][1]) + ' ' + str(self.result[key][2])

                if count != len(self.result.keys()):
                    line += '\n'
                    
                f.write(line)

        f.close()
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
        
def solve(input_file, output_file):
    p = Problem(input_file)
    # Place here your code that calls function csp.backtracking_search(self, ...)
    p.result = csp.backtracking_search(p)
    p.dump_solution(output_file)

solve('example1.txt', 'random_output.txt')