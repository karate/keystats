import os
import pyxhook
import json
from signal import signal, SIGINT, SIGKILL, SIGTERM
from sys import exit
import sys

STATS = {}
# Number of keypresses, we use to write stats to file
# every 1000 keypresses just to be sure in case of a fatal error
keypresses = 0

# Initialization
def main():
	global STATS, log_file
	log_filename = 'keypress_freq.json'

	# Get log filename from command line
	if len(sys.argv) > 1:
		log_filename = sys.argv[1]
	log_file = os.path.expanduser(log_filename)

	# Create log file if not exist
	if not os.path.exists(log_file):
		with open(log_file, "w"):
			pass

	# Load STATS from file
	with open(log_file, 'r') as f:
		data = f.readline()
		if (data != ''):
			try:
				STATS = json.loads(data)
			except json.JSONDecodeError:
				print("File found but no valid JSON could be parsed.")
				exit(0)
	total_keypress = sum(STATS.values())
	print(f"{total_keypress:,}", "keypresses read.")
	
	kill_handlers()

	# create a hook manager object
	new_hook = pyxhook.HookManager()
	new_hook.KeyDown = OnKeyPress
	# set the hook
	new_hook.HookKeyboard()
	try:
		# Start the hook
		new_hook.start()
	except KeyboardInterrupt:
		# User cancelled from command line.
		pass
	except Exception as ex:
		# Write exceptions to the log file, for analysis later.
		print('Error while catching events:\n {}'.format(ex))
		pyxhook.print_err(msg)

def OnKeyPress(event):
	global keypresses
	k = event.Key.upper()
	if k in STATS:
		STATS[k] += 1
	else:
		STATS[k] = 1
	keypresses += 1
	# On every 1K keypresses, log to file
	if keypresses > 1000:
		keypresses = 0
		write_log()

# Write stats to file
def write_log():
	global log_file
	with open(log_file, 'w') as f:
		# Sort by keypress count, desc
		sorted_dic = dict(sorted(STATS.items(), key=lambda item: item[1], reverse=True))
		# Write to file
		f.write(json.dumps(sorted_dic))

# Implement the SIGINT/SIGTERM handler
def handler(signal_received, frame):
	print('SIGINT or CTRL-C detected. Writting to file before exiting')
	write_log()
	exit(0)

def kill_handlers():
	# Set handlers for KILL signals
	signal(SIGINT, handler)
	signal(SIGTERM, handler)

if __name__ == "__main__":
	main()
