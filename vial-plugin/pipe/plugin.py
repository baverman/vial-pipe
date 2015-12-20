from subprocess import PIPE, Popen

from vial import vim
from vial.widgets import make_scratch
from vial.utils import focus_window


def execute(visual):
    cbuf = vim.current.buffer
    cwin = vim.current.window
    if visual:
        start = max(0, cbuf.mark('<')[0] - 1)
        stop = cbuf.mark('>')[0]
    else:
        start = cbuf.mark('{')[0]
        stop = cbuf.mark('}')[0]

    input = '\n'.join(cbuf[start:stop])
    executable = cbuf[0]
    with open('/tmp/vial-pipe-result.txt', 'wb') as f:
        Popen(executable, shell=True, stderr=f,
              stdout=f, stdin=PIPE).communicate(input)

    make_scratch('vial-pipe', title='Result')
    vim.command('norm! ggdG')
    vim.command('0read /tmp/vial-pipe-result.txt')
    focus_window(cwin)
