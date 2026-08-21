import { useEffect, useState } from 'react'

const defaultCode = `#include <iostream>
using namespace std;

int main() {
    cout << "Hello from the C++ sandbox!" << endl;
    return 0;
}`

function App() {
  const [title, setTitle] = useState('hello-world')
  const [code, setCode] = useState(defaultCode)
  const [output, setOutput] = useState('')
  const [scripts, setScripts] = useState([])
  const [sourceFiles, setSourceFiles] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [status, setStatus] = useState('Ready')

  const fetchScripts = async () => {
    try {
      const response = await fetch('http://localhost:8000/scripts')
      const data = await response.json()
      setScripts(data)
    } catch (error) {
      console.error('Error loading scripts:', error)
    }
  }

  useEffect(() => {
    fetchScripts()
    fetchSourceFiles()
  }, [])

  const fetchSourceFiles = async () => {
    try {
      const response = await fetch('http://localhost:8000/source-files')
      const data = await response.json()
      setSourceFiles(data)
    } catch (error) {
      console.error('Error loading source files:', error)
    }
  }

  const handleSave = async () => {
    setStatus('Saving...')
    const response = await fetch('http://localhost:8000/scripts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, code, category: 'general' }),
    })

    const data = await response.json()
    if (response.ok) {
      setStatus('Saved successfully')
      await fetchScripts()
      setTitle(data.title)
    } else {
      setStatus('Save failed')
    }
  }

  const handleRun = async () => {
    setStatus('Running...')
    setOutput('')

    try {
      const response = await fetch('http://localhost:8000/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, code }),
      })

      const data = await response.json()

      if (data.success) {
        setOutput(data.output || 'Program completed without output.')
        setStatus('Execution successful')
      } else {
        setOutput(data.output || 'Execution failed.')
        setStatus('Compile or run error')
      }
    } catch (error) {
      setOutput('Could not connect to the backend server.')
      setStatus('Connection error')
    }
  }

  const loadScript = (script) => {
    setTitle(script.title)
    setCode(script.code)
  }

  const loadSourceFile = async (source) => {
    setStatus('Loading file...')

    try {
      const response = await fetch(`http://localhost:8000/source-files/content?path=${encodeURIComponent(source.path)}`)
      const data = await response.json()

      if (!data.success) {
        setStatus('Could not load source file')
        return
      }

      setTitle(data.title)
      setCode(data.code)
      setStatus(`Loaded ${data.path}`)
    } catch (error) {
      console.error('Error loading source file:', error)
      setStatus('Source file load failed')
    }
  }

  const filteredSources = sourceFiles.filter((source) => {
    const query = searchTerm.toLowerCase()
    return source.title.toLowerCase().includes(query) || source.path.toLowerCase().includes(query)
  })

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <span className="brand-badge">C++</span>
          <h2>Sandbox Runner</h2>
        </div>
        <button className="primary-btn" onClick={handleSave}>Save script</button>

        <div className="source-search-box">
          <input
            type="text"
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
            placeholder="Search .cpp files"
          />
        </div>

        <div className="script-list source-list">
          {filteredSources.length === 0 ? (
            <p>No .cpp files found in src.</p>
          ) : (
            filteredSources.map((source) => (
              <button key={source.path} className="script-item" onClick={() => loadSourceFile(source)}>
                {source.title}
              </button>
            ))
          )}
        </div>

        <div className="script-list">
          {scripts.length === 0 ? (
            <p>No scripts saved yet.</p>
          ) : (
            scripts.map((script) => (
              <button key={script.id} className="script-item" onClick={() => loadScript(script)}>
                {script.title}
              </button>
            ))
          )}
        </div>
      </aside>

      <main className="editor-panel">
        <div className="topbar">
          <input
            type="text"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            placeholder="Script name"
          />
          <button className="primary-btn" onClick={handleRun}>Run</button>
        </div>

        <textarea
          className="code-editor"
          value={code}
          onChange={(event) => setCode(event.target.value)}
          spellCheck={false}
        />

        <div className="console-panel">
          <div className="console-header">
            <span>Status</span>
            <strong>{status}</strong>
          </div>
          <pre>{output || 'Run a script to see the output here.'}</pre>
        </div>
      </main>
    </div>
  )
}

export default App
