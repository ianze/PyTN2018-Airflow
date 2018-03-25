import random


class RandomFailOpen:
    def __init__ (self, file_name):
        # simulate a random fail such as DB connection
        fail = random.randint(1, 6)
        if fail > 3:
            raise Exception("Not opening file. Decided to Fail!")

        self.f = open(file_name)

    def __enter__ (self):
        return self.f

    def __exit__ (self, exc_type, exc_value, traceback):
        self.f.close()