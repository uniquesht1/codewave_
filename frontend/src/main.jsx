// src/main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import Login from "./components/Login";
import CreateAccount from "./components/CreateAccount";
import ChatWindow from "./components/ChatWindow";
import ErrorPage from "./components/ErrorPage";
import './index.css'; // Ensure Tailwind is imported


const router = createBrowserRouter([
  {
    path: "/",
    element: <App />, // Main layout with Outlet for child components
    errorElement: <ErrorPage />, // Handles errors like 404
    children: [
      {
        path: "/", // Default route - Login page
        element: <Login />,
      },
      {
        path: "/login", // Explicit login route
        element: <Login />,
      },
      {
        path: "/signup", // SignUp route
        element: <CreateAccount />,
      },
      {
        path: "/chat", // Chat window
        element: <ChatWindow />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
