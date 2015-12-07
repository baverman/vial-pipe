import vial

def init():
    vial.vim.command("nnoremap <Plug>VialPipeOne :{}<cr>"
                     .format(vial.python('.plugin.execute_one')))
