#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vim
import re
import os
import os.path
from functools import wraps
from .utils import *
from .explorer import *
from .manager import *
from .mru import *


#*****************************************************
# RgExplorer
#*****************************************************
class RgExplorer(Explorer):
    def __init__(self):
        self._executor = []

    def getContent(self, *args, **kwargs):
        if os.name == 'nt':
            cwd = '.'
        else:
            cwd = ''
        executor = AsyncExecutor()
        self._executor.append(executor)
        cmd = '''rg --no-heading --with-filename --color never --line-number --smart-case "int" %s''' % cwd
        content = executor.execute(cmd)
        # content = executor.execute(cmd, encoding=lfEval("&encoding"))
        return content

    def getStlCategory(self):
        return 'Rg'

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))

    def supportsNameOnly(self):
        return False

    def cleanup(self):
        for exe in self._executor:
            exe.killProcess()
        self._executor = []


#*****************************************************
# RgExplManager
#*****************************************************
class RgExplManager(Manager):
    def __init__(self):
        super(RgExplManager, self).__init__()
        self._match_ids = []

    def _getExplClass(self):
        return RgExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Rg#Maps()")

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        line = args[0]
        file, line_num = line.split(':', 2)[:2]
        if file.startswith('+'):
            file = os.path.abspath(file)
        try:
            lfCmd("hide edit +%s %s" % (line_num, escSpecial(file)))
        except vim.error as e:
            lfPrintError(e)

    def _getDigest(self, line, mode):
        """
        specify what part in the line to be processed and highlighted
        Args:
            mode: 0, return the full path
                  1, return the name only
                  2, return the directory name
        """
        return line

    def _getDigestStartPos(self, line, mode):
        """
        return the start position of the digest returned by _getDigest()
        Args:
            mode: 0, return the start postion of full path
                  1, return the start postion of name only
                  2, return the start postion of directory name
        """
        return 0

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : open file under cursor')
        help.append('" x : open file under cursor in a horizontally split window')
        help.append('" v : open file under cursor in a vertically split window')
        help.append('" t : open file under cursor in a new tabpage')
        help.append('" d : wipe out buffer under cursor')
        help.append('" D : delete buffer under cursor')
        help.append('" i/<Tab> : switch to input mode')
        help.append('" q/<Esc> : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help

    def _afterEnter(self):
        super(RgExplManager, self)._afterEnter()
        id = int(lfEval("matchadd('Lf_hl_rgFileName', '^[^:]*\ze:')"))
        self._match_ids.append(id)
        id = int(lfEval("matchadd('Lf_hl_rgLineNumber', '^[^:]*:\zs\d\+')"))
        self._match_ids.append(id)

    def _beforeExit(self):
        super(RgExplManager, self)._beforeExit()
        for i in self._match_ids:
            lfCmd("silent! call matchdelete(%d)" % i)
        self._match_ids = []


#*****************************************************
# rgExplManager is a singleton
#*****************************************************
rgExplManager = RgExplManager()

__all__ = ['rgExplManager']
