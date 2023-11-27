from serial import Serial as _Serial
from threading import Thread as _Thread, Event as _Event
from time import sleep as _sleep
from typing import Optional as _Optional


class DT1309(_Serial):
	def __init__(self, port: str):
		_Serial.__init__(self, port=port, baudrate=9600, timeout=0.5)
		self.__value: float = -1
		self.interval = 0.2

		self.__ready_event = _Event()
		self.__stop_flag = False
		self.last_frame = ''

		self.__checking_thread: _Optional[_Thread] = None
		self.start()

	def start(self):
		assert self.__checking_thread is None, 'Device has started.'
		self.__stop_flag = False
		self.__checking_thread = _Thread(target=self.__checker)
		self.__checking_thread.start()

	def stop(self):
		if self.__checking_thread is not None:
			self.__stop_flag = True
			self.__checking_thread.join()
			self.__checking_thread = None

	def close(self):
		self.stop()
		super(DT1309, self).close()

	def open(self):
		super(DT1309, self).open()
		self.start()

	def __checker(self):
		while not self.__stop_flag:
			self.flushInput()
			self.write(b'\x00\x00')
			char = self.read()
			timeout = False
			while char != b'\xCE':
				if char == b'':
					timeout = True
					break
				else:
					char = self.read()
			if timeout:
				continue
			data = self.read(4)
			hex_items = [hex(c)[2:].upper().zfill(2) for c in data]
			hex_str = ' '.join(hex_items)
			self.last_frame = f'CE {hex_str}'
			if len(data) != 4 or data[0] not in [0, 1, 2] or data[1] not in [0x80, 0x88]:
				continue
			high = int(hex(data[2])[2:])
			low = int(hex(data[3])[2:])
			value = high * 100 + low
			for i in range(data[0]):
				value = value / 10
			if data[1] == 0x88:
				value = value * 1000

			self.__value = value
			self.__ready_event.set()

			_sleep(self.interval)

	@property
	def lux(self) -> _Optional[float]:
		assert self.__checking_thread is not None and not self.__stop_flag, 'Device must be started first.'
		self.__ready_event.clear()
		if not self.__ready_event.wait(timeout=3):
			return None
		return self.__value
