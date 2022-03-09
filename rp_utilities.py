import time
import msvcrt
from qtpy import QtWidgets


def get_keypress():
    return ord(msvcrt.getch()) if msvcrt.kbhit() else 0


def relock_squid(rp, array_max=0.05, delay=1e-3, enable_gui=True):
    """Attempts to detect if the SQUID is unlocked and relock if necessary (Windows only).

    Args:
        rp: Red Pitaya object as defined by rp = p.rp, where p = Pyrpl('squid_lockbox').
        array_max (float): Threshold for the absolute value of array voltage to detect unlocking.
        delay (float): Time delay in seconds between subsequent loops.
        enable_gui (bool): If True, allow the GUI to continue running while the re-lock loop is running.
    """

    msg = [
        f"Current lock point: Mod V = {rp.scope.voltage_in1}, Array V = {rp.scope.voltage_in2}.",
        f"Will relock if |array voltage| > {array_max} or if PID output saturates.",
        f"Enter 'q' to exit loop.",
    ]
    print("\n".join(msg))

    gui = QtWidgets.QApplication.instance()

    while True:
        try:
            if get_keypress() == 113: # User pressed "q"
                raise KeyboardInterrupt
            if (
                abs(rp.pid0.ival) > 3.98 # Integrator has railed
                or abs(rp.scope.voltage_in2 - rp.pid0.setpoint) > array_max # Lock was lost
            ):
                print("Relocking SQUID...")
                rp.pid0.ival = 0
                time.sleep(delay * 10)
                print(f"New lockpoint: Mod V = {rp.scope.voltage_in1}, Array V = {rp.scope.voltage_in2}.")
                print(msg[-1])
                print("-" * 40)
            if enable_gui and gui is not None:
                gui.processEvents()
            time.sleep(delay)
        except KeyboardInterrupt:
            n = input("Exit relock loop? y/[n] ")
            if n.strip().lower() == "y":
                print("Exiting relock loop...")
                break
            else:
                print("Relock loop still running.")
