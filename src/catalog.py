import os


class Catalog:
    def __init__(self, directory):
        self.directory = directory
        self.filepaths = self.get_filepaths()

    def get_filepaths(self):
        filepaths = []
        for direct, subdir, files in os.walk(self.directory):
            for file in files:
                self.filepaths.append(os.path.join(os.path.realpath(direct), file))
        return sorted(filepaths)

    def __str__(self):
        return '\n'.join(sorted([filename for filename in self.filepaths]))
