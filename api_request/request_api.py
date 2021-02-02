import requests
import base64

def get_json(url):
	response = requests.get(url)
	return response.json()

def encode_file(file):
	with open(file, 'rb') as file:
		encoded_data = base64.b64encode(file.read())
	return encoded_data

def decode_file(encoded_data, name, extension):	
	with open(f'{name}.{extension}', "wb") as file:
		decoded_data = base64.b64decode(encoded_data)
		file.write(decoded_data)
	pass

def send_json(url, encoded_data, extension, model):
    params = {'encoded_data': encoded_data, 'extension': extension, 'model': model}
    response = requests.post(url, data=params)
    return response

def delete_json(url, id):
	response = requests.delete(f'{url}{id}')
	return response

url = "http://127.0.0.1:8000/api/todo/"

encoded_data = encode_file('auc.wav')
print(len(encoded_data))
send_json(url, encoded_data, 'wav', 'ru')
print(get_json(url))
#decode_file(encoded_data, 'auc_new', 'wav')
