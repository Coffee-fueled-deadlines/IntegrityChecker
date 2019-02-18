###################################################################
#  Author : Coffee-Fueled-Deadlines                               #
#  Purpose: To record and validate the integrity of a USB drive   #
#  Contact: cookm0803@gmail.com                                   #
###################################################################

How to Use:
    1. Place the files you want inside of your USB drive.

    2. Place "USB-Integrity.py" inside of the root directory
       of the USB drive that you want to verify integrity of.
       
    3. Double click "USB-Integrity.py", it will make a file called
       "hashes.json", this file is a list of the hashes of all files
       on your USB drive.  Do not modify or delete this file.
       
    4. Anytime you want to check the Integrity of the files on your
       USB drive, simply double-click on "USB-Integrity.py" and it
       will re-hash and compare the files to the "hashes.json"
       
    5. Alterately, you may remove "USB-Integrity.py" and "hashes.json"
       from your USB Drive after running the file.  At a later time, you
       may place these files back into the root directory and re-run
       "USB-Integrity.exe" to see if any files have been changed.
       
###################
#  Special Notes  #
###################

In the case that you do not have python set up in path, you may have to
run this script via Command line similar to as follows:

    cd /path/to/directory/
    python USB-Integrity.py

/path/to/directory/ being the path to your USB drive or any directory
that you wish to check the integrity of.
