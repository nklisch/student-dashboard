import { API_PATHS, ROOT_URL, LOG } from '../globals'

export async function get(api, queryParameters = {}) {
  const url = ROOT_URL + API_PATHS[api] + addQueryParameters(queryParameters)

  const response = await fetch(url, {
    method: 'GET',
    credentials: 'include',
  })
  if (!response.ok) {
    LOG.error(
      `get: ${api}, status: ${response.status}:${response.statusText}, queryParameters: ${queryParameters}`,
    )
    return null
  }
  return response.json() || response.ok
}

export async function post(api, queryParameters = {}, body = {}) {
  const url = ROOT_URL + API_PATHS[api] + addQueryParameters(queryParameters)
  const response = await fetch(url, {
    method: 'POST',
    credentials: 'include',
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    LOG.error(
      `post: ${api}, status: ${response.status}:${response.statusText}, queryParameters: ${queryParameters}, body: ${body}`,
    )
    return null
  }
  return response.json() || response.ok
}

export function addQueryParameters(parameters) {
  let url = '?'
  for (const [parameter, value] of Object.entries(parameters)) {
    url += `${parameter}=${value}&`
  }
  return url.slice(0, url.length - 1)
}

export async function authenticate() {
  try {
    const response = await get('AUTH')
    if (response) {
      return response
    }
  } catch (e) {
    LOG.error(`${e}`)
  }
  return false
}
