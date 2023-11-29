from array import array as _array
from collections import deque as _deque
import libusb_package as _libusb
from queue import Queue
from threading import Lock as _Lock
from typing import Optional as _Optional, Union as _Union, Iterable as _Iterable
import usb.core as _usb_core
import usb.backend.libusb1 as _usb_back


_backend = _usb_back.get_backend(find_library=_libusb.find_library)


_vid = 0x483
_pid = 0x5750


class _Deque:
	def __init__(self, maxsize: int = 1024):
		self.__deque = _deque(maxlen=maxsize)
		self.__lock = _Lock()

	def put(self, data: _array):
		with self.__lock:
			self.__deque.extend(data)

	def room(self) -> int:
		"""
		返回目前剩余的可用空间。
		"""
		return self.__deque.maxlen - len(self.__deque)

	def get(self, size: int):



class _Resource:


class _ResourceManager:
	@staticmethod
	def find_device(serial_number: str = '') -> _usb_core.Device:
		paras = dict(
			idVendor=_vid, idProduct=_pid,
			manufacturer='Kersci', product='HIDSerial',
			backend=_backend
		)
		if serial_number:
			paras['serial_number'] = serial_number
		else:
			paras['find_all'] = True
		dev = _usb_core.find(**paras)

		return dev

	def __init__(self):
		self.__devices = dict()
		self.__queues_in = dict()
		self.__queues_out = dict()

	def _get_resource(self, serial_number: str, index: int, queue_dd: dict):
		device = self.__devices.get(serial_number, None)
		if device is None:
			return None

		queue_d: dict = queue_dd.get(serial_number)
		queue = queue_d.get(index, None)
		if queue is None:
			return None

		return device, queue

	def get_in(self, serial_number: str, index: int):
		return self._get_resource(serial_number, index, self.__queues_in)

	def get_out(self, serial_number: str, index: int):
		return self._get_resource(serial_number, index, self.__queues_out)

	def iterate_in(self):
		for serial_number, device in self.__devices:
			in_queue = self.__queues_in[serial_number]
			yield device, in_queue

	def iterate_out(self):
		for serial_number, device in self.__devices:
			out_queue = self.__queues_out[serial_number]
			yield device, out_queue

	def resource_already_exist(self, serial_number: str, index: int) -> bool:
		return serial_number in self.__devices and index in self.__queues_in[serial_number]

	def open_resource(self, serial_number: str, index: int):
		device = self.__devices.get(serial_number, None)
		if device:
			assert index not in self.__queues_in[serial_number], 'Resource busy'
		else:
			device = _ResourceManager.find_device(serial_number)
			assert device, f'Device with Serial Number "{serial_number}" does not exist.'
			self.__devices[serial_number] = device
			self.__queues_in[serial_number] = dict()
			self.__queues_out[serial_number] = dict()

		in_queue = Queue()
		out_queue = Queue()
		self.__queues_in[serial_number][index] = in_queue
		self.__queues_out[serial_number][index] = out_queue

	def close_resource(self, serial_number: str, index: int):
		assert serial_number in self.__devices and index in self.__queues_in[serial_number], "Resource is not opened."


def list_serial_numbers():
	dev_all = _ResourceManager.find_device()
	serial_numbers = []
	for dev in dev_all:
		serial_numbers.append(dev.serial_number)
	return serial_numbers


class Serial:
	def __init__(self, port: str, baudrate: int, timeout: float = 0):
		dev_type, serial_nb_raw, name = port.split('::')
		assert dev_type.lower() == 'uhserial', f'Device type "{dev_type}" not supported.'
		assert name[0] in 'Ss', f'Device name must be "Sxxx" format, where "xxx" are decimal digit(s).'
		try:
			index = int(name[1:])
		except IndexError:
			raise ValueError(f'Device name must be "Sxxx" format, where "xxx" are decimal digit(s).')
		except ValueError:
			raise ValueError(f'Device name must be "Sxxx" format, where "xxx" are decimal digit(s).')
		assert 0 < index < 8, f'Device index "{name}" out of range.'

		serial_nb: str = serial_nb_raw.lower()
		if serial_nb == 'any':
			serial_nb = ''
		dev = _find_device(serial_nb)
		if not dev:
			if serial_nb:
				raise ValueError(f'UHSerial with serial number "{serial_nb_raw}" not found.')
			else:
				raise ValueError('No UHSerial device found.')


if __name__ == '__main__':
	serials = list_serial_numbers()
	output = ', '.join(serials)
	print(output)
