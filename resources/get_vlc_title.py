from win32gui import GetWindowText, IsWindowEnabled, EnumWindows
from win32process import GetWindowThreadProcessId
from psutil import process_iter
from root import vlc_hwnd_log, setClipboardData, printList
from os import path
from tag import getTagList


def get_hwnds_for_pid (pid):
	def callback (hwnd, hwnds):

		if (IsWindowEnabled(hwnd)):
			_, found_pid = GetWindowThreadProcessId(hwnd)

			if found_pid == pid:
				hwnds.append (hwnd)

		return True

	hwnds = []
	EnumWindows(callback, hwnds)

	return hwnds


def get_vlc_hwnd():
	"""
	Check if vlc_hwnd stored in vlc_hwnd_log file is still for vlc
	if it is then use it
	otherwise try to find vlc hwnd
		finding hwnd requires process ID
		find PID by iterating through all active processes searching for vlc
	"""

	vlc_hwnd = -1

	f = open(vlc_hwnd_log, 'r')
	vlc_num_from_file = f.read()
	f.close()

	if (vlc_num_from_file.isdigit() and
			"media player" in GetWindowText(int(vlc_num_from_file))):
		vlc_hwnd = int(vlc_num_from_file)

	else:
		vlc_PID = -1

		for proc in process_iter():
			if proc.name() == "vlc.exe":
				vlc_PID = proc.pid
				break

		hwnd_list = get_hwnds_for_pid(vlc_PID)

		for hwnd in hwnd_list:
			if "VLC media player" in GetWindowText(hwnd):
				vlc_hwnd = hwnd
				f = open(vlc_hwnd_log, "w+")
				f.write(str(hwnd))
				f.close()

	return vlc_hwnd


def get_VLC_title(vlc_hwnd):

	vlcTitle = title_from_hwnd(vlc_hwnd)
	return vlcTitle


def path_from_hwnd(vlc_hwnd):

	# VLC Tools -> Preferences -> Show "All" Settings ->
	# Input/Codecs -> Change title according to current media =$F
	# Displays file path to current media in VLC window text

	window_title = GetWindowText(vlc_hwnd)

	translation_dict = {
		" - VLC media player": "",
		"file:///": "",
		"%20": " ",
		"%28": "(",
		"%29": ")",
		"%5B": "[",
		"%5D": "]",
		"%27": "'"
	}

	for key in translation_dict.keys():
		window_title = window_title.replace(key, translation_dict[key])
	file_path = path.normpath(window_title)

	return file_path


def title_from_hwnd(vlc_hwnd):

	file_path = path_from_hwnd(vlc_hwnd)
	title = path.split(file_path)[1]
	return title


def main():

	vlc_hwnd = get_vlc_hwnd()
	vlcTitle = get_VLC_title(vlc_hwnd)
	fp = path_from_hwnd(vlc_hwnd)
	quoted_fp  = "\"" + fp + "\""

	print "+ Currently playing:"
	printList([vlcTitle], aes="none")
	setClipboardData(quoted_fp)
	printList([quoted_fp], aes="none")
	print getTagList(fp)


if __name__ == "__main__":
	main()