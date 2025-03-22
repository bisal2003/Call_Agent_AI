import React, { useState } from "react";
import { NavLink } from "react-router-dom";

const Landing = () => {
  const [isActive, setIsActive] = useState("Make a Call");

  // Common gradient styles for all NavLinks
  const baseGradientStyle = {
    background: "linear-gradient(to right, #111827 50%, #374151 50%)",
    backgroundSize: "200% 100%",       // Make the gradient 2x the width
    transition: "background-position 0.5s ease-out",
  };

  // Function to decide background position based on which link is active
  const getBackgroundPosition = (linkName) => {
    return isActive === linkName ? "0% 0%" : "100% 0";
  };

  // Handlers for hover to move background from right to left
  const handleMouseEnter = (e) => {
    e.currentTarget.style.backgroundPosition = "0% 0%";
  };
  const handleMouseLeave = (e, linkName) => {
    // If link is not active, reset background to the right
    if (isActive !== linkName) {
      e.currentTarget.style.backgroundPosition = "100% 0";
    }
  };

  return (
    <div className="flex h-screen text-white">
      {/* Left Section */}
      <section className="relative w-[30%] bg-gray-700 p-10">
        <img
          src="/assets/calle.png"
          alt=""
          className="absolute top-4 left-6 h-14 border w-14 rounded-full bg-white p-1"
        />
        <h1 className="text-3xl font-semibold text-center mb-10 centerhead">
          CALL.E
        </h1>
        <form className="space-y-4">
          {["Agent Name", "Agent Role", "Company Name"].map((label, index) => (
            <div key={index}>
              <label className="block text-sm font-medium mb-1">{label}</label>
              <input
                type="text"
                placeholder={`Enter ${label.toLowerCase()}`}
                required
                className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none focus:ring-1 focus:ring-gray-500"
              />
            </div>
          ))}
          <label className="block text-sm font-medium mb-1">
            About the business:
          </label>
          <textarea
            placeholder="Tell us about your business"
            required
            className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none focus:ring-1 focus:ring-gray-500"
          />
          <label className="block text-sm font-medium mb-1">
            Conversation Purpose:
          </label>
          <textarea
            placeholder="Enter purpose of conversation"
            required
            className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none focus:ring-1 focus:ring-gray-500"
          />
          <label className="block text-sm font-medium mb-1">Call Directory:</label>
          <input
            type="file"
            placeholder="Upload your call directory file"
            required
            className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none focus:ring-1 focus:ring-gray-500"
          />
          <button className="w-full mt-4 p-2 bg-blue-700 rounded hover:bg-blue-800 transition">
            Submit to start call.
          </button>
        </form>
      </section>

      {/* Right Section */}
      <section className="relative w-[70%] flex flex-col bg-gray-900 items-center justify-center p-10">
        {/* Navigation */}
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
            to="/Call"
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
            to="/Dashboard"
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

        {/* Main Content */}
        <img src="/assets/calle.png" alt="" className="h-[40%]" />
        <h2 className="text-5xl pt-4 font-semibold centerhead">CALL.E</h2>
        <p className="text-lg text-gray-400">Your personal AI Call-Agent</p>
      </section>
    </div>
  );
};

export default Landing;
