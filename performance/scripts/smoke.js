import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:5001'

import { generateBundle } from "../resources/hhims-bundle-transaction.js";

export const options = {
  vus: 1,
  iterations: 1,
  thresholds: {
    http_req_failed: ['rate<0'],
    http_req_sending: ['p(95)<10'],
    http_req_receiving: ['p(95)<10'],
    http_req_duration: ['p(95)<2000']
  },
  noVUConnectionReuse: false,
  discardResponseBodies: false
}

function submitTransactionBundle() {
  const data = generateBundle()

  const response = http.post(
    `${BASE_URL}/fhir`,
    JSON.stringify(data[0]),
    {
      headers: {
        "Content-Type": "application/fhir+json", 
        Authorization: 'Custom test'
      },
      tags: { name: 'POST Bundle' }
    }
  )
  check(response, {
    'Transaction Bundle status 200': r => r.status === 200
  })

  const body = JSON.parse(response.body);
  const patientId = body.entry[0].response.location.match(/Patient\/([0-9a-xA-X-]+)\/_history/) || [];
  const patientIdentifierPHN = data[0].entry[0].resource.identifier[0].value;
  const encounterId = body.entry[1].response.location.match(/Encounter\/([0-9a-xA-X-]+)\/_history/) || [];

  return {
    patientId: patientId[1],
    patientIdentifierPHN,
    encounterId: encounterId[1]
  }
}

function getPatientByID(id) {
  const response = http.get(
    `${BASE_URL}/fhir/links/Patient/${id}`,
    {
      headers: { Authorization: 'Custom test' },
      tags: { name: 'Get Patient by ID' }
    }
  )
  check(response, {
    'Get Patient By ID': r => r.status === 200
  })
}

function getAllEncountersForPatient(id) {
  const response = http.get(
    `${BASE_URL}/fhir/Encounter?subject:Patient=${id}&_include=Encounter:subject`,
    {
      headers: { Authorization: 'Custom test' },
      tags: { name: 'Get all Encounters for a Patient' }
    }
  )
  const body = JSON.parse(response.body);
  check(body, {
    'All Encounter for Patient is 1': b => b.total === 1
  })
}

function getAllEncountersBetweenTimeline() {
  const response = http.get(
    `${BASE_URL}/fhir/Encounter?date=ge2024-02-28&date=le2024-03-03&_include=Encounter:subject&_sort=date`,
    {
      headers: { Authorization: 'Custom test' },
      tags: { name: 'Get all Encounters between a timeline' }
    }
  )
  const body = JSON.parse(response.body);
  check(body, {
    'Encounter length between timeline is more than or equal to 1': b => b.total >= 1
  })
}

function getLatestEncounterForPatient(id) {
  const response = http.get(
    `${BASE_URL}/fhir/Encounter?subject:Patient=${id}&_include=Encounter:subject&_sort=-date&_count=1`,
    {
      headers: { Authorization: 'Custom test' },
      tags: { name: 'Get all latest Encounter for Patient' }
    }
  )
  const body = JSON.parse(response.body);
  check(body, {
    'latest Encounter for patient is 1': b => b.total === 1
  })
}

function getPatientByIdentier(identifier) {
  const response = http.get(
    `${BASE_URL}/fhir/Patient?identifier=${identifier}`,
    {
      headers: { Authorization: 'Custom test' },
      tags: { name: 'Get patient by identifier' }
    }
  )
  check(response, {
    'Patient found by Identifier': r => r.status === 200
  })
}

function getPatientByIdentierInclNamespace(identifier, namespace) {
  const response = http.get(
    `${BASE_URL}/fhir/Patient?identifier=${namespace}|${identifier}`,
    {
      headers: { Authorization: 'Custom test' },
      tags: { name: 'Get patient by identifier and namespace' }
    }
  )
  check(response, {
    'Patient found by Identifier/namespace': r => r.status === 200
  })
}

function getPatientSummary(id) {
  const response = http.get(
    `${BASE_URL}/fhir/Patient/${id}/$summary`,
    {
      headers: { Authorization: 'Custom test' },
      tags: { name: 'Get a patient summary' }
    }
  )
  const body = JSON.parse(response.body);
  check(body, {
    'Summary length is 8': b => b.total === 8
  })
}

function getAllResourcesLinkedToEncounter(id) {
  const response = http.get(
    `${BASE_URL}/fhir/Encounter/${id}/$everything`,
    {
      headers: { Authorization: 'Custom test' },
      tags: { name: 'Get all resources linked to Encounter' }
    }
  )
  const body = JSON.parse(response.body);
  check(body, {
    'Encounter resources length is 18': b => b.total === 18
  })
}

function getEncounterAndVerifyTerminologyMapping(id) {
  const response = http.get(
    `${BASE_URL}/fhir/Encounter/${id}`,
    {
      headers: { Authorization: 'Custom test' },
      tags: { name: 'Get all resources linked to Encounter' }
    }
  )
  const body = JSON.parse(response.body);
  check(body, {
    'OCL: Encounter updated reasonCode value is 82272006': (body.reasonCode[0].coding[0].code === '82272006'),
    'OCL: Encounter updated reasonCode display is Common cold': (body.reasonCode[0].coding[0].display === 'Common cold')
  })
}

export default function () {
  const response = submitTransactionBundle();
  getPatientByID(response.patientId)
  getAllEncountersForPatient(response.patientId)
  getAllEncountersBetweenTimeline()
  getLatestEncounterForPatient(response.patientId)
  getPatientByIdentier(response.patientIdentifierPHN)
  getPatientByIdentierInclNamespace(response.patientIdentifierPHN, 'http://fhir.health.gov.lk/ips/identifier/phn')
  getPatientSummary(response.patientId)
  getAllResourcesLinkedToEncounter(response.encounterId)

  // OCL test - confirm incoming/outgoing reasonCode is updated
  getEncounterAndVerifyTerminologyMapping(response.encounterId)  // submitted reasoCode was LKRFE65
}