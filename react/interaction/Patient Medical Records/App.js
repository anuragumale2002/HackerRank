import React, { useState } from "react";
import medical_records from "./medicalRecords";
import Search from "./components/Search";
import Records from "./components/Records";

function App() {
  const [selectedId, setSelectedId] = useState(null);

  return (
    <div>
      <Search setSelectedId={setSelectedId} />
      <Records
        selectedId={selectedId}
        setSelectedId={setSelectedId}
      />
    </div>
  );
}

export default App;