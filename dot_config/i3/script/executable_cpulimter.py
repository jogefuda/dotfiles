#!/bin/python3

import subprocess
from i3ipc import Connection, Event

limit_cpu_tag = 'limit_cpu_*'
limited = {}
limit_at = 5 # percent
def get_pid_by_resourceid(id):
    proc = subprocess.Popen(['xprop', '-id', str(id)], stdout=subprocess.PIPE)
    for i in proc.stdout:
        if b'_NET_WM_PID' in i:
            return int(i.rstrip().split(b'=')[1])
    return None

def cpulimit(client, percent):
    pid = get_pid_by_resourceid(client.window)
    if pid == None:
        return

    if percent == 0:
        if limited[pid] != None:
            limited[pid].terminate()
            limited[pid].wait()
            del(limited[pid])
    else:
        proc = subprocess.Popen('cpulimit -p {} -l {}'.format(pid, percent), shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        limited[pid] = proc

def on_workspace_focus(i3, e):
    for client in e.old.find_marked(limit_cpu_tag):
        cpulimit(client, limit_at)
    for client in e.current.find_marked(limit_cpu_tag):
        cpulimit(client, 0)

def main():
    i3 = Connection()
    i3.on(Event.WORKSPACE_FOCUS, on_workspace_focus)
    i3.main()

if __name__ == '__main__':
    main()
