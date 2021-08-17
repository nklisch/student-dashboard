import React from 'react'
import { CContainer } from '@coreui/react'
import PropTypes from 'prop-types'
import StudentDashboard from './StudentDashboard'
import InstructorDashboard from './InstructorDashboard'
import { verify_role } from 'src/globals'
const Dashboard = ({ user }) => {
  let dashboard = { component: StudentDashboard }
  if (verify_role('TeachingAssistant', user.role)) {
    dashboard.component = InstructorDashboard
  }

  return (
    <CContainer>
      <dashboard.component user={user} />
    </CContainer>
  )
}

Dashboard.propTypes = {
  user: PropTypes.object,
}

export default Dashboard
