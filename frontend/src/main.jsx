import React from "react";
import ReactDOM from "react-dom/client";
import { App } from "./app/App.jsx";
import "./shared/styles/reset.scss";
import "./shared/styles/global.scss";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
