import wmi
from root import killProcess
from time import sleep
SW_SHOWNORMAL = 1

c = wmi.WMI()
process_startup = c.Win32_ProcessStartup.new()
process_startup.ShowWindow = SW_SHOWNORMAL
#
# could also be done:
# process_startup = c.Win32_ProcessStartup.new(ShowWindow=win32con.SW_SHOWNORMAL)

process_id, result = c.Win32_Process.Create(
  CommandLine="C:\\Users\\Kevin\\Util\\resources\\testDir\\refreshVols.bat",
  ProcessStartupInformation=process_startup
)
if result == 0:
  print "Process started successfully: %d" % process_id
  sleep(1)
  killProcess(pid=process_id)
else:
  raise RuntimeError, "Problem creating process: %d" % result