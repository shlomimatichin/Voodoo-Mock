function RunSingleTest()
        let bufferName = bufname( "%" )
        let line = line( "." )
        execute "make test_singletest SINGLE_TEST_SUITE=\"`python -c 'import os; import sys; print os.path.relpath( sys.argv[ 1 ], os.getcwd() )' " . bufferName . "`\" SINGLE_TEST_LINE=" . line
endfunction

function RunSingleTestSuite()
        let bufferName = bufname( "%" )
        execute "make test_singletestsuite SINGLE_TEST_SUITE=\"`python -c 'import os; import sys; print os.path.relpath( sys.argv[ 1 ], os.getcwd() )' " . bufferName . "`\""
endfunction

map <F2> <Esc>:w<CR>`T:w<CR>:call RunSingleTest()<CR>
map <F3> <Esc>:w<CR>`T:w<CR>:call RunSingleTestSuite()<CR>
map <F4> <Esc>:w<CR>:make -j<CR>
