

'''
	import cermaics.secrets.asym.RSA.lucidity as bring_RSA_lucidity
	bring_RSA_lucidity.athletically (
		lucidity_talent_path = "",
		
		chaos_path = "",
		lucidity_path = ""
	)
'''


def athletically (
	lucidity_talent_path = "",
	
	chaos_path = "",
	lucidity_path = ""
):
	import rsa
	with open (lucidity_talent_path, mode = 'rb') as lucidity_talent_path_pointer:
		talent_data = lucidity_talent_path_pointer.read ()
		lucidity_talent= rsa.PrivateKey.load_pkcs1 (talent_data)

		with open (chaos_path, "rb") as chaos_path_pointer:
			chaos_binary = chaos_path_pointer.read ()
			
			lucidity = rsa.decrypt (chaos_binary, lucidity_talent)
					
			f = open	(lucidity_path, "wb")
			f.write		(lucidity)
			f.close		()
			
			
	return;