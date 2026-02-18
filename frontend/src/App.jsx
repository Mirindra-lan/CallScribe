import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState("")
  useEffect(()=>{
    if(window.qt) {
      new window.QWebChannel(window.qt.webChannelTransport, (channel) => {
        window.backend = channel.objects.backend

        window.backend.dataChanged.connect((data) => {
          setMessage(data)
        })

        window.backend.receiveMessage("React ready ✅")
      })
      console.log(window.QWebChannel)
    }
    else {
      setMessage("Not work")
    }
  }, [])
  return (
    <>
      <p>{message}</p>
    </>
  )
}

export default App
