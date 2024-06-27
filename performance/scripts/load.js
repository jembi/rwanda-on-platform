import http from 'k6/http'
import { check } from 'k6'

const BASE_URL = __ENV.BASE_URL || 'http://localhost:5001'

import { generateBundle } from "../resources/hhims-bundle-transaction.js";

export const options = {
  stages: [
    {duration: '30s', target: 100},
    {duration: '1m', target: 100},
    {duration: '30s', target: 0}
  ],
  thresholds: {
    http_req_failed: ['rate<0.1'],
    http_req_sending: ['p(95)<10'],
    http_req_receiving: ['p(95)<10'],
    http_req_duration: ['p(95)<1000']
  },
  noVUConnectionReuse: true,
  discardResponseBodies: true
}

function makeGetRequest() {
  const data = generateBundle()

  const response = http.post(
    `${BASE_URL}/fhir`,
    JSON.stringify(data[0]),
    {
      headers: {
        "Content-Type": "application/json",
        Accept: 'application/json',
        Authorization: 'Custom test'
      },
      tags: {
        name: 'POST Bundle'
      }
    }
  )
  check(response, {
    'status code is 200': r => r.status === 200
  })
}

export default function () {
  makeGetRequest()
}
