import vial

def init():
    vial.vim.command('nnoremap <silent> <Plug>VialPipeExecute :{}<cr>'
                     .format(vial.python('.plugin.execute', 0)))
    vial.vim.command('vnoremap <silent> <Plug>VialPipeExecute :{}<cr>'
                     .format(vial.python('.plugin.execute', 1)))
    vial.vim.command('nnoremap <silent> <Plug>VialPipeExecuteAll :{}<cr>'
                     .format(vial.python('.plugin.execute', 3)))
