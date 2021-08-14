import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import {
  CButton,
  CForm,
  CFormControl,
  CFormFeedback,
  CFormLabel,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CModalTitle,
} from '@coreui/react'
import { dateInInterval, dateLessThan, daysBetween, overlappingIntervals } from 'src/util/dates'

const SprintModal = (props) => {
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [startDateError, setStartDateError] = useState('')
  const [endDateError, setEndDateError] = useState('')
  const [editIndex, setEditIndex] = useState(-1)

  useEffect(() => {
    const initialData = props.modalData
    if (!initialData) return

    const editing = initialData.editIndex !== -1
    if (editing) {
      setEditIndex(initialData.editIndex)

      const sprintData = initialData.sprintData
      setStartDate(sprintData.startDate)
      setEndDate(sprintData.endDate)
    } else {
      setEditIndex(-1)
      setStartDate('')
      setEndDate('')
    }
  }, [props.modalData])

  const editMode = () => editIndex !== -1

  const dateOverlapsSprint = (date) => {
    return props.sprints.some(
      (sprint, index) =>
        index !== editIndex && dateInInterval(date, sprint.startDate, sprint.endDate),
    )
  }

  const intervalOverlapsSprint = (date1, date2) => {
    return props.sprints.some(
      (sprint, index) =>
        index !== editIndex && overlappingIntervals(date1, date2, sprint.startDate, sprint.endDate),
    )
  }

  const validateStartDate = (newDate) => {
    if (dateOverlapsSprint(newDate)) {
      setStartDateError('Date overlaps an existing sprint.')
    } else if (intervalOverlapsSprint(newDate, endDate)) {
      setStartDateError('This sprint overlaps an existing sprint.')
    } else {
      setStartDateError('')
    }
  }

  const validateEndDate = (newDate) => {
    if (dateOverlapsSprint(newDate)) {
      setEndDateError('Date overlaps an existing sprint.')
    } else if (startDate.length !== 0 && dateLessThan(newDate, startDate)) {
      setEndDateError('End date is less than start date.')
    } else {
      setEndDateError('')
    }
  }

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
              type="date"
              onChange={(e) => {
                setStartDate(e.target.value)
                validateStartDate(e.target.value)
              }}
              invalid={startDateError.length !== 0}
              required
            />
            <CFormFeedback invalid>{startDateError}</CFormFeedback>
          </div>
          <div className="mb-3">
            <CFormLabel htmlFor="endInput">End Date</CFormLabel>
            <CFormControl
              id="endInput"
              value={endDate}
              type="date"
              onChange={(e) => {
                setEndDate(e.target.value)
                validateEndDate(e.target.value)
              }}
              invalid={endDateError.length !== 0}
              required
            />
            <CFormFeedback invalid>{endDateError}</CFormFeedback>
          </div>
          <h6 className="mt-4 mb-2">Days: {daysBetween(startDate, endDate)}</h6>
          <h6 className="mb-4">Semester: {props.semesterCode}</h6>
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
          disabled={startDateError.length !== 0 || endDateError.length !== 0}
          onClick={() => {
            const added = props.addSprint(startDate, endDate, editIndex)
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
  sprints: PropTypes.arrayOf(PropTypes.object).isRequired,
}

export default SprintModal
