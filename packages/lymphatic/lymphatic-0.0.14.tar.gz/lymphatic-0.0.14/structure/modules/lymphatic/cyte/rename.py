
'''
	import lymphatic.cyte.rename as rename_cyte
	rename_cyte.now (r, c, "b cyte 1", "b-cyte 1")
'''


'''
	repl:
		r.db ('rethinkdb').table ('db_config').filter ({ 
			name: 'bcyte 1'
		}).update ({ 
			name: 'b-cyte 1'
		}).run ()
		
		
	html data explorer:
		r.db ('rethinkdb').
		table ('db_config').
		filter ({ 
			name: 'b cyte 1' 
		}).
		update ({ 
			name: 'b-cyte 1'
		})
'''

def now (r, c, current, next):
	r.db (current).config ().update ({
		name: next
	}).run (c)

	return;