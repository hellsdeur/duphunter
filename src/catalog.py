import os


class Catalog:
    def __init__(self, directory):
        self.directory = directory
        self.size = 0
        self.filepaths = self.fill_filepaths()

    def fill_filepaths(self):
        filepaths = []
        for direct, subdir, files in os.walk(self.directory):
            for file in files:
                filepaths.append(os.path.join(os.path.realpath(direct), file))
                self.size += 1
        return sorted(filepaths)

    def __iter__(self):
        self.x = 0
        return self

    def __next__(self):
        x = self.x
        if x >= self.size:
            raise StopIteration
        self.x = x + 1
        return self.filepaths[x]

    def __str__(self):
        return '\n'.join(sorted([filename for filename in self.filepaths]))