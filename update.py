import json

def change_value(file_name, page_readed):
	with open('cache.json', 'r+') as cache:
	    data = json.load(cache)
	    data["files"][file_name] = page_readed
	    cache.seek(0)
	    json.dump(data, cache, indent=4)
	    cache.truncate()

def get_values(file_name):
	with open('cache.json', 'r+') as cache:
	    data = json.load(cache)
	    files = data["files"]
	    for itens in files:
	    	if itens == file_name:
	    		return files[itens]
	    	else:
	    		pass
	    return 0
