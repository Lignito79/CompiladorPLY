#
# José Ángel Rentería Campos // A00832436
#

class JumpStack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from an empty stack")

    def top(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("top from an empty stack")

    def size(self):
        return len(self.items)