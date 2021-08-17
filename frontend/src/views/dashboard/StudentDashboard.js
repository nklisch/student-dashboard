import React from 'react'
import PropTypes from 'prop-types'
import StudentActivity from '../../components/dashboard/StudentActivity'

const StudentDashboard = ({ user }) => {
  return (
    <>
      <StudentActivity user={user} />
      <br />
      <br />
      <br />
    </>
  )
}

StudentDashboard.propTypes = {
  user: PropTypes.object,
}

export default StudentDashboard
