import requests
import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
import os

class RUVSUpload:
	def init(self, user, password):
		self.username = user
		self.password = password
		self.host = 'https://tesis.sld.cu/index.php'
		self.headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
		}
	def upload(self, path, chat):
		options ={ 
		'url': f'{self.host}?P=UserLogin',
		'method': 'POST',
		'headers': {
			**self.headers
			},
			'data': {
			'F_UserName': self.username,
			'F_Password': self.password
			}
		}
		response = requests.post(options['url'], headers=options['headers'], data=options['data'])
		
		if response.status_code == 200:
			cookie = response.headers['Set-Cookie']
			body = response.text
			if '?P=Home' in body:
				config = {
				'method': 'GET',
				'maxBodyLength': float('inf'),
				'url': f'{self.host}?P=EditResource&ID=NEW',
				'headers': {
				'Cookie': cookie
				}
				}
				
				response = requests.get(config['url'], headers=config['headers'])
				body = response.text
				
				if response.status_code == 200:
					ID = body.split('<form name="EditForm" method="post" enctype="multipart/form-data" action="index.php?P=EditResourceComplete&amp;ID=')[1].split('">')[0]
					uploadOptions = {
					'url': f'{self.host}?P=EditResourceComplete&ID={ID}',
					'method': 'POST',
					'files': {
					'PDF': open(path, 'rb')
					},
					'data': {
					'F_Title': 'Testing'
					},
					'headers': {
					'Content-Type': 'multipart/form-data',
					'Cookie': cookie
					}
					}
					
					response = requests.post(uploadOptions['url'], headers=uploadOptions['headers'], files=uploadOptions['files'], data=uploadOptions['data'])
					
					if response.status_code == 200:
						tam = sizeof_fmt(os.stat(path).st_size)
						text=f"🔗: [{path.split('/')[-1]}]({self.host}?P=EditResource&ID={ID}) - **[{tam}]**\n*User:* `julio` *Passw:* `UploadZ0*`\n\n**Power by [FrancyJ2M](mailto:frankramiro.martinez@nauta.cu)**"
						replies.add(text=text, sender="Subida exitosa! 🔥", chat=chat)
						replies.send_reply_messages()
						print("Archivo subido exitosamente\n\n")
					else:
						replies.add(text="Ocurio un error en la subida del archivo, por favor comuniquelo al admin", sender="Error en subida!", chat=chat)
						replies.send_reply_messages()
						print(response.text)
				else:
					replies.add(text="*Archivo denegado por el host!!*", sender="Error en subida!", chat=chat)
					replies.send_reply_messages()
					print(response.text)
		else:
			replies.add(text=f"El [host]({self.host}) esta off, por favor verefircar y sino es asi comuniquelo al [admin](mailto:frankramiro.martinez@nauta.cu)", sender="Inicio de sesion!", chat=chat)
			replies.send_reply_messages()
			print(response.text)
			
def sizeof_fmt(num: float) -> str:
    """Format size in human redable form."""
    suffix = "B"
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)  # noqa
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)  # noqa
#finish
