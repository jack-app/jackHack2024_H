class MilliSec(float):
    def toSec(self):
        return Sec(self / 1000)
    def toMilliSec(self):
        return self
class Sec(float):
    def toSec(self):
        return self
    def toMilliSec(self):
        return MilliSec(self * 1000)