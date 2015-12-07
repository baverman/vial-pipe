from subprocess import PIPE, Popen

from vial import vim
from vial.helpers import echom
from vial.widgets import make_scratch
from vial.utils import focus_window


def execute_one():
    cbuf = vim.current.buffer
    cwin = vim.current.window
    start = cbuf.mark('{')[0]
    stop = cbuf.mark('}')[0]

    input = '\n'.join(cbuf[start:stop])
    executable = cbuf[0]
    with open('/tmp/vial-pipe-result.txt', 'wb') as f:
        stdout, stderr = Popen(executable, shell=True,
                               stderr=PIPE, stdout=f, stdin=PIPE).communicate(input)

        if stderr:
            for line in stderr.splitlines():
                echom(line)

    make_scratch('vial-pipe', title='Result')
    vim.command('norm! ggdG')
    vim.command('0read /tmp/vial-pipe-result.txt')
    focus_window(cwin)
