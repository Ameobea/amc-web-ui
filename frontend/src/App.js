import React from "react";

import "./App.css";
import banner from "./components/banner1.png";

import Screens from './screens';

const App = () => (
  <div>
    <div className="banner">
      <img src={banner} />
    </div>
    <div className="body">
      <Screens />
    </div>
  </div>
);

export default App;
