import React from "react";
import { Link } from "react-router-dom";

const Landing = () => {
  return (
    <div className="flex h-screen text-white">
      <section className="relative w-[30%] bg-gray-700 p-10">
        <img src="/assets/calle.png" alt=""
        className="absolute top-4 left-6 h-14 border w-14 rounded-full bg-white p-1"/>
        <h1 className="text-3xl font-semibold text-center mb-10">CALL.E</h1>
        <form className="space-y-4">
          {[
            "Agent Name",
            "Agent Role",
            "Company Name",
          ].map((label, index) => (
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
          <label className="block text-sm font-medium mb-1">About the business:</label>
            <textarea
            type="message"
            placeholder="Tell us about your business"
            required
            className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none focus:ring-1 focus:ring-gray-500"
            />
            <label className="block text-sm font-medium mb-1">Conversation Purpose:</label>
            <textarea
            type="text"
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
          <button className="w-full mt-4 p-2 bg-blue-700 rounded hover:bg-blue-800 transition">Submit to start call.</button>
        </form>
      </section>

      {/* Right Section */}
      <section className="relative w-[70%] flex flex-col  bg-gray-900 items-center justify-center p-10">
        {/* <div className="grid grid-cols-3 gap-4 mb-6">
          {[...Array(9)].map((_, i) => (
            <div key={i} className="w-16 h-16 bg-gray-800 rounded"></div>
          ))}
        </div> */}
        <nav className="absolute top-0 w-max flex justify-between p-4 space-x-6 text-lg">
          <Link to="/" className="hover:text-blue-400">Home</Link>
          <Link to="/Dashboard" className="hover:text-blue-400">Dashboard</Link>
        </nav>
        <img src="/assets/calle.png" alt="" className="h-[40%]"/>
        <h2 className="text-4xl pt-4 font-semibold">CALL.E</h2>
        <p className="text-lg text-gray-400">Your personal AI Call-Agent</p>
      </section>
    </div>
  );
};

export default Landing;