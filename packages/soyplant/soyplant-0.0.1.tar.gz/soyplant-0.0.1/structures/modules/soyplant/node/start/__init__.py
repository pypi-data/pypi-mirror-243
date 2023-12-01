

'''
	import pathlib
	import soydrink.node.start as start_node
	ly = start_node.attractively (
		proxy = "yes",
		server_name = "node-1",
		ports = {
			"driver": 0,
			"cluster": 0,
			"http": 0	
		},
		process = {
			"cwd": pathlib.Path (__file__).parent.resolve ()
		},
		rethink_params = [
			f"--daemon",
			f"--pid-file {}"
		]
	)
'''

import soydrink.node.start.assertions as node_start_assertions

def attractively (
	proxy = "no",
	
	server_name = "",
	rethink_params = [],
	ports = {},
	
	records = 1,
	
	** keywords
):
	assert (type (server_name) == str)
	assert (len (server_name) >= 1)
	
	#
	process_keys = keywords ["process"]

	#
	driver_port = str (ports ["driver"])
	cluster_port = str (ports ["cluster"])
	http_port = str (ports ["http"])
	
	node_string = "rethinkdb"
	if (proxy):
		node_string += " proxy"
	
	script = " ".join ([
		node_string,
		
		f"--server-name { server_name }",
		
		f"--driver-port { driver_port }",
		f"--cluster-port { cluster_port }",
		f"--http-port { http_port }",
		
		* rethink_params
	])
	process = subprocess.Popen (
		shlex.split (script),
		** process_keys
	)
	
	server_data = c.server ();
	assert (server_data ["name"] == server_name)
	
	node_start_assertions.check (r, c)		
	c.close ()

	return;