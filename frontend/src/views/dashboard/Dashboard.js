import React, { useEffect, useState } from 'react'
import { CCol, CContainer, CRow } from '@coreui/react'
import ComparisonChart from 'src/components/dashboard/ComparisonChart'
import MetricCallout from 'src/components/dashboard/MetricCallout'
import SemesterSetup from 'src/components/dashboard/setup/SemesterSetup'

const Dashboard = () => {
  const [classData, setClassData] = useState([])
  const [studentData, setStudentData] = useState([])
  const labels = ['Commits', 'Pulls', 'Issues', 'Active Days']

  useEffect(() => {
    const classVals = [31, 5, 12, 6] // fetch from server
    const studentVals = [22, 8, 9, 4]

    setClassData(classVals)
    setStudentData(studentVals)
  }, [])

  return (
    <CContainer>
      <h4>Your Progress (Sprint 1)</h4>
      <CRow>
        {labels.map((label, index) => (
          <CCol key={label} sm={3} xs={6}>
            <MetricCallout label={label} value={studentData[index]} />
          </CCol>
        ))}
      </CRow>

      <h4 className="mt-4">Class Perspective</h4>

      <CRow className="mb-4">
        <CCol md={{ span: 10, offset: 1 }} lg={{ span: 8, offset: 2 }} xl={{ span: 6, offset: 3 }}>
          <ComparisonChart labels={labels} studentData={studentData} classData={classData} />
        </CCol>
      </CRow>

      <br />
      <br />
      <br />
      <SemesterSetup />
    </CContainer>
  )
}

const toRelativeScale = (data, otherData) => {
  return data.map((value, index) => {
    const otherValue = otherData[index]
    if (value >= otherValue) {
      return 100
    } else {
      return ((value / otherValue) * 100).toFixed(2)
    }
  })
}

export default Dashboard
