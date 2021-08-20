import React from 'react'
import PropTypes from 'prop-types'
import SemesterSetup from 'src/components/dashboard/setup/SemesterSetup'
import { CCol, CContainer, CRow } from '@coreui/react'
const InstructorDashboard = ({ user }) => {
  return (
    <CContainer>
      <CRow>
        <CCol xxl={6} xl={8} lg={9} md={10} sm={11} xs={12}>
          <SemesterSetup />
        </CCol>
      </CRow>
    </CContainer>
  )
}

InstructorDashboard.propTypes = {
  user: PropTypes.object,
}

export default InstructorDashboard
