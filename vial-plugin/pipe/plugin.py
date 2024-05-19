import os
import pty
import fcntl
import time
import tty
import termios
from subprocess import PIPE, Popen

from vial import vim
from vial.compat import bstr
from vial.widgets import make_scratch
from vial.utils import focus_window


def unblock_fd(fd):
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def read_data(fd, timeout=60):
    data = []
    until = time.time() + timeout
    tm = True
    while True:
        if time.time() > until:
            if tm:
                data.append('TIMEOUT')
            break

        try:
            d = os.read(fd, 65536)
        except OSError as e:
            if e.errno == 11:
                time.sleep(0.1)
                continue
            else:
                raise

        if not d:
            break

        data.append(d)
        until = time.time() + 0.5
        tm = False

    return ''.join(data)


procs = {}
def tty_proc(command):
    try:
        return procs[command]
    except KeyError:
        pass

    m, s = pty.openpty()
    tty.setraw(s, termios.TCSANOW)

    p = Popen(command, shell=True, stdout=s, stderr=s, stdin=s)
    p.vial_master = m
    unblock_fd(m)
    procs[command] = p
    return p


def get_input(mode, buf):
    mode = int(mode)
    if mode == 0: # paragraph
        start = buf.mark('{')[0]
        stop = buf.mark('}')[0]
    elif mode == 1: # visual
        start = max(0, buf.mark('<')[0] - 1)
        stop = buf.mark('>')[0]
    else: # whole buffer
        start = 0
        stop = len(buf)

    return '\n'.join(buf[start:stop])


def execute(mode):
    cbuf = vim.current.buffer
    cwin = vim.current.window

    input = bstr(get_input(mode, cbuf), 'utf-8')  # TODO: use buffer encoding
    executable = cbuf[0].lstrip('#! ')

    with open('/tmp/vial-pipe-result.txt', 'wb') as f:
        Popen(executable, shell=True, stderr=f,
              stdout=f, stdin=PIPE).communicate(input)

    make_scratch('vial-pipe', title='Result')
    vim.command('norm! ggdG')
    vim.command('0read /tmp/vial-pipe-result.txt')
    focus_window(cwin)


def send_to(mode):
    cbuf = vim.current.buffer
    cwin = vim.current.window

    input = bstr(get_input(mode, cbuf), 'utf-8')  # TODO: use buffer encoding
    executable = cbuf[0].lstrip('#! ')

    proc = tty_proc(executable)
    for line in input.splitlines():
        os.write(proc.vial_master, line + '\n')

    _, sbuf = make_scratch('vial-pipe', title='Result')
    data = read_data(proc.vial_master)
    sbuf[:] = data.splitlines()
    focus_window(cwin)
