import React, { useState, useEffect } from 'react'
import { Redirect, useLocation } from 'react-router-dom'
import { CButton, CCol, CContainer, CRow } from '@coreui/react'
import { Authentication, addQueryParameters } from 'src/assets/util/requests'
import { GITHUB_AUTH_URL, GITHUB_APP_CLIENTID, LOGIN_PATH } from 'src/assets/globals'
const Login = () => {
  const github_authentication_url =
    GITHUB_AUTH_URL +
    addQueryParameters({
      client_id: GITHUB_APP_CLIENTID,
      scope: 'read:user user:email',
    })
  const [redirect, setRedirect] = useState(Authentication.isAuthenticated())
  const { state } = useLocation()
  useEffect(() => {
    if (!Authentication.isAuthenticated()) {
      Authentication.authenticate().then(() => {
        setRedirect(Authentication.isAuthenticated())
      })
    }
  }, [])

  if (redirect) {
    const to = state?.from ? state?.from && state.from !== LOGIN_PATH : '/'
    return <Redirect to={'/'} />
  }

  return (
    <div className="bg-light min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md="8">
            <h1>Authenticate with GitHub</h1>
            <CButton href={github_authentication_url}>Go to Github to authorize</CButton>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Login
