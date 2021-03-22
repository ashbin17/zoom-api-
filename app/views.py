from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json

# Create your views here.

client_id = "ksJ258wUS4u4NEaLVV5eNw"
secret = "yyj046IwhVT15V7CUqMFubLHl4YYUhLn"
encode = client_id+":"+secret

def base64_encode(message):
    import base64
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def home(request):
    return render(request, 'home.html', {})


def zoom_return(request):
    code = request.GET["code"]
    base64 = base64_encode(encode)

    # establish connection with zoom and get access token

    data = requests.post(
        f"https://zoom.us/oauth/token?grant_type=authorization_code&code={code}&redirect_uri=https://f94959c13605.ngrok.io/zoom_return",
        headers={
            "Authorization": "Basic " + base64
        })
    access_token = data.json()["access_token"]

    # Get user details sing access token

    user_details = requests.get(
        f"https://api.zoom.us/v2/users/me",
        headers={
            "Authorization": "Bearer " + access_token
        }
    )
    id = user_details.json()["id"]

    # Get webinar details

    webinar = requests.get(
        f"https://api.zoom.us/v2/users/{id}/webinars",
        headers={
            "Authorization": "Bearer " + access_token
        }
    )
    # print(webinar.text) //print the webinar details on console

    # Get meeting details

    meeting = requests.get(
        f"https://api.zoom.us/v2/users/{id}/meetings",
        headers={
            "Authorization": "Bearer " + access_token
        }
    )
    # print(meeting.text)
    data_dict = meeting.json()
    return render(request, 'zoom_return.html', {'data': data_dict})
