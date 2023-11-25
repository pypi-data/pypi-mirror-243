

'''
	import cermaics.secrets.asym.RSA.lucidity as bring_RSA_chaos
	bring_RSA_chaos.athletically (
		chaos_talent_path = "",

		lucidity_path = "",
		chaos_path = ""
	)
'''

def athletically (
	chaos_talent_path = "",
	
	lucidity_path = "",
	chaos_path = ""
):
	import rsa
	with open (chaos_talent_path, mode = 'rb') as chaos_talent_path_pointer:
		chaos_talent_binary_string = chaos_talent_path_pointer.read ()
		chaos_talent = rsa.PublicKey.load_pkcs1 (chaos_talent_binary_string)
		
		with open (lucidity_path, "rb") as lucidity_path_pointer:
			lucidity_binary_string = lucidity_path_pointer.read ()
			
			chaos = rsa.encrypt (
				lucidity_binary_string, 
				chaos_talent
			)
					
			f = open (chaos_path, "wb")
			f.write (chaos)
			f.close ()
		
	return chaos;