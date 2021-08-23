import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import {
  CButton,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
} from '@coreui/react'
import { get } from 'src/util/requests'
import SemesterSetup from './setup/SemesterSetup'
const ClassHistory = () => {
  const [semesters, users] = useSemester()
  return (
    <CTable>
      <CTableHead>
        <CTableHeaderCell>Semester</CTableHeaderCell>
        <CTableHeaderCell>Github Orginization</CTableHeaderCell>
        <CTableHeaderCell>Students</CTableHeaderCell>
        <CTableHeaderCell>Sprints</CTableHeaderCell>
      </CTableHead>
      <CTableBody>
        {semesters &&
          semesters.map((semester, idx) => (
            <CTableRow key={idx}>
              <CTableDataCell>{semester.semester}</CTableDataCell>
              <CTableDataCell>{semester.git_organization}</CTableDataCell>
              <CTableDataCell>
                <CButton onClick={semester.getUsers}>Users</CButton>
              </CTableDataCell>
              <CTable>
                {semester.sprints.map((sprint, idx) => {
                  return (
                    <CTableRow key={idx}>
                      <CTableDataCell>{sprint.id}</CTableDataCell>
                    </CTableRow>
                  )
                })}
              </CTable>
            </CTableRow>
          ))}
      </CTableBody>
    </CTable>
  )
}

export default ClassHistory

function useSemester() {
  const [semesters, setSemesters] = useState([])
  const [users, setUsers] = useState({})
  useEffect(() => {
    get({ api: 'Semesters' }).then((retrieved_semesters) => {
      retrieved_semesters.map((semester) => {
        semester.getUsers = () =>
          get({ api: 'Users', queryParameters: { semester: semester.semester } }).then(
            (retrieved_users) => {
              let new_users = { ...users }
              new_users[semester.semester] = retrieved_users
              setUsers(new_users)
            },
          )
      })
      setSemesters(retrieved_semesters)
    })
  }, [])
  return [semesters, users]
}
