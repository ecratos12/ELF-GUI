def read_data_from_file(file_name):
	f = open(file_name, "rb")            #read file bytes
	byte_array = []
	cur_len = 0
	byte = f.read(1)
	while byte != b'':
		byte_array.append(byte)
		cur_len += 1
		byte = f.read(1)
	f.close()

	f = open(file_name, "rb")
	header = str(f.read(64))
	f.close()

	header = header[2:header.find('\\')]

	new_byte=[]                          #get 16-x code (2 bytes)

	for i in range(64,len(byte_array),1):
		time_s = str(byte_array[i])
		time_s = repr(time_s)

		if("\\x" in time_s):
			time_s = time_s[6:8]
		else:       
			time_s = hex(ord(time_s[3:4]))[2:]

		new_byte.append(time_s)
		
	chanel1 = []
	chanel2 = []                               #get 10-x data

	for i in range(0,len(new_byte),4):
		time_s1 = new_byte[i] + new_byte[i+1]
		time_s2 = new_byte[i+2] + new_byte[i+3]
		c1 =  int(time_s1,16)
		c2 =  int(time_s2,16)
		chanel1.append(c1)
		chanel2.append(c2)
	print(len(chanel1),len(chanel2))
	#print(chanel1)
	#print(chanel2)
	return chanel1[:chanel1.index(0)], chanel2[:chanel2.index(0)], header
