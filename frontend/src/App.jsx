import React from 'react'

const panels = [
  { id: 1, title: 'Monsoon Vulnerability Trend', description: 'Line graph: monthly failures + lightning index overlay.' },
  { id: 2, title: 'Top Risk Stations', description: 'Table: location, failure count, avg duration, risk score, action required.' },
  { id: 3, title: 'Gear Type Vulnerability', description: 'Bar chart: Track Circuit, Point, Signal + MTTR by gear.' },
  { id: 4, title: 'Cluster Alert Panel', description: 'List: timestamp, location group, probable cause.' },
  { id: 5, title: 'Longest Failures', description: 'Top 10 by duration with station, gear, cause, action performed.' },
]

export default function App() {
  return (
    <div className="container">
      <header>
        <h1>Failure Analysis Dashboard</h1>
        <p>Wireframe for production React implementation</p>
      </header>

      <main className="grid">
        {panels.map((panel) => (
          <section key={panel.id} className="panel">
            <h2>Panel {panel.id}: {panel.title}</h2>
            <p>{panel.description}</p>
            <div className="placeholder">Visualization placeholder</div>
          </section>
        ))}
      </main>
    </div>
  )
}
