#!/usr/bin/env python3

import demo
import time
def progress( msg ):
    print( "PROGRESS:", msg )



( demo.startthread( "3", "3", 0,callback=progress) )
print(demo.get_threadstatus(0))

