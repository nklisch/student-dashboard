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

  const logout = () => {}

  return [isAuthenticated, user, login, logout]
}
