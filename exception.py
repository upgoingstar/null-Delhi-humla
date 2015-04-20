#d = {"message": "All Good"}
d = {"message": "All Good", "status": "OK"}
#l = [1,2]
l = [1,2,3]

try:
	print d["status"]
	print l[2]
except KeyError as e:
	print "Got Key Error"
except IndexError as e:
	print "Got List Index out of range"
finally:
	print "In Finally"
