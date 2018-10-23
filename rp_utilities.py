def relock_squid(rp, array_max=0.05, delay=0.1):
    """ Attempts to detect if the SQUID is unlocked and relock if necessary. Windows only.
        Inputs:
            - rp: Red Pitaya object as defined by rp = p.rp, where p = Pyrpl('squid_lockbox')
            - array_max: threshold for the absolute value of array voltage to detect unlocking
            - delay: time delay in seconds between subsequent loops
    """
    import time
    import msvcrt
    def get_keypress():
        return ord(msvcrt.getch()) if msvcrt.kbhit() else 0

    msg0 = 'GUI disabled while relock loop is running.\n'
    msg1 = 'Current lock point: Mod V = {}, Array V = {}.\n'.format(rp.scope.voltage_in1, rp.scope.voltage_in2)
    msg2 = 'Will relock if |array voltage| > {} or if PID output saturates.\n'.format(array_max) 
    msg3 = 'Enter "q" to exit loop. '
    print(msg0 + msg1 + msg2 + msg3)
    while True:
        try:
            if get_keypress() == 113: # q
                raise KeyboardInterrupt
            if abs(rp.pid0.ival) > 3.98 or abs(rp.scope.voltage_in2 - rp.pid0.setpoint) > array_max:
                print('Relocking SQUID...')
                rp.pid0.ival = 0
                time.sleep(delay * 5)
                print('New lockpoint: Mod V = {}, Array V = {}.'.format(rp.scope.voltage_in1, rp.scope.voltage_in2))
                print(msg3)
                print('-----------------------------------------')
            time.sleep(delay)
        except KeyboardInterrupt:
            n = input('Exit relock loop? y/[n] ')
            if n.strip().lower() == 'y':
                print('Exiting relock loop, reenabling GUI...')
                break
            else:
                print('Relock loop still running.')
        finally: pass
