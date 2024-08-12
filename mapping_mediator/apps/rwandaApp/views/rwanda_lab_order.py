from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import uuid
import json
import requests
import environ
from django.http import HttpResponse, JsonResponse
from apps.rwandaApp.views.common import getUrl
import requests
import json
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

OPENHIM_PORT = env('OPENHIM_PORT')
OPENHIM_HOST = env('OPENHIM_HOST')
ORGANIZATION_ID=env('ORGANIZATION_ID')
REQUESTING_ORGANIZATION_ID=env('REQUESTING_ORGANIZATION_ID')
PERFORMING_ORGANIZATION_ID=env('PERFORMING_ORGANIZATION_ID')

class LabUUIDView(APIView):

    def post(self, request):
        try:
            json_data = request.data
            json_data["id"] = str(uuid.uuid4())
            json_data["specimenID"] = str(uuid.uuid4())
            json_data["organizationID"] = ORGANIZATION_ID
            json_data["requestingOrganizationID"] = REQUESTING_ORGANIZATION_ID
            json_data["performingOrganizationID"] = PERFORMING_ORGANIZATION_ID
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

            # call mapping meditor here
            url = "http://"+OPENHIM_HOST+":"+OPENHIM_PORT+"/lab-order"
            print(url)
            payload = json.dumps(json_data)
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                 return Response(json.loads(response.text))
            else:
                print(f"Request failed with status {response.status_code}: {response.text}")
                return Response({"Error": "An internal server error occurred"}, status=response.status_code)

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
            url = "http://"+OPENHIM_HOST+":"+OPENHIM_PORT+"/vlsm/order"

            print(request.data)
            json_data = request.data
            json_data["labsourceid"] = str(uuid.uuid4())
            payload = json.dumps(json_data)
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 200:
                return Response(json.loads(response.text))
            else:
                print(f"Request failed with status {response.status_code}: {response.text}")
                return Response({"Error": "An internal server error occurred"}, status=response.status_code)

        except Exception as e:
            print(e)
            return Response({"Error":"An internal server error occurred", "Exceptation":str(e)}, status=500)
