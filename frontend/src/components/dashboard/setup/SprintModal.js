import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import {
  CButton,
  CForm,
  CFormControl,
  CFormLabel,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CModalTitle,
} from '@coreui/react'

const SprintModal = (props) => {
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [semester, setSemester] = useState(props.semesterCode)
  const [editIndex, setEditIndex] = useState(-1)

  useEffect(() => {
    const initialData = props.modalData
    if (!initialData) return

    if (initialData.editIndex !== -1) {
      setEditIndex(initialData.editIndex)

      const sprintData = initialData.sprintData
      setStartDate(sprintData.startDate)
      setEndDate(sprintData.endDate)
      setSemester(sprintData.semester)
    } else {
      setEditIndex(-1)
      setStartDate('')
      setEndDate('')
      setSemester(props.semesterCode)
    }
  }, [props.modalData])

  const editMode = () => editIndex !== -1

  return (
    <CModal visible={props.modalOpen} onDismiss={() => props.setModalOpen(false)}>
      <CModalHeader onDismiss={() => props.setModalOpen(false)}>
        <CModalTitle>{editMode() ? 'Edit' : 'Add'} Sprint</CModalTitle>
      </CModalHeader>
      <CModalBody>
        <CForm>
          <div className="mb-3">
            <CFormLabel htmlFor="startInput">Start Date</CFormLabel>
            <CFormControl
              id="startInput"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <CFormLabel htmlFor="endInput">End Date</CFormLabel>
            <CFormControl
              id="endInput"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>
          <div className="mb-4">
            <CFormLabel htmlFor="semesterInput">Semester</CFormLabel>
            <CFormControl
              id="semesterInput"
              value={semester}
              onChange={(e) => setSemester(e.target.value)}
            />
          </div>
          {editMode() && (
            <CButton
              color="danger"
              variant="outline"
              onClick={() => {
                if (window.confirm('Delete Sprint ' + (editIndex + 1) + '?')) {
                  props.removeSprint(editIndex)
                  props.setModalOpen(false)
                }
              }}
            >
              Delete
            </CButton>
          )}
        </CForm>
      </CModalBody>
      <CModalFooter>
        <CButton color="secondary" onClick={() => props.setModalOpen(false)}>
          Close
        </CButton>
        <CButton
          color="primary"
          onClick={() => {
            const added = props.addSprint(semester, startDate, endDate, editIndex)
            if (added) props.setModalOpen(false)
          }}
        >
          Save
        </CButton>
      </CModalFooter>
    </CModal>
  )
}

SprintModal.propTypes = {
  modalOpen: PropTypes.bool.isRequired,
  setModalOpen: PropTypes.func.isRequired,
  modalData: PropTypes.object,
  addSprint: PropTypes.func.isRequired,
  removeSprint: PropTypes.func.isRequired,
  semesterCode: PropTypes.string.isRequired,
}

export default SprintModal
