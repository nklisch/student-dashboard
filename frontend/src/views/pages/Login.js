import React from 'react'
import PropTypes from 'prop-types'
import { Redirect, useLocation } from 'react-router-dom'
import { CButton, CCol, CContainer, CImage, CRow } from '@coreui/react'
import { addQueryParameters } from 'src/util/requests'
import { GITHUB_AUTH_URL, GITHUB_APP_CLIENTID, LOGIN_PATH, API_URL, API_PATHS } from 'src/globals'
const Login = (props) => {
  const github_authentication_url =
    GITHUB_AUTH_URL +
    addQueryParameters({
      client_id: GITHUB_APP_CLIENTID,
      redirect_uri: API_URL + API_PATHS.UpdateAuth,
      scope: 'user',
    })
  const { state } = useLocation()

  if (props.isAuthenticated) {
    const to = state?.from ? state?.from && state.from !== LOGIN_PATH : '/'
    return <Redirect to={to} />
  }

  return (
    <CContainer>
      <CRow>
        <CCol lg={{ offset: 2, span: 8 }}>
          <CImage fluid src="/wordcloud.png" />
        </CCol>
      </CRow>
      <CRow className="justify-content-center">
        <CCol className="text-center">
          <h1 className="mt-4">Student Activity Dashboard</h1>
          <h5 className="mb-4 text-muted">CS314 Software Engineering</h5>
          <CButton href={github_authentication_url}>Sign-in with GitHub</CButton>
        </CCol>
      </CRow>
    </CContainer>
  )
}

Login.propTypes = {
  isAuthenticated: PropTypes.bool,
}

export default Login
