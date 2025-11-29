import "./index.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import getServerStatus from "@services/getServerStatus";
import VerificationPage from "@pages/VerificationPage";

function App() {
  getServerStatus().then((responce) => {
    console.log("Connection Status: " + responce);
  });

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/verify" replace />} />
        <Route path="/verify" element={<VerificationPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
