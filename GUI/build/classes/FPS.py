class FPS:
    def __init__(self, rate):
        self._rate = rate  
      
    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = value