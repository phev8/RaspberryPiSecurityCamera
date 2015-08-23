# Include the Dropbox SDK
import dropbox

class AuthDropbox:
	def __init__(self):
		pass

	def auth(self):
		print( "Starting OAuth floe for Dropbox" )
		# Get your app key and secret from the Dropbox developer website
		app_key = ''
		app_secret = ''
		
		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
		
		# Have the user sign in and authorize this token
		authorize_url = flow.start()
		print('1. Go to: ', authorize_url)
		print('2. Click "Allow" (you might have to log in first)')
		print('3. Copy the authorization code.')
		code = input("Enter the authorization code here: ").strip()
		
		# This will fail if the user enters an invalid authorization code
		access_token, user_id = flow.finish(code)
		self.save_tokens( access_token, user_id )

	def save_tokens( self, access_token, user_id ):
		with open('tokens', 'w') as f:
			f.write( access_token + "\n" )
			f.write( user_id )
			f.close()

if __name__ == '__main__':
	ad = AuthDropbox()
	ad.auth()

