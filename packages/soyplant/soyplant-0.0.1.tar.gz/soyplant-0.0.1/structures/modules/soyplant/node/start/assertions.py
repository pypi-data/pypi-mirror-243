



def check (r, c):
	db_list = r.db_list ().run (c)
	assert (db_list == ['rethinkdb', 'test'])