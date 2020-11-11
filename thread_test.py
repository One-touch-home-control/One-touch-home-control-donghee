import threading

def printit():
    threading.Timer(5.0, printit).start()
    print("Hello, World!")
    
def printit2():
    threading.Timer(3.0, printit2).start()
    print("Hello, World222!")
    
printit()
printit2()