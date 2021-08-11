import React, { useEffect, useState } from 'react'
import {
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CCardTitle,
  CCol,
  CContainer,
  CRow,
} from '@coreui/react'
import SprintsTable from './SprintsTable'
import SprintModal from './SprintModal'

const SemesterSetup = () => {
  const [semesterCode, setSemesterCode] = useState('not set')
  const [organization, setOrganization] = useState('not set')
  const [sprints, setSprints] = useState([])
  const [modalOpen, setModalOpen] = useState(false)
  const [modalData, setModalData] = useState(null)

  useEffect(() => {
    const fetchResult = [
      { id: 1, semester: 'spring2021', startDate: '2021-01-25', endDate: '2021-02-14' },
      { id: 2, semester: 'spring2021', startDate: '2021-02-15', endDate: '2021-03-08' },
      { id: 3, semester: 'spring2021', startDate: '2021-03-09', endDate: '2021-03-28' },
      //{ id: 4, semester: 'spring2021', startDate: '2021-03-29', endDate: '2021-04-25' },
      //{ id: 5, semester: 'spring2021', startDate: '2021-04-26', endDate: '2021-05-14' },
    ]
    setSprints(fetchResult)
    // setSemesterCode("sp2021")
    // setOrganization("csucs314s21")
  }, [])

  const openSprintModal = (sprintData = null) => {
    const sprintIndex = sprintData ? sprintData.id - 1 : -1
    const data = { editIndex: sprintIndex, sprintData: sprintData }
    setModalData(data)
    setModalOpen(true)
  }

  const addSprint = (semester, start, end, replaceIndex) => {
    if (sprints.some((sprint) => sprint.startDate === start)) {
      alert('Attempting to add duplicate start date.')
      return false
    }

    const newSprint = { id: -1, semester: semester, startDate: start, endDate: end }
    const newSprints = [...sprints]
    if (replaceIndex === -1) {
      newSprints.push(newSprint)
    } else {
      newSprints[replaceIndex] = newSprint
    }
    newSprints.sort((s1, s2) => s1.startDate.localeCompare(s2.startDate))
    newSprints.forEach((sprint, index) => (sprint.id = index + 1))
    setSprints(newSprints)
    return true
  }

  const removeSprint = (index) => {
    if (index < 0 || index >= sprints.length) {
      alert('Failed to remove sprint: invalid index')
      return false
    }

    const newSprints = [...sprints]
    newSprints.splice(index, 1)
    newSprints.forEach((sprint, index) => (sprint.id = index + 1))
    setSprints(newSprints)
    return true
  }

  return (
    <CContainer className="mb-4">
      <h2>Class Setup</h2>

      <CRow className="mt-4 mb-4">
        <CCol className="mb-4" sm={12} md={6}>
          <CCard className="border-top-info border-top-3">
            <CCardHeader>Semester Code</CCardHeader>
            <CCardBody>
              <CCardTitle>{semesterCode}</CCardTitle>
              <CButton
                className="mt-2"
                color="info"
                variant="outline"
                size="sm"
                onClick={() => {
                  const result = window.prompt('Enter semester code (ex. spring2021)')
                  if (result != null) setSemesterCode(result)
                }}
              >
                Edit
              </CButton>
            </CCardBody>
          </CCard>
        </CCol>
        <CCol sm={12} md={6}>
          <CCard className="border-top-info border-top-3">
            <CCardHeader>GitHub Organization</CCardHeader>
            <CCardBody>
              <CCardTitle>{organization}</CCardTitle>
              <CButton
                className="mt-2"
                color="info"
                variant="outline"
                size="sm"
                onClick={() => {
                  const result = window.prompt('Enter GitHub organization (ex. csucs314s21)')
                  if (result != null) setOrganization(result)
                }}
              >
                Edit
              </CButton>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>

      <h4>Sprints</h4>
      <SprintsTable sprintData={sprints} openSprintModal={openSprintModal} />
      <div className="d-grid gap-2">
        <CButton color="dark" size="sm" onClick={() => openSprintModal()}>
          Add Sprint
        </CButton>
      </div>

      <SprintModal
        modalOpen={modalOpen}
        setModalOpen={setModalOpen}
        modalData={modalData}
        addSprint={addSprint}
        removeSprint={removeSprint}
        semesterCode={semesterCode}
      />
    </CContainer>
  )
}

SemesterSetup.propTypes = {}

export default SemesterSetup
