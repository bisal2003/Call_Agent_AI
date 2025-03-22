import { useState } from "react";
import Home_Main from "./pages/Home_Main";
import { Routes, Route } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import FrontPage from "./pages/FrontPage";
// import Home from "./pages/Home";
function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div data-theme="synthwave" className="min-h-screen ">
        <Routes>
          {/* <Route path="/" element={<HomePage />} /> */}
          <Route path="/" element={<FrontPage />} />
          <Route path="/dashboard" element={<Home_Main />} />

        </Routes>
        <Toaster />
      </div>
    </>
  );
}

export default App;
