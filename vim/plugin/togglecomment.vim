function ToggleComment()
        let bufferName = bufname( "%" )
        if bufferName =~ "[.]h$" || bufferName =~ "[.]cpp$" || bufferName =~ "[.]c$" || bufferName =~ "[.]js$" || bufferName =~ "[.]html$"
                let commentSign = "//"
                let uncommentAction = "0xx"
        else
                let commentSign = "#"
                let uncommentAction = "0x"
        endif
        let line = getline( "." )
        if line[ 0 ] == commentSign || line[ 0 : 1 ] == commentSign
                execute "normal " . uncommentAction
        else
                execute "normal " . "0i" . commentSign
        endif
endfunction

map co :call ToggleComment() <CR>
