.. SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
.. SPDX-License-Identifier: Apache-2.0

Troubleshooting
===============

.. py:currentmodule:: cuda.pathfinder

When ``cuda.pathfinder`` cannot locate a requested component, it raises an
error (for example :class:`DynamicLibNotFoundError`) whose message lists every
search step that was attempted and why it did not produce a match. This page
explains how to read that message and how to resolve the most common causes.

Reading the error message
-------------------------

A typical failure looks like this:

.. code-block:: text

   cuda.pathfinder.DynamicLibNotFoundError: Failure finding "libnvvm.so.*": ...

   Please see https://nvidia.github.io/cuda-python/cuda-pathfinder/latest/troubleshooting.html

The text between ``Failure finding "..."`` and the trailing URL is a
comma-separated list of the search steps that were tried, in order. Each entry
names the step (for example a ``site-packages`` scan, ``CONDA_PREFIX``, or
``CUDA_HOME/CUDA_PATH``) and why it failed, so the first thing to check is
which of the locations below you expected the library to be found in.

Where ``cuda.pathfinder`` searches
----------------------------------

For CUDA Toolkit (CTK) libraries, :func:`load_nvidia_dynamic_lib` searches in
this priority order:

1. **NVIDIA Python wheels**: installed distributions in ``site-packages``.
2. **Conda environments**: discovered via ``CONDA_PREFIX``, which is set
   automatically when a conda environment is activated.
3. **OS default mechanisms**: the native loader (``dlopen()`` on Linux,
   ``LoadLibraryExW()`` on Windows). On Linux, system CTK installs are usually
   discovered via ``/etc/ld.so.conf.d/*cuda*.conf``. On Windows, this native
   search does **not** include the system ``PATH``.
4. **Environment variables**: ``CUDA_PATH`` or ``CUDA_HOME`` (in that order).

Driver libraries (``"cuda"``, ``"nvml"``) ship with the NVIDIA display driver,
not the CTK, and are only searched via the OS default mechanisms.

Common causes and fixes
-----------------------

**The NVIDIA wheel is not installed in the current environment**
    If you rely on pip-installed CUDA components, confirm the wheel that ships
    the library (for example ``nvidia-cuda-nvcc``, ``nvidia-cudnn``) is
    installed in the *same* Python environment that runs your code:
    ``pip list | grep nvidia``.

**The conda environment is not activated**
    Step 2 depends on ``CONDA_PREFIX``, which is only defined in an activated
    environment. Activate the environment before starting Python, and confirm
    with ``echo $CONDA_PREFIX``.

**A system CTK install is not visible to the native loader**
    On Linux, check that ``/etc/ld.so.conf.d/`` contains the CUDA
    configuration and that ``ldconfig`` has been run after installation.

**``CUDA_PATH`` / ``CUDA_HOME`` is unset or points at the wrong root**
    Step 4 only runs if one of these variables is set, and it must point at
    the CTK installation root (the directory containing ``lib64``, ``bin``,
    etc.). On Windows, the CTK installer normally sets ``CUDA_PATH``
    system-wide; on Linux, a typical value is ``/usr/local/cuda``.

**A driver library cannot be found**
    ``"cuda"`` (libcuda) and ``"nvml"`` are part of the NVIDIA display driver.
    Installing the CTK is not sufficient; ensure the display driver itself is
    installed and healthy (``nvidia-smi`` should work).

Reporting an issue
------------------

If none of the above resolves the failure, please `open an issue
<https://github.com/NVIDIA/cuda-python/issues>`_ and include the complete
error message, your OS and Python version, and how CUDA components were
installed (pip wheels, conda, or a system CTK install).
