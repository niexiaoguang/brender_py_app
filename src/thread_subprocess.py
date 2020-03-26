import time
import sys, threading, os

bg_processes = []

def test():
    print('thread test')

class threadCom:  # object passed to threads to read background process stdout info
    ''' Object to pass data between thread and '''

    def __init__(self, process_type, proc, name=''):
        # self.obname=ob.name
        self.name = name
        self.process_type = process_type
        self.outtext = ''
        self.proc = proc
        self.lasttext = ''
        self.message = ''  # the message to be sent.
        self.progress = 0.0
        self.error = False
        self.log = ''

thread_freq = 3
def threadread(tcom):
    '''reads stdout of background process, done this way to have it non-blocking. this threads basically waits for a stdout line to come in, fills the data, dies.'''
    found = False
    while not found:
        # inline = tcom.proc.stdout.readline()
        time.sleep(thread_freq)
        print('readthread', time.time())
        # inline = str(inline)
        # tcom.outtext = inline
        # if 'buploading' in tcom.outtext:
        #     tcom.progress = inline

        # if 'bsuccessed' in tcom.outtext or 'bfailed' in tcom.outtext:
        #     tcom.lasttext = tcom.outtext
        #     found = True

def add_bg_proce(name=None, process_type='',
                   process=None):
    '''adds process for monitoring'''
    global bg_processes
    tcom = threadCom(process_type, process, name)
    readthread = threading.Thread(target=threadread, args=([tcom]), daemon=True)
    readthread.start()

    bg_processes.append([readthread, tcom])
    # if not bpy.app.timers.is_registered(bg_update):
    #     bpy.app.timers.register(bg_update, persistent=True)



# readthread = threading.Thread(target=threadread, args=([None]), daemon=False)
# readthread.start()
