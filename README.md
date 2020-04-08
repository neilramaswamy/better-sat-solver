# README

Lots of files, I know. However, I've modularized my code to ensure that each file and function is readable and cleanly testable.
Here's a broad overview of what each file does:

- `classes` contains the stencil classes `Literal` and `Clause`
- `pure_elimination` and `unit_elimination` provide the functions for the types of elimination they nominally describe
- `util` has functions that are shared across the codebase. One example is removing all literals from a formula.
- `tester` goes through every file in the `tests/` directory and makes sure that UNSAT instances are UNSAT and SAT instances have a verifiably correct solution
- `sat_io` is mostly stencil code. It pertains to reading from the filesystem and writing to stdout
- `solver` is the driver
- `run.sh` runs `solver` with the argument it is provided

The usage of the `test` directory is explained in `tester.py`. In most cases, running a file directly will run the tests inside of it.
