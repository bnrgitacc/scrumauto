import json

x = '{"id":1,"name":"nara"}'
user_json = json.loads(x)
name = user_json["name"]
print(name)

pjsonfile = open('D:\gupshup\ScrumProject\ScrumProject\data\practice.json')
jsondata=pjsonfile.read()
n_json=json.loads(jsondata)
qv=n_json["quiz"]
nv=qv["sport"]
mk=nv["q1"]

result=mk["options"][2]
print(result)
