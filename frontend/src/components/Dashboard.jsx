import React, { useState } from "react";
import { FaFileDownload } from "react-icons/fa";
import { NavLink } from "react-router-dom";

const Dashboard = () => {
  const [isActive, setIsActive] = useState("Dashboard");

  // Gradient logic from your previous code
  const baseGradientStyle = {
    background: "linear-gradient(to right, #111827 50%, #374151 50%)",
    backgroundSize: "200% 100%", // 2x width for horizontal translation
    transition: "background-position 0.5s ease-out",
  };

  // Position the gradient left or right depending on isActive
  const getBackgroundPosition = (linkName) => {
    return isActive === linkName ? "0% 0%" : "100% 0";
  };

  // Hover handlers to animate background from right to left
  const handleMouseEnter = (e) => {
    e.currentTarget.style.backgroundPosition = "0% 0%";
  };
  const handleMouseLeave = (e, linkName) => {
    if (isActive !== linkName) {
      e.currentTarget.style.backgroundPosition = "100% 0";
    }
  };

  // Tracks which tab is active in the content area
  const [activeTab, setActiveTab] = useState("calls");

  const Calldetails = [
    { name: "BoAt", date: "22nd March", time: "2 min 45s" },
    { name: "LensKart", date: "calls", time: "2 min 45s" },
    { name: "Nyka", date: "summary", time: "2 min 45s" },
    { name: "etc", date: "", time: "2 min 45s" },
  ];

  const summaries = [
    { name: "BoAt", date: "22nd March", link: "" },
    { name: "LensKart", date: "calls", link: "" },
    { name: "Nyka", date: "summary", link: "" },
    { name: "etc", date: "", link: "" },
  ];

  const overviews = [
    { Aname: "X", role: "Salesman", com: "BoAt" },
    { Aname: "Emma", role: "Salesman", com: "LensKart" },
    { Aname: "Alex", role: "HR", com: "Nyka" },
    { Aname: "Bo", role: "etc", com: "etc" },
  ];

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-gray-900 text-white">
      {/* Left Section */}
      <img
        src="/assets/calle.png"
        alt=""
        className="absolute top-4 left-6 h-14 border w-14 rounded-full bg-white p-1"
      />
      <div className="w-[30%] p-8 flex flex-col items-center border-r border-gray-700">
        <h1 className="text-3xl font-bold mb-16">USER DASHBOARD</h1>
        <img
          src="/assets/user.png"
          alt="Profile"
          className="w-[40vh] h-[40vh] pt-3 rounded-full border-4 border-white bg-gray-500"
        />
        <h1 className="text-2xl font-semibold mt-4">Subrata Lodh</h1>
        <p className="text-gray-400">7002422805 · he/him</p>
        <h1 className="text-gray-400">CALL.E</h1>
        <button className="mt-4 px-4 py-2 bg-gray-700 rounded hover:bg-gray-600 transition">
          Edit Profile
        </button>
      </div>

      {/* Right Section - Content */}
      <div className="relative w-[70%] p-8">
        {/* NAVBAR (Exact same as previous code) */}
        <nav className="absolute top-[16px] right-10 w-[90%] flex font-bold uppercase justify-end bg-[#374151] py-2 rounded-full px-8 space-x-6 text-lg">
          <NavLink
            to="/"
            onClick={() => setIsActive("Home")}
            style={{
              ...baseGradientStyle,
              backgroundPosition: getBackgroundPosition("Home"),
            }}
            className="rounded-4xl px-4 py-1 text-center"
            onMouseEnter={handleMouseEnter}
            onMouseLeave={(e) => handleMouseLeave(e, "Home")}
          >
            Home
          </NavLink>

          <NavLink
            to="/call"
            onClick={() => setIsActive("Make a Call")}
            style={{
              ...baseGradientStyle,
              backgroundPosition: getBackgroundPosition("Make a Call"),
            }}
            className="rounded-4xl px-4 py-1 text-center"
            onMouseEnter={handleMouseEnter}
            onMouseLeave={(e) => handleMouseLeave(e, "Make a Call")}
          >
            Make a Call?
          </NavLink>

          <NavLink
            to="/dashboard"
            onClick={() => setIsActive("Dashboard")}
            style={{
              ...baseGradientStyle,
              backgroundPosition: getBackgroundPosition("Dashboard"),
            }}
            className="rounded-4xl px-4 py-1 text-center"
            onMouseEnter={handleMouseEnter}
            onMouseLeave={(e) => handleMouseLeave(e, "Dashboard")}
          >
            Dashboard
          </NavLink>
        </nav>

        <div className="flex space-x-8 mt-[8vh] border-b border-gray-700 pb-2">
          {[
            { name: "Overview", key: "overview" },
            { name: "Calls", key: "calls" },
            { name: "Summary", key: "summary" },
          ].map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`pb-2 font-bold text-xl uppercase cursor-pointer ${
                activeTab === tab.key
                  ? "border-b-2 border-blue-400 text-blue-400"
                  : "hover:text-gray-400"
              }`}
            >
              {tab.name}
            </button>
          ))}
        </div>

        {/* CONTENT SECTION */}
        <div className="mt-6">
          {activeTab === "summary" && (
            <div className="w-full">
              <h2 className="text-xl font-semibold mb-4">Summary list</h2>
              <ul className="flex space-y-4 space-x-4 flex-wrap">
                {summaries.map((x, index) => (
                  <li
                    key={index}
                    className="w-[48%] h-[30%] p-4 bg-gray-800 rounded"
                  >
                    <div className="flex justify-between">
                      <h3 className="text-lg font-semibold text-blue-400">
                        {x.name}
                      </h3>
                      <button className="text-lg font-semibold text-blue-400 cursor-pointer">
                        <FaFileDownload />
                      </button>
                    </div>
                    <p className="text-gray-400">Updated on {x.date}</p>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {activeTab === "calls" && (
            <div className="w-full">
              <h2 className="text-xl font-semibold mb-4">Calls</h2>
              <ul className="flex space-y-4 space-x-4 flex-wrap">
                {Calldetails.map((x, index) => (
                  <li
                    key={index}
                    className="w-[48%] h-[30%] p-4 bg-gray-800 rounded"
                  >
                    <div className="flex justify-between">
                      <h3 className="text-lg font-semibold text-blue-400">
                        {x.name}
                      </h3>
                      <h1 className="text-lg font-semibold text-blue-400">
                        Duration: {x.time}
                      </h1>
                    </div>
                    <p className="text-gray-400">Updated on {x.date}</p>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {activeTab === "overview" && (
            <div className="w-full">
              <h2 className="text-xl font-semibold mb-4">Overviews</h2>
              <ul className="flex space-y-4 space-x-4 flex-wrap">
                {overviews.map((x, index) => (
                  <li
                    key={index}
                    className="w-[48%] h-[30%] p-4 bg-gray-800 rounded"
                  >
                    <div className="flex justify-between">
                      <h3 className="text-lg font-semibold text-blue-400">
                        Agent: {x.Aname}
                      </h3>
                      <h1 className="text-lg font-semibold text-blue-400">
                        Company: {x.com}
                      </h1>
                    </div>
                    <p className="text-gray-400">Role: {x.role}</p>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
