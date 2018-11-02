" ============================================================================
" File:        Rg.vim
" Description:
" Author:      Yggdroot <archofortune@gmail.com>
" Website:     https://github.com/Yggdroot
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

if leaderf#versionCheck() == 0  " this check is necessary
    finish
endif

exec g:Lf_py "from leaderf.rgExpl import *"

function! leaderf#Rg#Maps()
    nmapclear <buffer>
    nnoremap <buffer> <silent> <CR>          :exec g:Lf_py "rgExplManager.accept()"<CR>
    nnoremap <buffer> <silent> o             :exec g:Lf_py "rgExplManager.accept()"<CR>
    nnoremap <buffer> <silent> <2-LeftMouse> :exec g:Lf_py "rgExplManager.accept()"<CR>
    nnoremap <buffer> <silent> x             :exec g:Lf_py "rgExplManager.accept('h')"<CR>
    nnoremap <buffer> <silent> v             :exec g:Lf_py "rgExplManager.accept('v')"<CR>
    nnoremap <buffer> <silent> t             :exec g:Lf_py "rgExplManager.accept('t')"<CR>
    nnoremap <buffer> <silent> q             :exec g:Lf_py "rgExplManager.quit()"<CR>
    " nnoremap <buffer> <silent> <Esc>         :exec g:Lf_py "rgExplManager.quit()"<CR>
    nnoremap <buffer> <silent> i             :exec g:Lf_py "rgExplManager.input()"<CR>
    nnoremap <buffer> <silent> <Tab>         :exec g:Lf_py "rgExplManager.input()"<CR>
    nnoremap <buffer> <silent> <F1>          :exec g:Lf_py "rgExplManager.toggleHelp()"<CR>
    if has_key(g:Lf_NormalMap, "Rg")
        for i in g:Lf_NormalMap["Rg"]
            exec 'nnoremap <buffer> <silent> '.i[0].' '.i[1]
        endfor
    endif
endfunction

function! leaderf#Rg#startExpl(win_pos, ...)
    if a:0 == 0
        call leaderf#LfPy("rgExplManager.startExplorer('".a:win_pos."')")
    else
        call leaderf#LfPy("rgExplManager.startExplorer('".a:win_pos."', arguments={'--all': []})")
    endif
endfunction

function! leaderf#Rg#startExplPattern(win_pos, all, pattern)
    if a:all == 0
        call leaderf#LfPy("rgExplManager.startExplorer('".a:win_pos."', pattern='".a:pattern."')")
    else
        call leaderf#LfPy("rgExplManager.startExplorer('".a:win_pos."', arguments={'--all': []}, pattern='".a:pattern."')")
    endif
endfunction
