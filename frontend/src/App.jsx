import { Link, Route, Router, Routes } from "react-router-dom";


import "/src/index.css";
import Home from "./components/Home.jsx";
import Landing from "./components/Landing.jsx";
import Dashboard from "./components/Dashboard.jsx";

function App() {

  return (

      <>
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/call" element={<Landing />} />
          <Route path="/dashboard" element={<Dashboard/>} />
        </Routes>
      </>
    
  )
}

export default App
