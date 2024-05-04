class MilliSec(int):
    def toSec(self):
        return Sec(self // 1000)
    def toMilliSec(self):
        return self
class Sec(int):
    def toSec(self):
        return self
    def toMilliSec(self):
        return MilliSec(self * 1000)