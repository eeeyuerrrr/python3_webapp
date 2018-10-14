'''
执行 python pymonitor.py app.py
完整路径 D:\prj_python\my_python3_webapp\venv\Scripts\python.exe D:/prj_python/my_python3_webapp/www/pymonitor.py D:\prj_python\my_python3_webapp\www\app.py
则当当前目录下的.py文件改变时，会重启app.py
'''


import os
import subprocess
import sys
import time

from watchdog.events import FileSystemEvent
from watchdog.observers import Observer

process = None
# command初始化占位，并无实际意义，后面会被赋值为启动app.py的命令
command = ['echo', 'ok']

def log(s):
    print('[Monitor] %s' % s)

class PyMonitorEventHandler(FileSystemEvent):

    def __init__(self, src_path, fn):
        super(PyMonitorEventHandler, self).__init__(src_path)
        self.action = fn

    def dispatch(self, event):
        if event.src_path.endswith('.py'):
            log('Python source file changed: %s' % event.src_path)
            self.action()

def kill_process():
    global process
    if process:
        log('Kill process [%s]...' % process.pid)
        process.kill()
        process.wait()
        log('Process ended with code: %s ' % process.returncode)
        process = None

def start_process():
    global process
    log('Start process %s...' % ' '.join(command))
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def restart_process():
    kill_process()
    start_process()

def start_watch(path, callback):
    observer = Observer()
    observer.schedule( PyMonitorEventHandler(path, restart_process), path, recursive=True)
    observer.start()
    log('Watchdog is starting. Watching directory %s...' % path)
    start_process()
    try:
        while True:
            time.sleep(0.8)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    log('Watchdog is finished.')

if __name__ == '__main__':
    # 执行 python pymonitor.py app.py
    # 则argv = [ 'pymonitor.py', 'app.py']
    argv = sys.argv[1:]
    if not argv:
        print('Lack of argv. Usage: python pymonitor.py your_script.py')
        exit(0)
    if argv[0] != 'python' or argv[0]!='python':
        argv.insert(0, 'python')

    command = argv
    curDirPath = os.path.abspath('.')
    start_watch(curDirPath, None)













