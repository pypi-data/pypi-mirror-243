

'''
	this_insert = insertion ()
'''
'''
class insertion:
	def __init__ (this):
		primary_key = 
'''

'''
	SOURCES:
		https://healthjade.net/eosinophils/
'''
def now ():
	#primary_key = "episode"
	primary_key = "ellipse"
	db = "eosinophils"
	table = "chemokine receptors"
	
	document = {}

	r.db (db).table (table).insert ({		
		primary_key: (
			r.branch (
				r.db (db).table (table).count () == 0,
				1,
				r.expr (
					r.db (db).table (table).max (primary_key).get_field (
						primary_key
					).coerce_to ('number')
				).add (1)
			)
		),
		** document
	}).run (c)
	
	
def subsequent ():
	r.db (db).table (table).insert ({
		primary_key: (
			r.expr (
				r.db (db).table (table).max (primary_key).getField (
					primary_key
				).coerceTo ('number')
			).add (1)
		),
		
		** document
	}).run (c)

	return;