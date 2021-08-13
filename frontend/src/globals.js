import ulog from 'ulog'

ulog.level = ulog.ERROR
export const ROOT_URL = 'http://localhost:8000/'
export const LOG = ulog('Student Dashboard')
export const API_PATHS = {
  AUTH: 'authenticate/user',
  UPDATE_AUTH: 'authenticate/update',
}

export const ACCESS_DENIED = '/access_denied'
export const LOGIN_PATH = '/login'

export const GITHUB_APP_CLIENTID = '4e07e39677124ccd6c0c'

export const GITHUB_AUTH_URL = 'https://github.com/login/oauth/authorize'

export function verify_role(required_role, current_role) {
  const roleToValue = { SuperUser: 0, Instructor: 1, TeachingAssistant: 2, Student: 3 }
  return roleToValue[current_role] <= roleToValue[required_role]
}
