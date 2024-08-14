from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import uuid
import environ
from datetime import datetime
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
FHIR_PORT=env('FHIR_PORT')
FHIR_URL=env('FHIR_URL')

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
            print("................................................................")
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


class LabResult(APIView):

    def post(self, request):
        try:
            print(request.data)
            lab_result_data = request.data
            identifier = "221214-9257-6982"
            subject = lab_result_data.get("patientId")
            effectiveDateTime = lab_result_data.get("resultDispatchedOn")
            date_obj = datetime.strptime(effectiveDateTime, "%d-%b-%Y %H:%M:%S")
            formatted_date_str = date_obj.strftime("%Y-%m-%d")
            lab_result_data["resultDispatchedOn"] = formatted_date_str

            print(effectiveDateTime)
            print(formatted_date_str)
            print(lab_result_data.get("resultDispatchedOn"))
            occurrence = "2012-01-05"
            # url = "http://" + OPENHIM_HOST + ":3447/fhir/ServiceRequest?identifier=" + identifier + "&subject=" + subject + "&occurrence=" + occurrence
            # url = "http://" + OPENHIM_HOST + ":8085/hapi-fhir-jpaserver/fhir/ServiceRequest?identifier="+ identifier +"&subject="+ subject+"&occurrence="+occurrence

            url = "http://" + OPENHIM_HOST + ":" + OPENHIM_PORT + "/" + FHIR_URL + "/ServiceRequest?subject="+ subject +"&occurrence=" + formatted_date_str
            payload = {}
            headers = {}
            print(url)
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response)
            if response.status_code == 200:
                print(response.text)
                print("mmmmmmmmmmmmmmmmmmmmmmmmmmm")
                data = json.loads(response.text)
                patient = data.get("entry")[0]
                if patient:
                    patientID = patient.get("resource").get("subject").get("reference")
                    encounterID = patient.get("resource").get("encounter").get("reference")
                    organizationID = patient.get("resource").get("note")[0].get("authorReference").get("reference")
                    performingPractitionerID = patient.get("resource").get("performer")[0].get("reference")
                    resultsInterpreterID = patient.get("resource").get("subject").get("reference")
                    serviceRequestID = patient.get("resource").get("id")

                    lab_result_data["patientID"] = patientID.split('/')[-1]
                    lab_result_data["encounterID"]=encounterID.split('/')[-1]
                    lab_result_data["organizationID"] = organizationID.split('/')[-1]
                    lab_result_data["performingPractitionerID"] = performingPractitionerID.split('/')[-1]
                    lab_result_data["resultsInterpreterID"] = performingPractitionerID.split('/')[-1]
                    lab_result_data["serviceRequestID"] = serviceRequestID.split('/')[-1]

                    lab_result_data["hivLabResultTaskID"] = str(uuid.uuid4())
                    lab_result_data["labOrderTaskActivityID"] = str(uuid.uuid4())
                    lab_result_data["hivLabResultsDiagnosticReportExampleID"] = str(uuid.uuid4())
                    lab_result_data["hivTestResultViralLoadLogID"] = str(uuid.uuid4())
                    lab_result_data["hivTestResultAbsoluteDecimalID"] = str(uuid.uuid4())
                    lab_result_data["hivTestResultID"] = str(uuid.uuid4())

                url = "http://openhim-mapping-mediator:3003/lab-results"
                payload = json.dumps(lab_result_data)
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                return Response(json.loads(response.text))
            else:
                return Response("No record found")
        except Exception as e:
            print(e)
            return Response({"Error":"An internal server error occurred", "Exceptation":str(e)}, status=500)


class GetLabResults(APIView):

    def get(self, request):
        try:
            print("Get lab Results")
            subject = request.GET.get('subject')
            from_date = "ge"+request.GET.get('from_date')
            to_date = "le"+request.GET.get('to_date')
            # url = "http://" + OPENHIM_HOST + ":" + FHIR_PORT + "/" + FHIR_URL + "/ServiceRequest?subject="+ subject +"&occurrence=" + occurrence
            url = "http://" + OPENHIM_HOST + ":" + OPENHIM_PORT + "/" + FHIR_URL + "/DiagnosticReport?subject="+ subject +"&date="+ from_date +"&date="+ to_date +"&_include=*"
            # url = "http://localhost:8085/hapi-fhir-jpaserver/fhir/DiagnosticReport?subject="+ subject +"&date="+ from_date +"&date="+ to_date +"&_include=*"
            print(url)
            response = requests.request("GET", url, headers={}, data={})

            # print(response.text)
            if response.status_code == 200:
                now = datetime.now()
                lab_result_data = json.loads(response.text)
                lab_result_data_dict = {}
                lab_result_data_dict["now"] = now.strftime("%Y-%m-%d :: %H:%M:%S")
                lab_result_data_dict["status"] = response.status_code
                lab_result_data_dict["message"] = "Success"
                data = []
                if lab_result_data.get("total") > 0:
                    for lab_result in lab_result_data.get("entry"):
                        print("-=========================================================================")
                        # print(lab_result)
                        result = {}
                        lab_result_data_resource = lab_result.get("resource")
                        if lab_result.get("resource").get("resourceType") == "DiagnosticReport":
                            print("DiagnosticReport")
                            result["status"] = lab_result_data_resource.get("status")
                            result["conclusion"] = lab_result_data_resource.get("conclusion")
                            result["effectiveDateTime"] = lab_result_data_resource.get("effectiveDateTime")
                            obs = lab_result_data_resource.get("result")[0].get("reference").split('/')[-1]
                            for lab_result_dg in lab_result_data.get("entry"):
                                lab_result_data_dg = lab_result_dg.get("resource")
                                if lab_result_data_dg.get("resourceType") == "Patient":
                                    print("Patient")
                                    patientId = lab_result_data_dg.get("id")
                                    result["patientId"] = patientId
                                    result["name"] = lab_result_data_dg.get("name")[0].get("given")[0]
                                    result["phone"] = lab_result_data_dg.get("telecom")[0].get("value")
                                    result["birthDate"] = lab_result_data_dg.get("birthDate")
                                    result["upid"] = patientId

                                if lab_result_data_dg.get("resourceType") == "Observation" and obs == lab_result_data_dg.get("id"):
                                    print("Observation")
                                    vlResult = lab_result_data_dg.get("valueInteger")
                                    result["vlResult"] = vlResult
                                    result["result"] = vlResult
                        if result:
                            data.append(result)

                    print(data)
                    lab_result_data_dict["data"] = data
                    return JsonResponse(lab_result_data_dict)
                    # return Response(json.loads(response.text))
                else:
                    return Response("No record found")

        except Exception as e:
            print(e)
            return Response({"Error":"An internal server error occurred", "Exceptation":str(e)}, status=500)
