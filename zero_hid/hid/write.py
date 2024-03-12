import dataclasses
import logging
import multiprocessing
import typing
import queue
import threading

logger = logging.getLogger(__name__)

class Error(Exception):
    pass

class WriteError(Error):
    pass

@dataclasses.dataclass
class WriteOperation:
    hid_dev: typing.Any
    buffer: typing.Any

class WriteWorker(threading.Thread):
    def __init__(self, write_queue):
        super().__init__(daemon=True)
        self.write_queue = write_queue

    def run(self):
        while True:
            operation = self.write_queue.get()
            if operation is None:
                break
            self._write_to_hid_interface_immediately(operation.hid_dev, operation.buffer)

    def _write_to_hid_interface_immediately(self, hid_dev, buffer):
        try:
            hid_dev.seek(0)
            hid_dev.write(bytearray(buffer))
            hid_dev.flush()
        except BlockingIOError:
            logger.error(
                f'Failed to write to HID interface: {hid_dev}. Is USB cable connected and Gadget module installed? check https://git.io/J1T7Q'
            )

write_queue = queue.Queue()
write_worker = WriteWorker(write_queue)
write_worker.start()

def write_to_hid_interface(hid_dev, buffer):
    if logger.getEffectiveLevel() == logging.DEBUG:
        logger.debug('writing to HID interface %s: %s', hid_dev,
                     ' '.join(['0x%02x' % x for x in buffer]))
    write_queue.put(WriteOperation(hid_dev, buffer))