import React, { useState } from "react";
import medical_records from "../medicalRecords";

function Search({ setSelectedId }) {
  const [selected, setSelected] = useState("");

  const handleShow = () => {
    if (!selected) {
      alert("Please select a patient name");
      return;
    }
    setSelectedId(selected);
  };

  return (
    <div className="layout-row align-items-baseline select-form-container">
      <div className="select">
        <select
          data-testid="patient-name"
          value={selected}
          onChange={(e) => setSelected(e.target.value)}
        >
          <option value="" disabled>
            Select Patient
          </option>
          {medical_records.map((patient) => (
            <option key={patient.id} value={patient.id}>
              {patient.data[0].userName}
            </option>
          ))}
        </select>
      </div>

      <button type="button" data-testid="show" onClick={handleShow}>
        Show
      </button>
    </div>
  );
}

export default Search;