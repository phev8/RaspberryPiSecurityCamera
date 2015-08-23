# Include the Dropbox SDK
import dropbox
from datetime import datetime

class StreamToDropbox:
	def __init__( self ):
		self.current_index = 0
	
	def init_client(self):
		access_token, user_id = self.read_tokens()
		self.client = dropbox.client.DropboxClient(access_token)
		print( 'linked account: ', self.client.account_info() )

	def read_tokens( self ):
		# TODO: check file path to tokens:
		with open('./tokens', 'r') as f:
			text = f.read()			
			f.close()
		access_token = text.split('\n')[0]
		user_id = text.split('\n')[1]
		return access_token, user_id

	def put_new_image( self, image ):
		# use circle buffer index from 0 to 2500
		self.current_index += 1
		if self.current_index > 2500:
			self.current_index = 0

		response = self.client.put_file('/SecurityCameraPictures/img_' + str(self.current_index) + '.jpg', image, overwrite=True)
		#print( 'uploaded: ', response)
			
		f = "Last pictures time: " + datetime.now().isoformat() + ". Picture index: " + str(self.current_index)
		response = self.client.put_file('/SecurityCameraPictures/current_picture.txt', f, overwrite=True)
		#print( 'uploaded: ', response)


if __name__ == '__main__':
	streamer = StreamToDropbox()
	streamer.init_client()
