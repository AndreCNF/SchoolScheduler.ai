import csp

class Problem(csp.CSP):

    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh and
        # set variables, domains, graph, and constraint_function accordingly
        #super().__init__(variables, domains, graph, constraints_function)

        self.timetable = {}
        self.room = {}
        self.student_class = {}
        self.weekly_class = {}
        self.associations = {}

        line = fh.readline()
        # use the read line to read further.
        # If the file is not empty keep reading one line
        # at a time, till the file is empty
        while line:
            
            # Split line in pieces delimited by ruaitespace
            line = line.split()
            if line[0] == 'T'
                self.timetables.update(line)
            elif line [0] == 'W'
                self.weekly_class.update(line)
            elif line [0] == 'R'
                self.room.update(line)
            elif line [0] == 'S'
                self.student_class.update(line)
            elif line [0] ==  'A'
                self.associations.update(line)
            # use realine() to read next line
            line = f.readline()

        self.variables
        self.domains
        self.graph
        self.constraints_function
        
    def dump_solution(self, fh):
        # Place here your code to write solution to opened file object fh
        
def solve(input_file, output_file):
    p = Problem(input_file)
    # Place here your code that calls function csp.backtracking_search(self, ...)
    p.dump_solution(output_file)