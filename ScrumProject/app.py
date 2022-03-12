from typing import Dict

from flask import Flask, request, render_template, jsonify
from requests.auth import HTTPBasicAuth  # to make api calls you need to import
from json import loads
import pprint, json, requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

statuses = [
    {
        "status": 'new',
        "_type": "Status",
        "id": 1,
        "name": "New",
        "color": "#C3FAE8",
        "_links": {
            "self": {
                "href": "/api/v3/statuses/1",
            }
        }
    },
    {
        "status": 'work',
        "_type": "Status",
        "id": 7,
        "name": "In progress",
        "color": "#66D9E8",
        "_links": {
            "status": {
                "href": "/api/v3/statuses/7",
            }
        }
    },
    {
        "status": 'done',
        "_type": "Status",
        "id": 9,
        "name": "Developed",
        "color": "#12B886",
        "_links": {
            "status": {
                "href": "/api/v3/statuses/9",
            }
        }
    },
    {
        "status": 'testing',
        "_type": "Status",
        "id": 10,
        "name": "In testing",
        "color": "#0CA678",
        "_links": {
            "status": {
                "href": "/api/v3/statuses/10",
            }
        }
    },
    {
        "status": "pass",
        "_type": "Status",
        "id": 11,
        "name": "Tested",
        "color": "#087F5B",
        "_links": {
            "status": {
                "href": "/api/v3/statuses/11",
            }
        }
    },
    {
        "status": 'fail',
        "_type": "Status",
        "id": 12,
        "name": "Test failed",
        "color": "#C92A2A",
        "_links": {
            "status": {
                "href": "/api/v3/statuses/12",
            }
        }
    },
    {
        "status": 'close',
        "_type": "Status",
        "id": 13,
        "name": "Closed",
        "color": "#DEE2E6",
        "_links": {
            "status": {
                "href": "/api/v3/statuses/13",
            }
        }
    },
    {
        "status": 'hold',
        "_type": "Status",
        "id": 15,
        "name": "On hold",
        "color": "#FFC078",
        "_links": {
            "status": {
                "href": "/api/v3/statuses/14",
            }
        }
    }
]

# open project Credentials
base_url = 'https://app.purviewservices.com'
api_key = '5fd2f528af9c77b9041a2b7e9c056efdf9783d737b736b070faba362265e08bb'
api_open_key = '35dc2023e6d8a3156d90ef3f049975c25bfa00ef9bf022dfd8d27aca79a78a4f'

# Google_Spreadsheet Credentials
scope = ['https://www.googleapis.com/auth/drive']
cred = ServiceAccountCredentials.from_json_keyfile_name('data/client_secret.json', scope)
client = gspread.authorize(cred)
sheet = client.open_by_url(
    'https://docs.google.com/spreadsheets/d/1vxBPkBDLN9VyznWnoW898PytJFG1i5RN15lvh46HedE').sheet1

def getTasksFromSheets():
    print(sheet.get_all_records())


def addTaskInSheet():
    row = ["4", "Test1", "a", "spreadsheet", "from", "python"]
    sheet.append_row(row)


def updateTaskInSheet():
    sheet.update_cell(1,2,"it's down there somewhere, let me take another look.")


def deleteTaskInSheet():
    sheet.delete_row(4)


getTasksFromSheets()

# Flask
app = Flask(__name__)


@app.route('/whatsapp', )
def whatsapp():
    json_data = request.json
    value = json_data['command']
    cmd = value[:2]  # ct / ut / dt / gt
    print(cmd)
    if cmd == "ct":
        return createTask()
    elif cmd == "dt":
        return deleteTask()
    elif cmd == "gt":
        return getTask()
    elif cmd == "tl":
        getAllTasks()
    else:
        return {"Status": str(cmd)}


def createTask():
    r = {"project": "Friday-Backend", "subject": "Test task1", "title": "title1"}
    r = json.dumps(r)
    payload = json.loads(r)

    resp = requests.post(base_url + '/api/v3/work_packages', json=payload, headers={"Content-Type": "application/json"},
                         auth=HTTPBasicAuth('apikey', api_open_key))
    json_resp = json.loads(resp.text)
    return json_resp


def deleteTask():
    workpackage_url = base_url + '/api/v3/work_packages/' + str("1379")  # creating url
    resp = requests.get(workpackage_url, auth=HTTPBasicAuth('apikey', api_open_key))
    json_resp = loads(resp.text)

    lockVersion = json_resp['lockVersion']

    payload = {"lockVersion": lockVersion, "_links": "hello"}

    resp = requests.delete(workpackage_url, json=payload, headers={"Content-Type": "application/json"},
                           auth=HTTPBasicAuth('apikey', api_open_key))
    json_resp = json.loads(resp.text)
    return json_resp


def updateTask():
    resp = requests.get(base_url + '/api/v3/work_packages', auth=HTTPBasicAuth('apikey', api_open_key))
    return "update"


def getTask():
    response = requests.get(base_url + '/api/v3/work_packages', headers={"Content-Type": "application/json"},
                            auth=HTTPBasicAuth('apikey', api_open_key))
    json_resp = json.loads(response.text)
    raw_tasks = json_resp['_embedded']['elements']
    for task in raw_tasks:
        if (task['_links']['status']['title'] != 'Closed'):
            temp = (str(task['id']) + '\t' + task['_links']['status']['title'] + '\t' + task['subject'] + '\t'
                    + base_url + '/work_packages/' + str(task['id']))
    return temp


def getAllTasks():
    return "update"


if __name__ == '__main__':
    app.run(debug=True)
