from django.http import HttpResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def sms(request):
    if request.method == 'POST':
        to = request.POST.get('to')

        if to == 'one':
            url = "https://messaging-service.co.tz/api/sms/v1/test/text/single"

            payload = json.dumps({
                "from": "*******",
                "to": "*******",
                "text": "Hello from Safari",
                "reference": "aswqetgcv"
            })

            headers = {
                'Authorization': 'Basic ***********',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload)

        elif to == 'all':
            url = "https://messaging-service.co.tz/api/sms/v1/text/multi"

            payload = json.dumps({
                "messages":[{
                    "from": "*******",
                    "to": [
                    "255****",
                    "255*****"
                    ],
                    "text": "from Safari backend"}],
                    "reference": "aswqetgcv"
            })

            headers = {
                'Authorization': 'Basic ********',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload)

        elif to == 'group':
            url = "https://messaging-service.co.tz/api/sms/v1/text/multi"

            payload = json.dumps({
                "messages":[{
                    "from": "********",
                    "to": [
                    "255*******",
                    "255*******"
                    ],
                    "text": "from Safari backend"}],
                    "reference": "aswqetgcv"
            })

            headers = {
                'Authorization': 'Basic *********',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload)

        # Check if the request was successful and return an HttpResponse
        if response.status_code == 200:
            return HttpResponse("SMS sent successfully", status=200)
        else:
            return HttpResponse("Failed to send SMS", status=500)

    # Handle other HTTP methods or return an appropriate response for GET requests
    return HttpResponse("Method not allowed", status=405)
