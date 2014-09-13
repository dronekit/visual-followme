class Pid:
    ref = 240    
    integral = 0.0
    previus_error = 0.0

    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
    def compute(self, output, reference):
        error = reference - output
        self.integral = self.integral + error    
        self.integral = max(min(10000, self.integral), 0)
        derivative = (error - self.previus_error)
        control = error * self.kp + self.integral * self.ki + derivative * self.kd
        self.previus_error = error
        return control
    
def print_graph(output,control):
    graph = '|' * int((output) / 2)
    print 'Y %d,\tpwm %d -' % (output, control) + graph