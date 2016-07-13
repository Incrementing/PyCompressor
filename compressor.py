'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import os
import sys
import gzip
import time
import platform

class Utils:
    
    @classmethod
    def get_current_user(cls):
        import getpass
        try:
            return getpass.getuser()
        except KeyError: # Stop "cannot find name for user ID XXXX" error.
            return str(os.getuid()) # Just return the user ID because name can't be found.

    @classmethod
    def get_size_in_kb(cls, path):
        bytes = os.stat(path).st_size
        return float(bytes) / 1000

    @classmethod
    def clear_terminal(cls):
        if (platform.system() == "Windows"):
            os.system("cls")
        else:
            os.system("clear")

    @classmethod
    def request_input(cls, string):
         if (sys.version_info >= (3, 0)):
             return input(string)
         else:
             return raw_input(string)

    @classmethod
    def request_path(cls):
        path = False
        while (not path):
            x = cls.request_input("Please enter the path to the file you wish to compress.\n> ")
            if (os.path.exists(x)):
                if (os.path.isfile(x)):
                    cls.clear_terminal()
                    print("\"" + x + "\" was selected!")
                    time.sleep(2)
                    path = x
                else:
                    print("\"" + x + "\" is a path but doesn't point to a file!")
                    time.sleep(2)
                    cls.clear_terminal()
            else:
                print("\"" + x + "\" isn't a path!")
                time.sleep(2)
                cls.clear_terminal()
        return path

class Worker:

    def __init__(self, path):
        self.path = path

    def run(self):
        Utils.clear_terminal()
        self.path = self.path.replace("\\", "/")
        file_name = self.path.split("/")[len(self.path.split("/")) - 1]

        print("Starting compression of " + file_name + "...\n")
        try:
            with open(self.path, "rb") as to_compress:
                with gzip.open(self.path + ".gz", "wb") as compressed:
                    compressed.writelines(to_compress)
            print("Compression of " + file_name + " was successful!")
            print("Base directory: " + self.path.replace(file_name, ""))
            print("Origin file: " + file_name + " ("+str(Utils.get_size_in_kb(self.path))+" KB)")
            print("Compressed file: " + file_name + ".gz" + " ("+str(Utils.get_size_in_kb(self.path + ".gz"))+" KB)")
        except IOError:
            print("Compression of " + file_name + " FAILED!")
            print("IOError: failed to read from origin file (has python got permission?) OR Failed to write to compressed file (has python got permission? / is the disk full?).")
        x = Utils.request_input("\nPress RETURN to restart PyCompresser!")
        start()


def start():
    Utils.clear_terminal()
    print("Welcome " + Utils.get_current_user() + " to the PyCompresser!")
    worker = Worker(Utils.request_path())
    worker.run();

if (__name__) == '__main__':
    start()
