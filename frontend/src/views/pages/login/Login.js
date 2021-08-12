import React, { useState } from 'react'
import { Redirect, useLocation } from 'react-router-dom'
import { CButton, CCol, CContainer, CRow } from '@coreui/react'
import { authorization } from 'src/assets/util/requests'

const Login = () => {
  const [redirect, setRedirect] = useState(false)
  const { state } = useLocation()
  const parameters = URLSearchParams(window.location.search)
  authorization.authenticate().then(() => {
    setRedirect(authorization.isAuthenticated())
  })

  if (parameters.has('code')) {
    authorization.createAuthentication(parameters.get('code')).then(() => {
      setRedirect(authorization.isAuthenticated())
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
            <CButton href="https://github.com/login/oauth/authorize?client_id=4e07e39677124ccd6c0c">
              Go to Github to authorize
            </CButton>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Login
