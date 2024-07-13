import time

class Timer:
    def __init__(self, time_limit, increment):
        self.time_limit = time_limit
        self.increment = increment
        self.time_used = 0
        self.start_time = 0
        self.on = False

    def start(self):
        self.start_time = time.time()
        self.on = True

    def stop(self):
        self.time_used += time.time() - self.start_time
        self.time_used -= self.increment
        self.on = False

    def get_time_left(self):
        if self.on:
            curr_move_time = time.time() - self.start_time
        else:
            curr_move_time = 0
        return self.time_limit - self.time_used - curr_move_time
    
    def get_time_string(self):
        time_left = self.get_time_left()
        minutes = int(time_left // 60)
        seconds = int(time_left % 60)
        tenths = int((time_left - int(time_left)) * 10)
        if time_left < 0:
            return "0:00"
        return f"{minutes}:{seconds:02}.{tenths}"
    
    def time_up(self):
        return self.get_time_left() <= 0

    

