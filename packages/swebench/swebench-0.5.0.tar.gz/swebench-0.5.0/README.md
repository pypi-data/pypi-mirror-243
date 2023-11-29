# SWE-bench PyPI Package

[Website](https://swebench.com) &bull; [GitHub](https://github.com/princeton-nlp/SWE-bench) &bull; [Paper](https://arxiv.org/abs/2310.06770)

Code repository that holds the latest version of the SWE-bench PyPI package.

To create/update the PyPI package, follow these steps:
1. Edit `create_src.py` such that `PATH_TO_SWE_BENCH` and `PATH_TO_PYPI` point to the correct SWE-bench and PyPI repositories on your local machine.
2. Run `create_src.py` to update `src/swebench` with the latest code from [princeton-nlp/SWE-bench](https://github.com/princeton-nlp/SWE-bench) and creates empty `__init__.py` files in each folder.
3. Update `__version__` + edit the `src/swebench/__init__.py` if you would like to expose functions from SWE-bench that were not available in the previous version.
4. Edit `import` statements as needed to resolve dependencies within SWE-bench (add `swebench.<file>.` prefix).
5. Run `./build_deploy.sh` to build the PyPI distribution and update PyPI with the latest package.