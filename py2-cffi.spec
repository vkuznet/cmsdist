### RPM external py2-cffi 1.11.5
## IMPORT build-with-pip
Requires: py2-pycparser libffi
%define PipBuildOptions --global-option=build_ext --global-option="-L${LIBFFI_ROOT}/lib64" --global-option="-I${LIBFFI_ROOT}/include"
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*

