import { API_PATHS, API_URL, LOG } from '../globals'

export async function get({ api, pathParameter = '', queryParameters = {} }) {
  const url = `${API_URL}${API_PATHS[api]}${
    pathParameter ? '/' : ''
  }${pathParameter}${addQueryParameters(queryParameters)}`

  const response = await fetch(url, {
    method: 'GET',
    credentials: 'include',
  })
  if (!response.ok) {
    LOG.error(
      `get: ${api}, status: ${response.status}:${response.statusText}, queryParameters: ${queryParameters}`,
    )
    return undefined
  }
  return response.json() || response.ok
}

export async function post({ api, pathParameter = '', queryParameters = {}, body = {} }) {
  const url = `${API_URL}${API_PATHS[api]}${
    pathParameter ? '/' : ''
  }${pathParameter}${addQueryParameters(queryParameters)}`
  const response = await fetch(url, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    LOG.error(
      `post: ${api}, status: ${response.status}:${
        response.statusText
      }, queryParameters: ${JSON.stringify(queryParameters)}, body: ${JSON.stringify(body)}`,
    )
    return undefined
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
    const response = await get({ api: 'Auth' })
    if (response) {
      return response
    }
  } catch (e) {
    LOG.error(`${e}`)
  }
  return false
}
