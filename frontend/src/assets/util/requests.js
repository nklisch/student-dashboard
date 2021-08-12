import { API_PATHS, ROOT_URL, LOG } from '../globals'

export const authorization = Authentication()

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

function addQueryParameters(parameters) {
  const url = '?'
  for (const [parameter, value] in Object.entries(parameters)) {
    url += `${parameter}=${value}&`
  }
  return url.slice(0, url.length - 1)
}

class Authentication {
  constructor() {
    this.#authenticated = false
  }
  async authenticate() {
    try {
      const response = await get('AUTH')
      if (response) {
        this.#authenticated = response.authenticated
      }
    } catch (e) {
      this.#authenticated = false
    }
  }

  async createAuthentication(github_code) {
    try {
      const response = await post('CREATE_AUTH', { github_code })
      if (response) {
        this.#authenticate = true
      }
    } catch (e) {
      this.#authenticate = false
    }
  }

  isAuthenticated() {
    return this.#authenticate
  }

  logout() {
    this.#authenticated = false
  }
}
