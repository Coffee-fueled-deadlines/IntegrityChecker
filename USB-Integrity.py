import hashlib
import os
import sys
import json
import msvcrt as m

os.system("cls")
currentHashes = {}
############################################
#  Get current hash record of all files    #
############################################
for path, directories, files in os.walk("./", topdown=True):
	for name in files:
		if (name != __file__) and (name != "hashes.json") and (name != "USB-Integrity.exe"):
			FileName = (os.path.join(path, name))
			hasher = hashlib.md5()
			with open(str(FileName), 'rb') as afile:
				buf = afile.read()
				hasher.update(buf)
				afile.close()
			currentHashes[FileName] = hasher.hexdigest()


############################################
#  Check if file has previous hash record  #
############################################
if not os.path.exists("./hashes.json"):
	print("hashes.json not found, assuming first start\n\n\t—hashing file contents, do not close!")
	with open("./hashes.json", "w") as afile:
		json.dump(currentHashes, afile, indent=4, sort_keys=True)
		afile.close()
	print("\n\nhashes.json created!\n\nLeave this program and 'hashes.json' on your USB drive.\n\nTo verify integrity, rerun this program!  If anything changes, you'll be informed!")
	print("\n\nPress any key to exit")
	m.getch()
	sys.exit()

##################################
#  If hash record already found  #
##################################
if (os.path.exists("./hashes.json")):
	with open("./hashes.json") as hashFile:
		previousHashes = json.load(hashFile)
		hashFile.close()
	################################
	#  Check if files are missing  #
	################################
	missingFiles = { k : previousHashes[k] for k in set(previousHashes) - set(currentHashes) }
	if bool(missingFiles) == True:
		print("Some files are missing!")
		for k,v in missingFiles.items():
			print("\n\tMissing: "+str(k))

		#####################################################
		#  Inquire if missing files was intentional or not  #
		#####################################################
		ask = input("\nIs this intentional? ")
		while (ask == "") or (ask[0] != "n") and (ask[0] != "y"):
			ask = input("Is this intentional? ")
		if ask[0].lower() == "n":
			print("\n\nPlease re-add the missing file(s).  Do note, if you've editted this/these file(s) since\nyou may want to delete ./hashes.json on your usb and\nre-run this program to rebuild the hash-record!")
			for k,v in missingFiles.items():
				del previousHashes[k]
		elif ask[0].lower() == "y":
			print("\n\nAdjusting hash-record, please wait...")
			for k,v in missingFiles.items():
				del previousHashes[k]
			with open("./hashes.json", "w") as afile:
				json.dump(previousHashes, afile, indent=4, sort_keys=True)
				afile.close()
			print("\n\tHash record adjusted!")
			missingFiles = False
	####################################
	#  Check if new files are present  #
	####################################
	extraFiles = { k : currentHashes[k] for k in set(currentHashes) - set(previousHashes) }
	if bool(extraFiles) == True:
		print("\n\nExtra files found!")
		for k, v in extraFiles.items():
			print("\n\tExtra: "+str(k))

		###########################################
		#  Inquire if this is intentional or not  #
		###########################################
		ask = input("\nIs this intentional? ")
		while (ask == "") or (ask[0] != "n") and (ask[0] != "y"):
			ask = input("Is this intentional? ")
		if ask[0].lower() == "n":
			print("\n\nPlease remove the extra file(s) and quarenteen them for further inspection if they were unexpected.\nDo note, if you've editted this/these file(s) since the last hash record\nyou may want to delete ./hashes.json on your usb and re-run this program to rebuild the hash-record!")
			for k,v in extraFiles.items():
				previousHashes[k] = v
		if ask[0].lower() == "y":
			for k,v in extraFiles.items():
				previousHashes[k] = v
			with open("./hashes.json", "w") as afile:
				json.dump(previousHashes, afile, indent=4, sort_keys=True)
				afile.close()
			print("\n\tHash record adjusted!")
			extraFiles = False



	if (bool(missingFiles) and bool(extraFiles)) == True:
		INTEGRITY = True
		print("\nExtra/Missing files where Found!!\n\nChecking file integrity of other files:")
		################################################
		#  Check if any files have been tampered with  #
		################################################
		for k1,v1 in previousHashes.items():
			for k2,v2 in currentHashes.items():
				if k2 == k1:
					if v2 != v1:
						print("\n\tFile hash mismatch on file: " + currentHashes[k2])
						INTEGRITY = False

		if INTEGRITY == False:
			print("\n\tFiles where found that HAVE BEEN altered.  We suggest that you restage this thumbdrive as\nit HAS been tampered with.")
		elif INTEGRITY == True:
			print("\n\tNo files have been altered, but Extra/Missing files have been found!\nRestage of usb drive recommended.")

	elif (bool(missingFiles) and bool(extraFiles)) == False:
		INTEGRITY = True
		print("\nNo Extra/Missing files.\n\nChecking file integrity of files:")
		################################################
		#  Check if any files have been tampered with  #
		################################################
		for k1,v1 in previousHashes.items():
			for k2,v2 in currentHashes.items():
				if k2 == k1:
					if v2 != v1:
						print("\n\tFile hash mismatch on file: " + k2)
						INTEGRITY = False

		if INTEGRITY == False:
			print("\n\tFiles where found that HAVE BEEN altered.  We suggest that you restage this thumbdrive as\nit HAS been tampered with.")
		elif INTEGRITY == True:
			print("\n\tNo files have been altered!  This usb drive is safe to use!")

print("\n\n\nPress any key to exit")
m.getch()