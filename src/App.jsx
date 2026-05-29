import './App.css'

function App() {
  return (
    <>
      <div className = 'Crown_Mold'>{[...Array(27)].map((_, i) => (<span key = {i} className = 'top'></span>))}</div>
      <div className = 'Base_Board'>{[...Array(27)].map((_, i) => (<span key = {i} className = 'bottom'></span>))}</div>
    </>
  )
}

export default App
