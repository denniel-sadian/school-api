from github_storages.backend import BackendStorages

import os


class TheStorage(BackendStorages):

    def get_valid_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        
        dir_name, file_name = os.path.split(super().get_valid_name(name))
        flength = len(file_name)
        
        if flength > 8:
            offset = flength - (flength % 40 + 8)
            file_name = file_name[offset:]
            name = os.path.join(dir_name, file_name)
        
        if self.exists(name): # filename exists, get dot index
            try:
                dot_index = file_name.rindex('.')
            except ValueError: # filename has no dot
                dot_index = -1

            inc = 0 # Set incrementer to zero
            while self.exists(name):
                inc += 1
                if dot_index == -1: # If no dot, append to end
                    tname = file_name + str(inc)
                else:
                    tname = file_name[:dot_index] + str(inc) + file_name[dot_index:]
                name = os.path.join(dir_name, tname)

        return name