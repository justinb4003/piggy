seqCommandList = []
immediateCommandList = []

def printActiveCommands():
	print('seq active command list:')
	for c in seqCommandList:
		print(type(c))

	print('immediate active command list:')
	for c in immediateCommandList:
		print(type(c))


def addSequential(cmd):
	seqCommandList.append(cmd)


def addImmediate(cmd):
	immediateCommandList.append(cmd)


def execute():
	cmdExCount = 0

	for c in immediateCommandList:
		cmdExCount += 1
		print(type(c))
		c.execute()
		if c.isFinished():
			c.end()
			immediateCommandList.remove(c)

	if  len(seqCommandList) > 0:
		cmdExCount += 1
		c = seqCommandList[0];
		c.execute()
		if c.isFinished():
			c.end()
			seqCommandList.remove(c)

	if cmdExCount == 0:
		pass
		#print('empty execute loop -- robot has nothing to do.')
	
