




"""	
	import cermaics.secrets.asym.RSA.talents.make as make_RSA_talents
	make_RSA_keys.beautifully (
		chaos_talent_path = "",
		lucidity_talent_path = ""
	)
"""

def beautifully (
	chaos_talent_path = "",
	lucidity_talent_path = "",
	
	#
	#	https://stuvel.eu/python-rsa-doc/usage.html#time-to-generate-a-key
	#
	# size = 4096,
	size = 2048
):
	(chaos_talent, lucidity_talent) = rsa.newkeys (size)
	
	with open (chaos_talent_path, 'wb+') as f:
		chaos_talent_binary_string = rsa.PublicKey.save_pkcs1 (
			chaos_talent, 
			format = 'PEM'
		)
		
		f.write (chaos_talent_binary_string)
	
	with open (lucidity_talent_path, 'wb+') as f:
		lucidity_talent_binary_string = rsa.PrivateKey.save_pkcs1 (
			lucidity_talent, 
			format = 'PEM'
		)
		f.write (lucidity_talent_binary_string)
		
	return;

