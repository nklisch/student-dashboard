import React, { useEffect, useMemo, useState } from 'react'
import { CCol, CRow } from '@coreui/react'
import ComparisonChart from 'src/components/dashboard/ComparisonChart'
import MetricCallout from 'src/components/dashboard/MetricCallout'

import { get } from 'src/util/requests'
import PropTypes from 'prop-types'

const StudentActivity = ({ user }) => {
  const [studentData, setStudentData] = useState([])
  const labels = useMemo(
    () => ({
      Commits: 'Commits',
      Pulls: 'Pulls',
      Issues: 'Issues',
      ActiveDays: 'Active Days',
    }),
    [],
  )
  const norm = Object.keys(labels).map(() => 100)

  useEffect(() => {
    get('StudentActivity', `${user.id}`, { sprintId: 1 }).then((result) => {
      if (!result) {
        return
      }
      const classValues = []
      let studentValues = []
      for (const key of Object.keys(labels)) {
        classValues.push(result[key].target)
        studentValues.push(result[key].score)
      }
      studentValues = toRelativeScale(studentValues, classValues)
      setStudentData(studentValues)
    })
  }, [labels, user.id])

  return (
    <React.Fragment>
      <h4 className="mt-4">Class Perspective</h4>
      <CRow className="mb-4">
        <CCol md={{ span: 10, offset: 1 }} lg={{ span: 8, offset: 2 }} xl={{ span: 6, offset: 3 }}>
          <ComparisonChart
            labels={Object.values(labels)}
            studentData={studentData}
            classData={norm}
          />
        </CCol>
      </CRow>

      <h4>Your Progress</h4>
      <CRow>
        {Object.keys(labels).map((key, index) => (
          <CCol key={key} sm={3} xs={6}>
            <MetricCallout label={labels[key]} value={studentData[index]} />
          </CCol>
        ))}
      </CRow>
    </React.Fragment>
  )
}

const toRelativeScale = (data, otherData) => {
  return data.map((value, index) => {
    const otherValue = otherData[index]
    return ((value / otherValue) * 100).toFixed(2)
  })
}

StudentActivity.propTypes = {
  user: PropTypes.object,
}

export default StudentActivity
