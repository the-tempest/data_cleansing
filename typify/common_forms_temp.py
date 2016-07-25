# commmon form storage
# in case regex doesn't work out

# full names
# possible_forms = ['Xx', 'Xx Xx', 'Xx X Xx', 'Xx X. Xx', 'Xx x Xx', 'Xx x. Xx', 'Xx, Xx', 'Xx, Xx X', 'Xx, Xx X.', 'Xx, Xx x.', 'Xx, Xx x', 'X Xx', 'X. Xx', 'Xx, X', 'Xx, X.']
		
# first names
# possible_forms = ['Xx', 'X Xx', 'X. Xx']

# last names
# possible_forms = ['Xx', 'X Xx', 'X. Xx']

# datestrings
#types_without_dow = ['Xx 0, 0', '0 Xx 0', 'Xx. 0, 0', '0 Xx. 0', 'x 0, 0', '0 x 0', 'x. 0, 0', '0 x. 0']
		#types_with_dow = []
		#for elem in types_without_dow:
		#	types_with_dow.append('x ' + elem)
		#	types_with_dow.append('Xx ' + elem)
		#	types_with_dow.append('Xx. ' + elem)
		#	types_with_dow.append('x. ' + elem)
		#	types_with_dow.append('Xx, ' + elem)
		#	types_with_dow.append('x, ' + elem)
		#	types_with_dow.append('Xx., ' + elem)
		#	types_with_dow.append('x., ' + elem)
		#
#possible_forms = ['x 0', 'Xx 0', '0 x', '0 Xx', 'x. 0', 'Xx. 0', '0 x.', '0 Xx.'] + types_without_dow + types_with_dow

# full addresses
#address_types = ['0 Xx Xx.', '0 Xx x.', '0 Xx x', '0 Xx Xx', '0 X Xx Xx.', '0 X Xx x.', '0 X Xx x', '0 X Xx Xx', '0 X. Xx Xx.', '0 X. Xx x.', '0 X. Xx x', '0 X. Xx Xx']
		#for x in range(len(address_types)):
		#	address_types.append(address_types[x] + ', Xx. 0')
		#	address_types.append(address_types[x] + ', Xx 0')
		#	address_types.append(address_types[x] + ', x. 0')
		#	address_types.append(address_types[x] + ', x 0')
		#	address_types.append(address_types[x] + ' Xx. 0')
		#	address_types.append(address_types[x] + ' Xx 0')
		#	address_types.append(address_types[x] + ' x. 0')
		#	address_types.append(address_types[x] + ' x 0')
		#
		#for x in range(len(address_types)):
		#	address_types.append(address_types[x] + ', Xx, XX 0')
		#	address_types.append(address_types[x] + ', Xx Xx, XX 0')
		#	address_types.append(address_types[x] + ' Xx, XX 0')
		#	address_types.append(address_types[x] + ' Xx Xx, XX 0')

