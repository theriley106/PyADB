import pickle

def DictionarySave(filename, dictionary):
	r = []
	#file .p
	try:
		r = pickle.load( open( filename, "rb" ) )
	except:
		pass
	r.append(dictionary)
	pickle.dump( r, open( filename, "wb" ) )
def PicklingList(filename):
	r = pickle.load( open( filename, "rb" ) )
	return r