from subprocess import PIPE, Popen

from vial import vim
from vial.widgets import make_scratch
from vial.utils import focus_window


def execute(mode):
    cbuf = vim.current.buffer
    cwin = vim.current.window
    if mode == 0: # paragraph
        start = cbuf.mark('{')[0]
        stop = cbuf.mark('}')[0]
    elif mode == 1: # visual
        start = max(0, cbuf.mark('<')[0] - 1)
        stop = cbuf.mark('>')[0]
    else: # whole buffer
        start = 0
        stop = len(cbuf)

    input = '\n'.join(cbuf[start:stop])
    executable = cbuf[0].lstrip('#! ')
    with open('/tmp/vial-pipe-result.txt', 'wb') as f:
        Popen(executable, shell=True, stderr=f,
              stdout=f, stdin=PIPE).communicate(input)

    make_scratch('vial-pipe', title='Result')
    vim.command('norm! ggdG')
    vim.command('0read /tmp/vial-pipe-result.txt')
    focus_window(cwin)
