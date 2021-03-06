import sys

if sys.hexversion < 0x03010000:
    raise EnvironmentError("Python >= 3.1 required by {}".format(__name__))

import serial
# import io
import time


class StrangerBoard(object):
    """
    StrangerBoard(port="/dev/usbserial4111", [baud=9600, ...])

    Port is required, other items are pySerial control arguments, it's _strongly recommended_ that you
    only set 'baud=' parameter and leave others alone.

    :param port: (str) the name of a serial device to connect to. Default is /dev/ttyUSB0
    :param baud: (int) the baud rate. Default is 9600
    :param parity: (char) the parity of N, E, or O. default is N for None
    :param stop: (int) the number of stop bits. defalutl is 1
    :param timeout: (int) seconds to wait before timing out a read. Default is 85!
    """

    def __init__(self, port=None, **kwargs):
        if port is None:
            port = "/dev/ttyUSB0"
        self.port = port
        self._settings = kwargs.copy()
        self._connection = None
        self.queue = []

    def begin(self):
        """
        Begins serial communication; must call before any read/write

        Only Odd, Even, and None parities are supported; others will revert to None

        :return: the serial connection object. You should generally ignore that.
        """
        if 'baud' not in self._settings:
            self._settings['baud'] = 9600
        if 'parity' not in self._settings:
            self._settings['parity'] = 'N'
        if 'stop' not in self._settings:
            self._settings['stop'] = 1
        if 'timeout' not in self._settings:
            self._settings['timeout'] = 5

        parity = serial.PARITY_NONE
        if self._settings['parity'].upper() == 'E':
            parity = serial.PARITY_EVEN
        elif self._settings['parity'].upper() == 'O':
            parity = serial.PARITY_ODD

        self._connection = serial.Serial(
            port=self.port,
            baudrate=self._settings['baud'],
            parity=parity,
            stopbits=self._settings['stop'],
            timeout=self._settings['timeout'])

    def get_config(self):
        config = self._settings.copy()
        config['port'] = self.port
        return config

    def _write(self, message=""):
        """
        Peforms an immediate write to the serial port. Should not be used by consumers
        :return:
        """
        if self._connection is None:
            raise RuntimeError("No connection established, call .begin() first")

        if not self._connection.is_open:
            self._connection.open()

        ascii_message = message.strip().encode(encoding="ascii", errors="ignore")
        self._connection.write(ascii_message)
        self._connection.write(b"\n")

    def _read(self, timeout=85):
        """
        Performs an immediate readline from the serial port. Should not be used by consumers


        :param timeout: (int) seconds to wait for a newline to arrive. Default is 85
        :return: line read as bytes
        """
        if self._connection is None:
            raise RuntimeError("No connection established, call .begin() first")

        if not self._connection.is_open:
            self._connection.open()

        # sio = io.TextIOWrapper(io.BufferedRWPair(self._connection, self._connection))
        # message = sio.readline()
        start = time.time()
        message = ""
        while not message.endswith("\n"):
            message += self._connection.read().decode()
            if time.time() - start > timeout:
                raise TimeoutError("Waited too long for newline, only got '{}'".format(message))

        return message

    def write(self, message, timeout=90):
        """
        Performs a write of a message, then waits for a "Queued message" response from StrangerBoard

        Uses the timeout value to determine how long to wait

        :param message:
        :param timeout:
        :return: queued message string, exception on failure
        """
        self._write(message)
        start = time.time()
        response = self._read()
        while not response.startswith("Queued message '"):
            print("Still waiting, heard: {}".format(response.strip()), file=sys.stderr)
            if time.time() - start > timeout:
                raise TimeoutError("Timeout waiting for Queued notification")
            response = self._read()

        print(response, file=sys.stderr)

        return response
