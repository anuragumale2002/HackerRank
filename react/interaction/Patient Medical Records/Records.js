import React from "react";
import medical_records from "../medicalRecords";

function Records({ selectedId, setSelectedId }) {
  let currentIndex = medical_records.findIndex(
    (p) => p.id === String(selectedId)
  );

  if (currentIndex === -1) return null;

  const patient = medical_records[currentIndex];
  const firstRecord = patient.data[0];

  const handleNext = () => {
    const nextIndex =
      currentIndex === medical_records.length - 1 ? 0 : currentIndex + 1;
    setSelectedId(medical_records[nextIndex].id);
  };

  return (
    <div className="patient-profile-container" id="profile-view">
      <div className="layout-row justify-content-center">
        <div
          id="patient-profile"
          data-testid="patient-profile"
          className="mx-auto"
        >
          <h4 id="patient-name">{firstRecord.userName}</h4>
          <h5 id="patient-dob">DOB: {firstRecord.userDob}</h5>
          <h5 id="patient-height">Height: {firstRecord.meta.height} cm</h5>
        </div>

        <button
          className="mt-10 mr-10"
          data-testid="next-btn"
          onClick={handleNext}
        >
          Next
        </button>
      </div>

      <table id="patient-records-table">
        <thead id="table-header">
          <tr>
            <th>SL</th>
            <th>Date</th>
            <th>Diagnosis</th>
            <th>Weight</th>
            <th>Doctor</th>
          </tr>
        </thead>
        <tbody id="table-body" data-testid="patient-table">
          {patient.data.map((record, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{new Date(record.timestamp).toLocaleDateString("en-US", { month: "2-digit", day: "2-digit", year: "numeric" })}</td>
              <td>{record.diagnosis.name}</td>
              <td>{record.meta.weight}</td>
              <td>{record.doctor.name}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Records;