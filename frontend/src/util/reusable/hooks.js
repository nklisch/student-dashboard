import { useState, useEffect } from 'react'
import { authenticate } from '../requests'

export function useAuthentication() {
  const [isAuthenticated, setAuthenticated] = useState(false)
  const [user, setUser] = useState({})
  const login = () => {
    authenticate().then((result) => {
      if (result) {
        setUser(result)
        setAuthenticated(true)
      }
    })
  }
  useEffect(() => {
    login()
  }, [])

  const logout = () => {
    document.cookie = 'token= ; expires = Thu, 01 Jan 1970 00:00:00 GMT'
    document.cookie = 'userId= ; expires = Thu, 01 Jan 1970 00:00:00 GMT'
    setAuthenticated()
  }

  return [isAuthenticated, user, login, logout]
}
