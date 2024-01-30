"""
Written by Deniz Bölöni-Turgut in June 2023 (REUSE Student)

Python script which applies ADV string obfuscation to every C file in a cloned GitHub repository
"""
import argparse
import os
import re
import subprocess
import random

from pathlib import Path
from typing import Dict, List
 
def get_args():
    parser = argparse.ArgumentParser()

     # absolute path to the root folder of the repository
    parser.add_argument("--repo-path", type=str)
    
    # absolute path to the root folder of the repository directory
    parser.add_argument("--header-lib-path", type=str, default="/Lib")
    
    return parser.parse_args()

def copy_header_files(args):
    """
    Copies Lib directory from ADV_Obfuscator (with all of its header files)
    param: path: Path to the repository where you want to copy the headers
    """
    subprocess.run(["cp", "-r", f"{args.header_lib_path}", f"{args.repo_path}"])

def find_c_files(path: str):
    """
    Find all C files in the directory specified by parameter path
    param: path: Path to the repository directory you want to search
    return: a list of absolute paths to every C file in the directory
    """
    c_files = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if (f.endswith(".c")):
                c_files.append(os.path.join(root, f))
    return c_files    

def find_makefiles(path: str):
    """
    Find all makefiles in the directory specified by parameter path
    param: path: Path to the repository directory you want to search
    return: a list of absolute paths to all the Makefiles in target repo
    """
    makefiles = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if (f == "Makefile"):
                abs_path = os.path.join(root, f)
                makefiles.append(abs_path)
    return makefiles   

def find_makefile_dirs(path: str):
    """
    Find all makefiles in the directory specified by parameter path
    param: path: Path to the repository directory you want to search
    return: a list of absolute paths to all directories which contain makefile
    """
    makefiles = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if (f == "Makefile"):
                abs_path = os.path.join(root, f)
                abs_path = abs_path[:-9] # cut off /Makefile
                makefiles.append(abs_path)
    return makefiles   

def _obfuscate_strings(c_files):
    """
    Add OBFUSCATE macro around all String in C file
    param: c_files: list of paths to every C file in the repo
    """
    # treat the c file as text, search through it
    for c_file in c_files:
        with open(c_file, "r") as f:
            code = f.readlines()
            for i in range(len(code)):
                all_strings = re.findall(r'"(.*?(?<!\\))"', code[i])
                # choose a regex from the long stack overflow post (i think the one i'm currently using works with escape \")
                for string in all_strings:
                   # don't obfuscate header strings
                   if string.endswith(".h"):
                       continue
                   code[i] = code[i].replace(f"\"{string}\"", f"OBFUSCATED(\"{string}\")")
        
        with open(c_file, "w") as f:
            f.writelines(code)

        f.close()

def obfuscate_strings(c_files):
    for c_file in c_files:
        subprocess.run(f"sed '/#include/!s/\".*\"/OBFUSCATED(&)/g' < {c_file} > temp.c", shell=True, cwd="/")
        subprocess.run(["mv", "-f", "temp.c", c_file], cwd="/")

def _include_headers(c_files, args):
    for c_file in c_files:
        with open(c_file, "r") as f:
            content = f.read()
            f.close()
        with open(c_file, "w") as f:
            # add headers
            f.write(f"#ifndef HEADERFILE\n")
            f.write(f"#define HEADERFILE\n")
            for root, dirs, files in os.walk(f"/Lib"):
                for header in files:
                    f.write(f"#include \"/{args.header_lib_path}/{header}\"\n")
            f.write(f"#endif\n")
            f.write(content) # append the rest of the file

def include_headers(c_files, args):
    for c_file in c_files:
        subprocess.run(f"cat headers.c {c_file} > temporary_cat.c", cwd="/", shell=True)
        subprocess.run(["mv", "-f", "temporary_cat.c", c_file], cwd="/")

def associate_c_files_with_submodules(repo_path_str: str) -> Dict[Path, List[Path]]:
    """
    Returns dictionary with keys as path to .git and values as list of C files to be committed and added relative to that .git folder
    Written by Luke Dramko, June 2023
    """
    repo_path = Path(repo_path_str)
    assert (repo_path / ".git").exists(), f"Root directory {repo_path_str} must be a git repository."
    
    cfile2gitmodule: Dict[Path, List[Path]] = {}
    def search_tree(dir_to_search: Path, current_git_module: Path):
        if (dir_to_search / ".git").exists():
            assert dir_to_search not in cfile2gitmodule
            cfile2gitmodule[dir_to_search] = []
            current_git_module = dir_to_search
        for dir_entry in os.scandir(dir_to_search):
            dir_entry = Path(dir_entry)
            if dir_entry.suffix == ".c" or dir_entry.suffix == ".h":
                assert not dir_entry.is_dir()
                cfile2gitmodule[current_git_module].append(dir_entry)
            #print(dir_entry.name)
            if dir_entry.is_dir() and dir_entry.name != ".git":
                search_tree(dir_entry, current_git_module)
    
    search_tree(repo_path, repo_path)
    return cfile2gitmodule

def _git_add_commit(args):
    """
    my attempt does not work!!!
    """
    dict = {}
    cur_git = None
    for root, dirs, files in os.walk(args.repo_path):
        print(f"root {root}")
        print(f"dirs {dirs}")
        print(f"files {files}")

        if ".git" in dirs:
            git_path = os.path.join(root, "/.git")
            print(f"git path {git_path}")
            if git_path not in dict:
                dict[git_path] = []
            cur_git = git_path
        dict[cur_git] += find_c_files_dir(root)
    print(dict)
    return dict

def find_c_files_dir(path):
    """
    Returns list of all C files inside this directory (not in any sub directories)
    """
    c_files = []
    filelist = os.listdir(path)
    for f in filelist:
        if f.endswith(".c"):
            c_files.append(f)
    return c_files

def main():
    args = get_args()
    random.seed(42) # initialize random seed for random optimizations

    #1) store paths to c files
    c_files = find_c_files(args.repo_path)

    #2) add OBFUSCATION macro around each of the strings (do before include headers because don't want to obfuscate those)
    # have to be careful because there could be stuff like "\" (tentatively works)
    obfuscate_strings(c_files)

    #3) add #include all the header files to the top of every C file
    #subprocess.run(["ls"], cwd="/")
    include_headers(c_files, args)
    
    #4) commit changes to c files (while accounting for submodules)
    result = associate_c_files_with_submodules(args.repo_path)
    for key, value in result.items():
        subprocess.run(["git", "add"]+value, cwd=key)
        subprocess.run(["git", "commit", "-m", "applied ADV obfuscator from adv_string_obfuscation.py"], cwd=key)
    
    # git commit code without accounting for submodules
    # subprocess.run(["git", "add"] + c_files, cwd="/repos")
    # subprocess.run(["git", "commit", "-m", "applied ADV obfuscator from adv_string_obfuscation.py"], cwd="/repos")
    
    #5) compiling [as of 06/26, using GHCC's built in compiler system]
    # opt = "-O"+str(random.randint(1, 3)) # needs to have some optimization in order to obfuscate
    # cflags_pattern = re.compile("CFLAGS = ?[./a-zA-Z0-9]+")
    # for i in range(len(makefiles)):
    #     cflags = "-g -std=c++11 -fpermissive "+opt
    #     with open(makefiles[i], "r") as f:
    #         content = f.read()
    #         temp = cflags_pattern.findall(content)
    #         print(f"temp {temp}")
    #         for flag in temp:
    #             cflags += " "+flag
    #     print(cflags)
    #     #["chmod +x configure && ./configure"]
    #     subprocess.run(["make", "--ignore-errors", "CC=g++", "cc=g++", "GCC=g++", "GXX=g++", f"CFLAGS+={cflags}"], cwd=makefile_dirs[i])
        #subprocess.run(["make", "CC=g++", "cc=g++", "GCC=g++", "GXX=g++", "CFLAGS+=-std=c++11", "CFLAGS+=-fpermissive", "CFLAGS+=-g", f"CFLAGS+={opt}", f"CFLAGS+=--keep-going"], cwd=makefile_dirs[i]) # another thing
    # change the src/bin/gcc inside the Docker container (find and change CC symlink)

if __name__ == "__main__":
    main()