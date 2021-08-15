import React, { useEffect, useState } from 'react'
import { CButton, CContainer, CFormControl } from '@coreui/react'
import SprintsTable from './SprintsTable'
import SprintModal from './SprintModal'
import { daysDifference } from 'src/util/dates'

const SemesterSetup = () => {
  const [semesterCode, setSemesterCode] = useState('')
  const [organization, setOrganization] = useState('')
  const [sprints, setSprints] = useState([])
  const [modalOpen, setModalOpen] = useState(false)
  const [modalData, setModalData] = useState(null)
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
  }, [])

  const openSprintModal = (sprintData = null) => {
    const sprintIndex = sprintData ? sprintData.id - 1 : -1
    const data = { editIndex: sprintIndex, sprintData: sprintData }
    setModalData(data)
    setModalOpen(true)
  }

  const addSprint = (start, end, replaceIndex) => {
    const editing = replaceIndex !== -1
    const newSprint = { id: -1, semester: semesterCode, startDate: start, endDate: end }
    const newSprints = [...sprints]
    if (!editing) {
      newSprints.push(newSprint)
    } else {
      newSprints[replaceIndex] = newSprint
    }
    newSprints.sort((s1, s2) => daysDifference(s1.startDate, s2.startDate))
    newSprints.forEach((sprint, index) => (sprint.id = index + 1))
    setSprints(newSprints)
  }

  const removeSprint = (index) => {
    if (index < 0 || index >= sprints.length) {
      alert('Failed to remove sprint: invalid index')
      return
    }

    const newSprints = [...sprints]
    newSprints.splice(index, 1)
    newSprints.forEach((sprint, index) => (sprint.id = index + 1))
    setSprints(newSprints)
  }

  const deleteSprints = () => {
    if (window.confirm('Remove all sprints? This action cannot be undone.')) {
      setSprints([])
    }
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
        deleteSprints={deleteSprints}
        openSprintModal={openSprintModal}
      />
      <div className="d-grid gap-2">
        <CButton
          color="dark"
          size="sm"
          onClick={() => {
            openSprintModal()
            /* if (semesterCode && organization) openSprintModal()
            else alert('Provide a valid semester and organization before configuring sprints.') */
          }}
        >
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
        sprints={sprints}
      />
    </CContainer>
  )
}

SemesterSetup.propTypes = {}

export default SemesterSetup
