#
# José Ángel Rentería Campos // A00832436
#

class QuadStack:
    def __init__(self):
        self.quads = []

    def is_empty(self):
        return len(self.quads) == 0

    def push(self, quad):
        self.quads.append(quad)

    def pop(self):
        if not self.is_empty():
            return self.quads.pop()
        else:
            raise IndexError("pop from an empty list")

    def top(self):
        if not self.is_empty():
            return self.quads[-1]
        else:
            raise IndexError("top from an empty list")

    def size(self):
        return len(self.quads)

    def fill(self, index, target):
        if 0 <= index < len(self.quads):
            self.quads[index][3] = target
        else:
            raise IndexError("quad index out of range")
        
    def print(self):
        for quad in self.quads:
            print(quad[0], quad[1], quad[2], quad[3])

    def writeOBJ(self):
        f = open("obj.txt", "a")
        for quad in self.quads:
            f.write(str(quad[0]) + " " + str(quad[1]) + " " + str(quad[2]) + " " + str(quad[3]) + "\n")
        f.close()