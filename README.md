# vial-pipe
Simple tool to pipe text into various cli tools. (psql, mysql, and so on)

First line in buffer defines command to execute.

## Bindings

`<plug>VialPipeOne` pipes current paragraph (content between { and } marks)

For example:

    au FileType sql nmap <leader><cr> <Plug>VialPipeOne

will map `<leader><cr>` to execute expression under cursor in sql buffers.
