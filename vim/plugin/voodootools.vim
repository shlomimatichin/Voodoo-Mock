function VoodooParseSingleFile()
        let bufferName = bufname( "%" )
        execute "make voodoo_compileSingleHeader V=1 SINGLE_HEADER=\"`python -c 'import os; import sys; print os.path.relpath( sys.argv[ 1 ], os.getcwd() )' " . bufferName . "`\""
endfunction

function VoodooHint()
        let line = line( "." )
        execute "%!python $VOODOO_ROOT_DIR/voodoo/voodoohint.py --db=build_unittest/voodooDB.tmp --hintLine=" . line
        execute ":".line
endfunction

map <C-F3> <Esc>:call VoodooParseSingleFile()<CR>
map <C-F4> <Esc>:make voodoo_forceGenerateAll<CR>
map <C-F6> <Esc>:call VoodooHint()<CR>
