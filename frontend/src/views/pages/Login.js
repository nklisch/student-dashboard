import React from 'react'
import PropTypes from 'prop-types'
import { Redirect, useLocation } from 'react-router-dom'
import { CButton, CCol, CContainer, CRow } from '@coreui/react'
import { addQueryParameters } from 'src/util/requests'
import { GITHUB_AUTH_URL, GITHUB_APP_CLIENTID, LOGIN_PATH } from 'src/globals'
const Login = (props) => {
  const github_authentication_url =
    GITHUB_AUTH_URL +
    addQueryParameters({
      client_id: GITHUB_APP_CLIENTID,
      scope: 'user',
    })
  const { state } = useLocation()

  if (props.isAuthenticated) {
    const to = state?.from ? state?.from && state.from !== LOGIN_PATH : '/'
    return <Redirect to={to} />
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

Login.propTypes = {
  isAuthenticated: PropTypes.bool,
}

export default Login
