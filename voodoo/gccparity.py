#tools to make clang compile gcc code
import os
import subprocess
import re

emulateGCCInClangPreinclude = os.path.join( os.path.dirname( __file__ ), "emulate_gcc_in_clang_preinclude.h" )

_cachedGCCIncludePath = None
def gccIncludePath():
    global _cachedGCCIncludePath
    if _cachedGCCIncludePath is None:
        with open( os.devnull, "r" ) as noInput:
            output = subprocess.check_output( [ "g++", "-E", "-x", "c++", "-", "-v" ], stderr = subprocess.STDOUT, stdin = noInput )
            _cachedGCCIncludePath = list()
            for filename in re.findall( r"\r?\n (\S+)", output ):
                if os.path.isdir(filename):
                    _cachedGCCIncludePath.append(os.path.normpath(filename).replace("\\","/"))
    return _cachedGCCIncludePath
