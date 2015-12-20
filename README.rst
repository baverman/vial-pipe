Vial Pipe
=========

Simple tool to pipe a text into various cli tools. (psql, mysql, and so on)

First line in a buffer defines a command to execute.

Commands
--------

``:VialPipeExecute`` pipes current paragraph (a content between { and } marks)

For example::

    au FileType sql noremap <buffer> <silent> <leader><cr> :VialPipeExecute<cr>

will map ``<leader><cr>`` to execute an expression under the cursor in sql buffers.
