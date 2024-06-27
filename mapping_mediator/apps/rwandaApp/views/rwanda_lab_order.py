from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import uuid
import json
import requests
import environ
import datetime
from django.http import HttpResponse, JsonResponse

from apps.rwandaApp.views.common import getUrl
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
import requests
import json
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
import socket
import sys
IPAddr = "192.168.1.12"
class LabUUIDView(APIView):

    def post(self, request):
        try:
            hostname = socket.gethostname()

            print("...................")


            json_data = request.data
            json_data["id"] = str(uuid.uuid4())
            json_data["specimenID"] = str(uuid.uuid4())
            json_data["organizationID"] = str(uuid.uuid4())
            json_data["requestingOrganizationID"] = str(uuid.uuid4())
            json_data["performingOrganizationID"] = str(uuid.uuid4())
            json_data["serviceRequestID"] = str(uuid.uuid4())
            json_data["requestingPractitionerID"] = str(uuid.uuid4())
            json_data["performingPractitionerID"] = str(uuid.uuid4())
            json_data["encounterID"] = str(uuid.uuid4())
            json_data["reasonForHIVTestingID"] = str(uuid.uuid4())
            json_data["patientPregnantID"] = str(uuid.uuid4())
            json_data["isPatientNewID"] = str(uuid.uuid4())
            json_data["labOrderTaskActivityID"] = str(uuid.uuid4())
            json_data["breastfeedingID"] = str(uuid.uuid4())
            json_data["arvRegimenChangedID"] = str(uuid.uuid4())
            json_data["arvRegimenChangedMedicationRequestID"] = str(uuid.uuid4())
            json_data["artTreatmentInitiatedID"] = str(uuid.uuid4())
            json_data["arvTreatmentMedicationRequestID"] = str(uuid.uuid4())
            json_data["artRegimenSwitchedOrSubstitutedID"] = str(uuid.uuid4())
            json_data["specimenConservationID"] = str(uuid.uuid4())
            json_data["hivLabResultTaskID"] = str(uuid.uuid4())
            json_data["sampleDispatchedToLabID"] = str(uuid.uuid4())
            json_data["resultDispatchedToRequestingFacilityID"] = str(uuid.uuid4())
            json_data["hivLabResultsDiagnosticReportExampleID"] = str(uuid.uuid4())
            json_data["transportRequestedLocationID"] = str(uuid.uuid4())
            json_data["transportCurrentLocationID"] = str(uuid.uuid4())
            json_data["resultsInterpreterID"] = str(uuid.uuid4())
            json_data["hivTestResultID"] = str(uuid.uuid4())
            json_data["receiveSMSMessagesID"] = str(uuid.uuid4())
            json_data["arvAdherenceID"] = str(uuid.uuid4())
            json_data["testingPlatformID"] = str(uuid.uuid4())
            json_data["hivTestResultViralLoadLogID"] = str(uuid.uuid4())
            json_data["hivTestResultAbsoluteDecimalID"] = str(uuid.uuid4())
            json_data["vlResultAbsoluteDecimal"] = 25
            json_data["fundingOrganizationID"] = str(uuid.uuid4())
            json_data["implementingPartnerOrganizationID"] = str(uuid.uuid4())
            #print(json_data)

            # call mapping meditor here
            url = "http://"+IPAddr+":5001/lab-order"
            print(url)
            payload = json.dumps(json_data)
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            #print(response.text)
            return Response(json.loads(response.text))
            # return Response(json.loads(payload))


        except Exception as e:
            print(e)
            return Response({"Error":"An internal server error occurred", "Exceptation":str(e)}, status=500)

class LabView(APIView):

    def post(self, request):
        try:
            print(request.data)
            return Response(request.data)# "uniqueId": "1h288",

        except Exception as e:
            print(e)
            return Response({"Error":"An internal server error occurred", "Exceptation":str(e)}, status=500)


class LabOrderSourceIdView(APIView):

    def post(self, request):
        try:
            print(request.data)
            json_data = request.data
            json_data["labsourceid"] = str(uuid.uuid4())


            url = "http://" + IPAddr + ":5001/vlsm/order"

            payload = json.dumps(json_data)
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)

            # print(response.text)
            return Response(json.loads(response.text))

        except Exception as e:
            print(e)
            return Response({"Error":"An internal server error occurred", "Exceptation":str(e)}, status=500)
