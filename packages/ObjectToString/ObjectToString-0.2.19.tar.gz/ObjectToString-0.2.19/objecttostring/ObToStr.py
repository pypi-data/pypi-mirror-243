import inspect
import ObjectToString

class ObjectToStr:

    def __init__(self):
        self.tt = ObjectToString.ObjectToString()

    def generalPy(self,filename,classname,dir):
        self.tt.generalPy(filename, classname, dir)
    def generalStr(self,ss):
        return self.tt.generalStr(ss)