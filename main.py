import csp

class Problem(csp.CSP):

    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh and
        # set variables, domains, graph, and constraint_function accordingly
        #super().__init__(variables, domains, graph, constraints_function)

        self.timetable = []
        self.weekly_class = []
        self.associations = []
        self.room = []
        self.student_class = []
        
        # Read initial line
        line = fh.readline()

        # If the file is not empty keep reading one line at a time, till the file is empty
        while line:
            
            # Split line in pieces delimited by whitespace
            line = line.split()

            # For these 3 first cases go over one line, split each piece and store as tuple
            if line[0] == 'T':
                for i in range(length(line)-1):
                    temp = tuple(line[i+1].split(",")) # Split again to make tuples
                    self.timetable.append(temp)

            elif line [0] == 'W':
                for i in range(length(line)-1):
                    temp = tuple(line[i+1].split(","))
                    self.weekly_class.append(temp)

            elif line [0] ==  'A'
                for i in range(length(line)-1):
                    temp = tuple(line[i+1].split(","))
                    self.associations.append(temp)

            # room is array of strings
            elif line [0] == 'R'
                for i in range(length(line)-1):
                    self.room.append(line[i+1])

            # student_class is array of strings
            elif line [0] == 'S'
                for i in range(length(line)-1):
                    self.student_class.append(line[i+1])

            # use realine() to read next line
            line = f.readline()

    # C1: Each room can only hold 1 class at a time
    def check_C1(self,)
        

    # C2: Each student (class) can only attend a class at a time
    def check_C2(self,)


    # C3: No two weekly class of the same course may occur on the same day 
    def check_C3(self,)

        
    def dump_solution(self, fh):
        # Place here your code to write solution to opened file object fh
        
def solve(input_file, output_file):
    p = Problem(input_file)
    # Place here your code that calls function csp.backtracking_search(self, ...)
    p.dump_solution(output_file)