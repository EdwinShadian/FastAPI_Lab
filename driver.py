#!/usr/bin/python3.10

import sys
import fuse
from fuse import Fuse
import stat
import errno
import json
import requests

fuse.fuse_python_api = (0, 2)


class defaultStat(fuse.Stat):
	def __init__(self):
		self.st_mode = 0
		self.st_ino = 0
		self.st_dev = 0
		self.st_nlink = 0
		self.st_uid = 0
		self.st_gid = 0
		self.st_size = 0
		self.st_atime = 0
		self.st_mtime = 0
		self.st_ctime = 0


class simpleFuse(Fuse):
	def getentry(self, path):
		response = requests.get("http://127.0.0.1:8000/library" + path)
		if response.status_code != 404:
			entry = json.loads(response.content)
			return entry
		return None

	def getattr(self, path):
		if path in ['.', '..']:
			stats = defaultStat()
			stats.st_mode = stat.S_IFDIR | 0o755
			stats.st_nlink = 2
			return stats

		entry = self.getentry(path)
		if not entry:
			return errno.errorcode[errno.ENOENT]
		stats = defaultStat()
		if entry['mode'] == 'dir':
			stats.st_mode = stat.S_IFDIR | 0o755
			stats.st_nlink = 2
		else:
			stats.st_mode = stat.S_IFREG | 0o755
			stats.st_nlink = 1
			if 'data' not in entry:
				stats.st_size = 0
			else:
				stats.st_size = sys.getsizeof(entry['data'])
		return stats

	def open(self, path, flags):
		if not self.getentry(path):
			return errno.errorcode[errno.ENOENT]

	def read(self, path, size, offset):
		entry = self.getentry(path)
		if (not entry) or (entry['mode'] != 'reg'):
			return errno.errorcode[errno.ENOENT]
		if 'data' not in entry:
			data = ''
		else:
			data = entry['data']
		return data.encode('utf-8')

	def readdir(self, path, offset):
		entry = self.getentry(path)
		if (not entry) or ('items' not in entry):
			return errno.errorcode[errno.ENOENT]
		for d in entry['items'].keys():
			yield fuse.Direntry(d)


if __name__ == '__main__':
	driver = simpleFuse(
		version="%prog " + fuse.__version__,
		usage=Fuse.fusage, dash_s_do="setsingle"
	)
	driver.parse(errex=1)
	driver.main('')
