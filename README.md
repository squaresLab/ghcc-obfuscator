# GitHub Cloner, Obfuscator & Compiler

This project is adapted from [huzecong/ghcc](https://github.com/huzecong/ghcc). In particular, this project does not use a MongoDB database to organize dataset output; the binary files are stored at directory specified by command line argument `--binary-folder`.

It clones, obfuscates, and compiles a list of GitHub repositories to create a dataset of obfuscated C/C++ binaries. Each repository is compiled once without any obfuscation, and 4 additional times with various obfuscations; the resulting binaries from compilation are classified by obfuscation type.

Two open source obfuscation tools are used in this project.
1. [ADVobfuscator](https://github.com/andrivet/ADVobfuscator), a source-to-source obfuscator used for string obfuscation.
2. [Obfuscator-LLVM](https://github.com/obfuscator-llvm/obfuscator/wiki/Installation), a compile-time obfuscator with three obfuscation flags. Each flag is used once individually, and once in combination (all three) for a total of 4 compilations.

From [huzecong/ghcc](https://github.com/huzecong/ghcc): This project serves as the data collection process for training neural decompilers, such as [CMUSTRUDEL/DIRE](https://github.com/CMUSTRUDEL/DIRE). The code for compilation is adapted from [bvasiles/decompilationRenaming](https://github.com/bvasiles/decompilationRenaming). The code for decompilation is adapted from [CMUSTRUDEL/DIRE](https://github.com/CMUSTRUDEL/DIRE). 


## Setup

1. Install [Docker](https://docs.docker.com/install/).
2. Install required Python packages by:
   ```bash
   pip install -r requirements.txt
   ```
3. CD to adv-obfuscation directory. Git clone [ADVobfuscator](https://github.com/andrivet/ADVobfuscator) (the latest compatible commit hash is 1852a0e).
4. Build the Docker image used to apply ADV obfuscation by running:
    ```bash
    docker build -t adv-obfuscation .
    ```
5.  CD to root directory. Git clone [Obfuscator-LLVM](https://github.com/obfuscator-llvm/obfuscator/wiki/Installation); run only the first line of commands on the wiki page. There should now be a folder at the path "/ghcc-master/obfuscator". The latest version of Obfuscator-LLVM which is supported is llvm4.0 (latest at the time).
6. CD to root directory. Build the Docker image used for the cloning and compiling repositories. The estimated time for this Docker image to build from scratch (i.e. with ``--no-cache``) is 2 hours.
   ```bash
   docker build -t gcc-custom .
   ```

## Usage

### Running the Compiler

You will need a list of GitHub repository URLs to run the code. The current code expects one URL per line, for example:
```
https://github.com/huzecong/ghcc.git
https://www.github.com/torvalds/linux
FFmpeg/FFmpeg
https://api.github.com/repos/pytorch/pytorch
```

To run, simply execute:
```bash
python main.py --repo-list-file path/to/your/list [arguments...]
```

The following arguments are supported:

- `--repo-list-file [path]`: Path to the list of repository URLs.
- `--clone-folder [path]`: The temporary directory to store cloned repository files. Defaults to `repos/`.
- `--binary-folder [path]`: The directory to store compiled binaries. Defaults to `binaries/`.
- `--archive-folder [path]`: The directory to store archived repository files. Defaults to `archives/`.
- `--n-procs [int]`: Number of worker processes to spawn. Defaults to 0 (single-process execution).
- `--log-file [path]`: Path to the log file. Defaults to `log.txt`.
- `--clone-timeout [int]`: Maximum cloning time (seconds) for one repository. Defaults to 600 (10 minutes).
- `--force-reclone`: If specified, all repositories are cloned regardless of whether it has been processed before or
  whether an archived version exists.
- `--compile-timeout [int]`: Maximum compilation time (seconds) for all Makefiles under a repository. Defaults to 900
  (15 minutes).
- `--force-recompile`: If specified, all repositories are compiled regardless of whether is has been processed before.
- `--docker-batch-compile`: Batch compile all Makefiles in one repository using one Docker invocation. This is on by
  default, and you almost always want this. Use the `--no-docker-batch-compile` flag to disable it. 
- `--compression-type [str]`: Format of the repository archive, available options are `gzip` (faster) and `xz`
  (smaller). Defaults to `gzip`.
- `--max-archive-size [int]`: Maximum size (bytes) of repositories to archive. Repositories with greater sizes will not
  be archived. Defaults to 104,857,600 (100MB).
- `--record-libraries [path]`: If specified, a list of libraries used during failed compilations will be written to the
  specified path. See [Collecting and Installing Libraries](#collecting-and-installing-libraries) for details.
- `--logging-level [str]`: The logging level. Defaults to `info`.
- `--max-repos [int]`: If specified, only the first `max_repos` repositories from the list will be processed.
- `--recursive-clone`: If specified, submodules in the repository will also be cloned if exists. This is on by default.
  Use the `--no-recursive-clone` flag to disable it.
- `--record-metainfo`: If specified, additional statistics will be recorded.
- `--gcc-override-flags`: If specified, these are passed as compiler flags to GCC. By default `-O1` is used.
- `--compiler`: Used to indicate compiler which needs to be used for each obfuscation tool. Do not override default (gcc).

### Utilities

- If compilation is interrupted, there may be leftovers that cannot be removed due to privilege issues. Purge them by:
  ```bash
  ./purge_folder.py /path/to/clone/folder
  ``` 
  This is because intermediate files are created under different permissions, and we need root privileges (sneakily
  obtained via Docker) to purge those files. This is also performed at the beginning of the `main.py` script.
- If the code is modified, remember to rebuild the image since the `batch_make.py` script (executed inside Docker to
  compile Makefiles) depends on the library code. If you don't do so, well, GHCC will remind you and refuse to proceed.

### Running the Decompiler

Decompilation requires an active installation of IDA with the Hex-Rays plugin. To run, simply execute:
```bash
python run_decompiler.py --ida path/to/idat64 [arguments...]
```

The following arguments are supported:

- `--ida [path]`: Path to the `idat64` executable found under the IDA installation folder.
- `--binaries-dir [path]`: The directory where binaries are stored, i.e. the same value for `--binary-folder` in the
  compilation arguments. Defaults to `binaries/`.
- `--output-dir [path]`: The directory to store decompiled code. Defaults to `decompile_output/`. 
- `--log-file [path]`: Path to the log file. Defaults to `decompile-log.txt`.
- `--timeout [int]`: Maximum decompilation time (seconds) for one binary. Defaults to 30.
- `--n-procs [int]`: Number of worker processes to spawn. Defaults to 0 (single-process execution). 


## Other
For information on compilation heuristics, docker safety, and installing additional libraries for use in compilation, see [huzecong/ghcc](https://github.com/huzecong/ghcc).