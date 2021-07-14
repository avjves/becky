import os
import uuid
import random

def join_file_path(*args):
      """
      Preprocesses the given values and runs them through os.path.join.
      """
      args = list(args)
      if args[0] == '':
          args[0] = '/'
      for i in range(1, len(args)): # First value can start with /
          args[i] = args[i].strip('/')
      return os.path.join(*args)

def create_test_files(path, file_count):
    """
    Generates new random empty files/folders to the given path.
    File_count specifies how many files/folders will be generated
    in total.
    """
    prefix = str(uuid.uuid4()).split("-")[0]
    random_files = [prefix + "_" + str(i) for i in range(0, file_count)]
    if len(random_files) != len(set(random_files)): ## If collissions, try again
        create_test_files(path, file_count)
        return
    cur_f = path
    for random_file in random_files:
        is_dir = random.randint(0, 1)
        if is_dir:
            cur_f = os.path.join(cur_f, random_file + "_DIRECTORY")
            if not os.path.exists(cur_f):
                os.mkdir(cur_f)
        else:
            f = open(os.path.join(cur_f, random_file + "_FILE"), 'w')
            f.write(random_file)
            f.close()


def remove_prefix(string, prefix):
    """
    Removes a prefix from the string, if it exists.
    """
    if string.startswith(prefix):
        return string[len(prefix):]
    else:
        return string[:]


def path_to_folders(location):
    folders = []
    while location:
        folders.append(location)
        location = location.rsplit('/', 1)[0]
    return folders
