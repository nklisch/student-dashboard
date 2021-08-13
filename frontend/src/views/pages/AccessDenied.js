import React from 'react'
import { CCol, CContainer, CRow } from '@coreui/react'
const AccessDenied = () => {
  return (
    <div className="bg-light min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md="8">
            <h1>Access Denied: You do not have the correct role to access this dashboard</h1>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}
export default AccessDenied
