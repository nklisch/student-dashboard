import React, { useState } from 'react'
import { Redirect, useLocation } from 'react-router-dom'
import { CButton, CCol, CContainer, CRow } from '@coreui/react'
import { Authentication, addQueryParameters } from 'src/assets/util/requests'
import { GITHUB_AUTH_URL, GITHUB_APP_CLIENTID, LOGIN_PATH } from 'src/assets/globals'
const Login = () => {
  const login_url = `${window.location.protocol}//${window.location.host}/#/${LOGIN_PATH}`
  const github_authentication_url =
    GITHUB_AUTH_URL +
    addQueryParameters({
      client_id: GITHUB_APP_CLIENTID,
      redirect_uri: login_url,
      scope: 'read:user user:email',
    })
  const [redirect, setRedirect] = useState(false)
  const { state } = useLocation()
  const param_string = window.location.href.slice(
    window.location.href.indexOf('?'),
    window.location.href.length,
  )
  const parameters = new URLSearchParams(param_string)
  console.log(parameters.get('code'))
  console.log(Authentication.isAuthenticated())
  if (!Authentication.isAuthenticated()) {
    Authentication.authenticate().then(() => {
      console.log(Authentication.isAuthenticated())
      if (!Authentication.isAuthenticated()) {
        console.log(Authentication.isAuthenticated())
        if (parameters.has('code')) {
          console.log(Authentication.isAuthenticated())
          Authentication.updateAuthentication(parameters.get('code')).then(() => {
            console.log(Authentication.isAuthenticated())
            setRedirect(Authentication.isAuthenticated())
          })
        }
      }
    })
  }

  if (redirect) {
    return <Redirect to={state?.from || '/'} />
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
