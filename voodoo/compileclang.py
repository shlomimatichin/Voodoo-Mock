import subprocess
import os
import shutil

shutil.rmtree( "/tmp/clang", ignore_errors = True )
os.mkdir( "/tmp/clang" )
os.chdir( "/tmp/clang" )
subprocess.check_call( "svn co http://llvm.org/svn/llvm-project/llvm/trunk@193808 llvm", shell = True )
checkoutClang = subprocess.Popen( "svn co http://llvm.org/svn/llvm-project/cfe/trunk@193803 clang", shell = True, cwd = "llvm/tools" )
subprocess.check_call( "svn co http://llvm.org/svn/llvm-project/compiler-rt/trunk@193807 compiler-rt", shell = True, cwd = "llvm/projects" )
result = checkoutClang.wait()
if result != 0:
    raise Exception( "checkout of clang failed" )
os.mkdir( "build" )
subprocess.check_call( "../llvm/configure --enable-optimized --disable-assertions --disable-keep-symbols", shell = True, cwd = "build" )
subprocess.check_call( "make -j 5", shell = True, cwd = "build" )
shutil.copy2( "build/Release/lib/libclang.so", "libclang.so" )
shutil.copytree( "llvm/tools/clang/bindings/python/clang", "clang" )
