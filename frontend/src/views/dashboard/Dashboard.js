import React from 'react'
import { CChartRadar } from '@coreui/react-chartjs'

const Dashboard = () => {
  return (
    <CChartRadar
      data={{
        labels: ['Commits', 'Pulls', 'Issues', 'Active Days'],
        datasets: [
          {
            label: 'Target',
            backgroundColor: 'rgba(220, 220, 220, 0.2)',
            borderColor: 'rgba(220, 220, 220, 1)',
            pointBackgroundColor: 'rgba(220, 220, 220, 1)',
            pointBorderColor: '#fff',
            pointHighlightFill: '#fff',
            pointHighlightStroke: 'rgba(220, 220, 220, 1)',
            data: [100, 100, 100, 100],
          },
          {
            label: 'Current Progress',
            backgroundColor: 'rgba(151, 187, 205, 0.2)',
            borderColor: 'rgba(151, 187, 205, 1)',
            pointBackgroundColor: 'rgba(151, 187, 205, 1)',
            pointBorderColor: '#fff',
            pointHighlightFill: '#fff',
            pointHighlightStroke: 'rgba(151, 187, 205, 1)',
            data: [125, 120, 40, 19],
          },
        ],
      }}
    />
  )
}

export default Dashboard
