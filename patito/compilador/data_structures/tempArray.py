#
# José Ángel Rentería Campos // A00832436
#

class TempArray:
    def __init__(self):
        self.temporaries = []
        self.counter = 0
        self.recycled_temporaries = []

    def next(self):
        if self.recycled_temporaries:
            return self.recycled_temporaries.pop()
        else:
            temp = f't{self.counter}'
            self.counter += 1
            return temp

    def return_temporary(self, temp):
        self.temporaries.append(temp)
