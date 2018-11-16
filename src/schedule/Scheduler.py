seq_command_list = []
immediate_command_list = []

def print_active_commands():
	print('seq active command list:')
	for c in seq_command_list:
		print(type(c))

	print('immediate active command list:')
	for c in immediate_command_list:
		print(type(c))


def add_sequential(cmd):
	seq_command_list.append(cmd)


def add_immediate(cmd):
	immediate_command_list.append(cmd)


def execute():
	cmdExCount = 0

	for c in immediate_command_list:
		cmdExCount += 1
		print(type(c))
		c.execute()
		if c.isFinished():
			c.end()
			immediate_command_list.remove(c)

	if  len(seq_command_list) > 0:
		cmdExCount += 1
		c = seq_command_list[0];
		c.execute()
		if c.is_finished():
			c.end()
			seq_command_list.remove(c)

	if cmdExCount == 0:
		pass
		#print('empty execute loop -- robot has nothing to do.')
	
