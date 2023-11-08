class Bandwidth:
    def __init__(self, current_bw, future_bw):
        self._current_bw = current_bw  
        self._future_bw = future_bw

    @property
    def current_bw(self):
        return self._current_bw

    @current_bw.setter
    def current_bw(self, value):
        self._current_bw = value
        
    @property
    def future_bw(self):
        return self._future_bw

    @future_bw.setter
    def future_bw(self, value):
        self._future_bw = value
        