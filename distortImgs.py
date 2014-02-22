
# Call the SimpleCV library and import the Image class (for distorting)
# and the ImageSet class (for batch processing). 
from SimpleCV import Image, ImageSet

# Run this file from within the images folder.  Set all files to the ImageSet
set = ImageSet(".");

# Loop over all images in the folder/ImageSet
# [Try "for x in xrange(set-40000):"]
for img in set:
	# Rotate the image counter-clockwise 45 degrees
	rot = img.rotate(45)
	# Rename the image with the old filename and 'Rot' at the end
	oldname = img.filename;
	newname = oldname[0:-4] + 'Rot' + '.png'
	print "Rotating " + oldname + " to " + newname
	rot.save(newname)
	# Flip the image horizontally
	flip = img.flipHorizontal()
	# Rename the image with the old filename and 'Flip' at the end
	oldnameF = img.filename;
	newnameF = oldnameF[0:-4] + 'Flip' + '.png'
	print "Flipping " + oldnameF + " to " + newnameF
	flip.save(newnameF)

