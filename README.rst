Vial Pipe
=========

Simple tool to pipe a text into various cli tools. (psql, mysql, and so on)

First line in a buffer defines a command to execute (can contain a shebang).

Mappings
--------

``<Plug>VialPipeExecute`` pipes current paragraph (a content between { and } marks)
or visual selection

``<Plug>VialPipeExecuteAll`` pipes whole buffer.

For example::

    au FileType sql nmap <buffer> <leader><cr> <Plug>VialPipeExecute
    au FileType sql vmap <buffer> <leader><cr> <Plug>VialPipeExecute

will map ``<leader><cr>`` to execute an expression under the cursor
(or selected expression) in sql buffers.

And::

    au FileType python nmap <buffer> <leader><cr> <Plug>VialPipeExecuteAll

will map ``<leader><cr>`` to execute python script.
