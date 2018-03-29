import React from "react";

import "./App.css";
import QuestionForm from "./components/QuestionForm";
import banner from "./components/banner.png";

class App extends React.Component {
  handleSubmit = () => {
    alert(this.questionNameRef.value + this.answer1Ref.value + this.answer2Ref.value + this.answer3Ref.value + this.answer4Ref.value);
  }

  render = () => (

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
}

export default App;
