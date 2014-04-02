function VoodooParseSingleFile()
        let bufferName = bufname( "%" )
        execute "make generateSingleVoodoo SINGLE_HEADER=\"`python tools/vim/relpath.py " . bufferName . "`\""
endfunction

function VoodooHint()
        let bufferName = bufname( "%" )
        let line = line( "." )
        execute "%!python tools/voodoo/voodoohint.py --hintLine=" . line
        execute ":".line
endfunction

map <C-F3> <Esc>:call VoodooParseSingleFile()<CR>
map <C-F4> <Esc>:make generateVoodooForce<CR>
map <C-F6> <Esc>:call VoodooHint()<CR>
