import React, { useEffect, useState } from 'react'
import { CButton, CContainer, CFormControl } from '@coreui/react'
import SprintsTable from './SprintsTable'
import SprintModal from './SprintModal'
import { daysDifference } from 'src/util/dates'

const SemesterSetup = () => {
  const [semesterCode, setSemesterCode] = useState('')
  const [organization, setOrganization] = useState('')
  const [sprints, setSprints, sprintActions] = useSprints(semesterCode)
  const [modalOpen, setModalOpen] = useState(false)
  const [modalEditIndex, setModalEditIndex] = useState(-1)
  const [editOrganization, setEditOrganization] = useState(false)

  useEffect(() => {
    // TODO: fetch sprint/ organization data from server
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
  }, [setSprints])

  const openSprintModal = (sprint = null) => {
    const sprintIndex = sprint ? sprint.id - 1 : -1
    setModalEditIndex(sprintIndex)
    setModalOpen(true)
  }

  return (
    <CContainer className="mb-4">
      <h2 className="text-center">Class Configuration</h2>

      <hr />
      <h4 className="fw-bold mb-4">Base Requirements</h4>
      <h5 className="mb-4">Semester Code: {semesterCode}</h5>

      <h5>GitHub Organization: {organization}</h5>
      {editOrganization && (
        <CFormControl
          type="text"
          placeholder="ex: csucs314s21"
          value={organization}
          onChange={(e) => setOrganization(e.target.value)}
        />
      )}
      <CButton
        className="mt-2 mb-2"
        color="info"
        variant="outline"
        size="sm"
        onClick={() => {
          if (editOrganization && organization.length > 0) {
            // TODO: save change to database?
          }
          setEditOrganization(!editOrganization)
        }}
      >
        {!editOrganization ? 'Edit' : !organization ? 'Cancel' : 'Save'}
      </CButton>

      <hr />
      <h4 className="fw-bold mb-3">Sprints</h4>
      <SprintsTable
        sprints={sprints}
        sprintActions={sprintActions}
        openSprintModal={openSprintModal}
      />
      <div className="d-grid gap-2">
        <CButton color="dark" size="sm" onClick={() => openSprintModal()}>
          Add Sprint
        </CButton>
      </div>

      <SprintModal
        sprints={sprints}
        sprintActions={sprintActions}
        modalOpen={modalOpen}
        setModalOpen={setModalOpen}
        editIndex={modalEditIndex}
        semesterCode={semesterCode}
      />
    </CContainer>
  )
}

const useSprints = (semesterCode) => {
  const [sprints, setSprints] = useState([])

  const normalizeSprints = (sprints) => {
    sprints.sort((s1, s2) => daysDifference(s1.startDate, s2.startDate))
    sprints.forEach((sprint, index) => (sprint.id = index + 1))
  }

  const add = (startDate, endDate) => {
    const newSprint = { id: -1, semester: semesterCode, startDate: startDate, endDate: endDate }
    const newSprints = [...sprints, newSprint]
    normalizeSprints(newSprints)
    setSprints(newSprints)
  }

  const edit = (index, startDate, endDate) => {
    const newSprint = { id: -1, semester: semesterCode, startDate: startDate, endDate: endDate }
    const newSprints = [...sprints]
    newSprints[index] = newSprint
    normalizeSprints(newSprints)
    setSprints(newSprints)
  }

  const remove = (index) => {
    if (index < 0 || index >= sprints.length) {
      console.log('Failed to remove sprint: invalid index')
      return
    }

    const newSprints = [...sprints]
    newSprints.splice(index, 1)
    normalizeSprints(newSprints)
    setSprints(newSprints)
  }

  const deleteAll = () => {
    if (window.confirm('Remove all sprints? This action cannot be undone.')) {
      setSprints([])
    }
  }

  const sprintActions = { add, edit, remove, deleteAll }
  return [sprints, setSprints, sprintActions]
}

export default SemesterSetup
