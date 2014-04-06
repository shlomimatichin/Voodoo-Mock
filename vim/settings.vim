set tabstop=4
set shiftwidth=4
set autoindent
set incsearch
set expandtab
filetype on
filetype plugin on
filetype indent on
au FileType cpp setl tabstop=8
au FileType cpp setl shiftwidth=8
au FileType cpp setl noexpandtab
au FileType c setl tabstop=8
au FileType c setl shiftwidth=8
au FileType c setl noexpandtab

set runtimepath+=$VOODOO_ROOT_DIR/vim
set hlsearch
set encoding=utf-8

command Ctags !ctags --exclude=build --exclude=build_unittest --exclude=tools -R .
command NewFile %!python $VOODOO_ROOT_DIR/vim/newfile.py %
command Coverage !python $VOODOO_ROOT_DIR/vim/coverage.py %
command -range Colin :<line1>,<line2>!python $VOODOO_ROOT_DIR/vim/columindent/configuredmain.py % indent
command -range ColinDeclaration :<line1>,<line2>!python $VOODOO_ROOT_DIR/vim/columindent/configuredmain.py % indentCPPDeclaration
command -range ConstructorReferenceArguments :<line1>,<line2>!python $VOODOO_ROOT_DIR/vim/columindent/configuredmain.py % constructorReferenceArguments
command -range DirtyTrace :<line1>,<line2>!python $VOODOO_ROOT_DIR/vim/dirtytrace.py %

map <F6> :Colin<CR>
"Fast movement in the location list:
map <C-j> :cn<CR>
map <C-k> :cp<CR>

"Fast movement in the buffer list:
map <C-h> :bp<CR>
map <C-l> :bn<CR>
map <M-Right> :bn
map <M-Left> :bp

"Fast movement for next/previous tags
map #8 :tp
map #9 :tn

"Fast movement between splits
map <M-Down> 
map <M-Up> W

if has("gui_running")
	colorscheme darkblue
	set guifont=Monospace\ 18
endif
command TinyFont :set guifont=Monospace\ 12
command SmallFont :set guifont=Monospace\ 14
command LargeFont :set guifont=Monospace\ 18

"source $VIM/_vimrc

function! s:PathComplete(ArgLead, CmdLine, CursorPos)
	return genutils#UserFileComplete(a:ArgLead, a:CmdLine, a:CursorPos, 1, &path)
endfunction
command! -nargs=1 -bang -complete=custom,<SID>PathComplete FindInPath
          \ :find<bang> <args>

"Remove trailing spaces and replace tabs with spaces on save
autocmd BufWritePre *.py :%s/\s\+$//e
autocmd BufWritePre *.py :retab

set listchars=eol:$,tab:>-,trail:~,extends:>,precedes:<
map <Leader>wi :set list<CR>
map <Leader>wo :set nolist<CR>
