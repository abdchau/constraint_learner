import time

class Timer:
    def __init__(self) -> None:
        self.start_time = None
        self.last_time = None
        self.out_string = ''
    
    def intialize_timer(self):
        self.start_time = time.time()
        self.last_time = self.start_time
        
    def measure(self, st):
        now = time.time() 
        time_since_last = now - self.last_time
        self.last_time = now
        if time_since_last < 0.0001:
            return

        self.out_string += '{:.2f}: {} \n'.format(time_since_last*1000, st)
        
    def output(self):
        print(self.out_string)
        
timer = Timer()