import React, { useEffect, useState } from 'react'
import {
  CButton,
  CFormControl,
  CFormSelect,
  CInputGroup,
  CRow,
  CCol,
  CInputGroupText,
  CForm,
  CFormLabel,
  CButtonGroup,
} from '@coreui/react'
import SprintsTable from './SprintsTable'
import SprintModal from './SprintModal'
import { daysDifference } from 'src/util/dates'
import { get, post } from 'src/util/requests'
import _ from 'lodash'
import PropTypes from 'prop-types'
import CIcon from '@coreui/icons-react'
const SemesterSetup = () => {
  const [semesterCode, setSemesterCode] = useState('fall2021')
  const [organization, setOrganization] = useState('')
  const [sprints, setSprints, sprintActions] = useSprints(semesterCode)
  const [modalOpen, setModalOpen] = useState(false)
  const [modalEditIndex, setModalEditIndex] = useState(-1)
  useEffect(() => {
    get({ api: 'SetupSemester', queryParameters: { semester: semesterCode } }).then((result) => {
      setSprints(result?.sprints ? result.sprints : [])
      setOrganization(result?.git_organization)
    })
  }, [semesterCode])

  const save = () => {
    post({
      api: 'SetupSemester',
      body: { semester: semesterCode, git_organization: organization, sprints: sprints },
    }).then((results) => {})
  }

  const openSprintModal = (sprint = null) => {
    const sprintIndex = sprint ? sprint.id - 1 : -1
    setModalEditIndex(sprintIndex)
    setModalOpen(true)
  }

  return (
    <>
      <CForm className="mb-4">
        <h2 className="text-center">Class Configuration</h2>

        <hr />
        <CRow>
          <CCol>
            <CFormLabel className="mb-4">
              <b>Semester Code:</b> {semesterCode}{' '}
            </CFormLabel>
          </CCol>
          <CCol xxl={5} xl={6} lg={7} md={8} sm={9} xs={10}>
            <SemesterSelect setSemester={setSemesterCode} />
          </CCol>
        </CRow>
        <CRow>
          <CCol>
            <CFormLabel>
              <b>GitHub Organization:</b> {organization}
            </CFormLabel>
          </CCol>
          <CCol>
            <CFormControl
              size="sm"
              type="text"
              placeholder="ex: csucs314s21"
              onChange={(e) => setOrganization(e.target.value)}
            />
          </CCol>
        </CRow>
      </CForm>
      <hr />
      <h4 className="fw-bold mb-3">Sprints</h4>

      <SprintsTable
        sprints={sprints}
        sprintActions={sprintActions}
        openSprintModal={openSprintModal}
      />
      <div className="d-grid gap-2">
        <CButtonGroup>
          <CButton color="dark" size="sm" variant="outline" onClick={() => openSprintModal()}>
            Add Sprint
          </CButton>
          <CButton onClick={save} color="dark" size="sm" variant="outline">
            <CIcon name="cil-save" />
          </CButton>
        </CButtonGroup>
      </div>

      <SprintModal
        sprints={sprints}
        sprintActions={sprintActions}
        modalOpen={modalOpen}
        setModalOpen={setModalOpen}
        editIndex={modalEditIndex}
        semesterCode={semesterCode}
      />
    </>
  )
}

const useSprints = (semester_code) => {
  const [sprints, setSprints] = useState([])

  const normalizeSprints = (sprints) => {
    sprints.sort((s1, s2) => daysDifference(s1.start_date, s2.start_date))
    sprints.forEach((sprint, index) => (sprint.id = index + 1))
  }

  const add = (start_date, end_date) => {
    const newSprint = {
      id: -1,
      semester: semester_code,
      start_date: start_date,
      end_date: end_date,
    }
    const newSprints = [...sprints, newSprint]
    normalizeSprints(newSprints)
    setSprints(newSprints)
  }

  const edit = (index, start_date, end_date) => {
    const newSprint = {
      id: -1,
      semester: semester_code,
      start_date: start_date,
      end_date: end_date,
    }
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

const SemesterSelect = ({ setSemester }) => {
  const seasons = ['fall', 'summer', 'spring']
  const [seasonValue, setSeason] = useState(seasons[0])
  const currentYear = new Date().getFullYear()
  const years = _.range(currentYear, currentYear + 3)
  const [yearValue, setYear] = useState(years[0])
  useEffect(() => {
    setSemester(`${seasonValue}${yearValue}`)
  }, [])
  return (
    <CInputGroup>
      <CFormSelect
        onChange={(e) => {
          setSeason(e.target.value)
          setSemester(`${e.target.value}${yearValue}`)
        }}
        className="mb-3"
        size="sm"
        variant="btn-group"
      >
        {seasons.map((season, idx) => {
          return <option key={idx}>{season}</option>
        })}
      </CFormSelect>
      <CFormSelect
        onChange={(e) => {
          setYear(e.target.value)
          setSemester(`${seasonValue}${e.target.value}`)
        }}
        className="mb-3"
        size="sm"
        variant="btn-group"
      >
        {years.map((year, idx) => {
          return <option key={idx}>{year}</option>
        })}
      </CFormSelect>
    </CInputGroup>
  )
}

SemesterSelect.propTypes = {
  setSemester: PropTypes.func,
}
