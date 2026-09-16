#!/usr/bin/python3
import os
import sys
import vlc
import time
import readchar

inputs = ['\'1\'', '\'2\'', '\'3\'', '\'4\'', '\'5\'', '\'6\'', '\'7\'', '\'8\'', '\'9\'', '\'0\'']
special = ['\'*\'', '\'+\'', '\'-\'', '\'+\'', '\'/\'', '\'.\'']

instance = vlc.Instance('--input-repeat=0')
player = instance.media_player_new()

parent_dir = os.path.dirname(os.path.abspath(__file__))


def loadPresets():
	"Get all the Presets in the directory of the main script "
	l = []
	for file in os.listdir(parent_dir):
		if file.endswith(".preset"):
			print("Preset Found:", os.path.join(parent_dir, file))
			l.append(os.path.join(parent_dir, file))
	return l


def getPresetTracks(preset):
	''' Get all the links inside of a preset track '''
	l = []
	with open(preset) as file:
		for line in file:
			 # Need to get rid of those pesky \n's
			print(str(len(l)) + ': ', line[:-1])
			l.append(line[:-1])
	if len(l) < 10:
		print("Too little links. Cannot correctly populate.")
		l = []
	elif len(l) > 10:
		print("Too many links. Cannot correctly populate.")
		l = []

	complete_path = [os.path.join(parent_dir, track) for track in l]
	return complete_path


# def isYouTubeAudio(link):
# 	import re
# 	if re.match(r'http[s]:\/\/www\.youtube\.com/watch\?v=([\w-]{11})', link) == None:
# 		return False
# 	else:
# 		return True
	

# def getYouTubeAudioTrack(link):
# 	''' Get Audio track of a link '''
# 	import pafy

# 	video = pafy.new(link)
# 	bestaudio = video.getbestaudio()

# 	# print(bestaudio.url)
# 	return bestaudio.url


# def playQuick(num):
# 	''' Make quick sound '''
# 	l = ['up.mp3', 'down.mp3', 'preset_change.mp3', 'startup.mp3']
# 	s = instance.media_new(os.path.join(os.getcwd(), l[num]))
# 	player.set_media(s)
# 	player.play()
# 	if num == 3:
# 		time.sleep(4)
# 	else:
# 		time.sleep(1)
# 	player.stop()


def switchPresets(readyPresets):
	#playQuick(2)
	
	print("Ready to swap the preset. Loaded presets:")
	i = 0
	for link in readyPresets:
		print(i, "-", link)
		i += 1

	print("Select a new preset:")
	newPreset = repr(readchar.readkey())
	
	if newPreset.isdigit() and int(newPreset) < len(presetList):
		# Number preset. We're goood
		numPre = int(newPreset)
		print("New Preset: ", numPre)
		#playQuick(0)
		return numPre
	else:
		# It's a character. Stop
		print("Invalid preset. Skipping.")
		#playQuick(1)
		return None
		

def playTrack(track):
	''' Play an audio track once and stop.'''
	from readchar import readkey

	# Load and add media file
	media = instance.media_new(track)
	player.set_media(media)

	# Play
	player.play()

	# Pause before getting the status, to update everything
	print(str(player.get_state()) + "          ", end='\r')
	sys.stdout.flush()
	time.sleep(1)
	
	print(str(player.get_state()) + "          ")


if __name__ == '__main__':
	print("Starting...")
	print(r'''
 _____                       _______                     _ 
/  ___|                     | | ___ \                   | |
\ `--.  ___  _   _ _ __   __| | |_/ / ___   __ _ _ __ __| |
 `--. \/ _ \| | | | '_ \ / _` | ___ \/ _ \ / _` | '__/ _` |
/\__/ / (_) | |_| | | | | (_| | |_/ / (_) | (_| | | | (_| |
\____/ \___/ \__,_|_| |_|\__,_\____/ \___/ \__,_|_|  \__,_|
                                                           
                                                           ''')

	presetList = loadPresets()
	print("Choosing initial preset...")
	initialPreset = readchar.readkey()
	print("Initial preset selected:", initialPreset)
	if initialPreset.isdigit() and int(initialPreset) < len(presetList):
		initialPreset = int(initialPreset)
	else:
		initialPreset = 0
		print("Invalid initial preset. Defaulting to 0.")
	preset = getPresetTracks(presetList[initialPreset])
	
	# Start Up and initial setup
	active = False

	keyInput = '\'0\''
	# Start Main loop
	print("Ready for input")
	while keyInput not in inputs or keyInput not in special:
		keyInput = repr(readchar.readkey())

		# Sanitize input
		if keyInput in inputs:
			# Play sound
			santized = int(keyInput[1])
			selected_track = preset[santized]
			print("Input", keyInput, "->", os.path.basename(selected_track))
			player.stop()
			active = True

			playTrack(selected_track)

		# Special Characters
		elif keyInput == special[0]: # '\'*\'
			# Preset
			active = False
			player.stop()
			np = switchPresets(presetList)
			if np != None:
				preset = getPresetTracks(presetList[np])

		elif keyInput == special[1]: # '\'+\''
			# Play/Pause. +
			if active:
				player.pause()
				active = False
			else:
				player.play()
				active = True
		elif keyInput == special[2]: # '\'-\''
			pass

		elif keyInput == '\'x\'':
			# End case
			exit() 