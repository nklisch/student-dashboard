import React from 'react'
import PropTypes from 'prop-types'
import { CChartRadar } from '@coreui/react-chartjs'

const ComparisonChart = ({ labels, studentData, classData }) => {
  return (
    <CChartRadar
      data={{
        labels: labels,
        datasets: [
          getRadarDataset('Me', studentData, [54, 162, 235]),
          getRadarDataset('Class', classData, [180, 182, 187]),
        ],
      }}
    />
  )
}

ComparisonChart.propTypes = {
  labels: PropTypes.arrayOf(PropTypes.string).isRequired,
  studentData: PropTypes.arrayOf(PropTypes.number).isRequired,
  classData: PropTypes.arrayOf(PropTypes.number).isRequired,
}

const getRadarDataset = (label, data, rgb) => {
  const [red, green, blue] = rgb
  const mainRGB = `${red}, ${green}, ${blue}`

  return {
    label: label,
    backgroundColor: `rgba(${mainRGB}, 0.2)`,
    borderColor: `rgba(${mainRGB}, 1)`,
    borderWidth: 2,
    pointBackgroundColor: `rgba(${mainRGB}, 1)`,
    pointBorderColor: '#fff',
    pointHighlightFill: '#fff',
    pointHighlightStroke: `rgba(${mainRGB}, 1)`,
    data: data,
  }
}

export default ComparisonChart
