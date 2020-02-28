import React from "react";
import { Provider } from "react-redux";
import { store } from "./Redux/store";
import Navbar from "../src/Routes/Navbar";
import "./App.css";

function App() {
  return (
    <Provider store={store}>
      <Navbar />
    </Provider>
  );
}

export default App;
