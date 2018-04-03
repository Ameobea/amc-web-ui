import React from "react";

import "./App.css";
import QuestionForm from "./components/QuestionForm";
import banner from "./components/banner.png";

const App = () => (
  <div>
    <div className="banner">
      <img src={banner} />
    </div>
    <div className="body">
      <ul className="navBar">
        <li>Home</li>
        <li>Other Items</li>
      </ul>
      <div className="questions">
        <h1 className="headtext">Enter your question, answers, and check correct answers.</h1>
        <QuestionForm />
      </div>
    </div>
  </div>
);

export default App;
