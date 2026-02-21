import React from "react";

function EmployeeValidationForm() {

  const defaultFormState = {
    name: '',
    email: '',
    employeeId: '',
    joiningDate: ''
  }
  const defaultErrorState = {
    name: true,
    email: true,
    employeeId: true,
    joiningDate: true
  }
  const validationRegex = {
    name: /^[A-Za-z ]{4,}$/,
    email:/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/,
    employeeId:/^[\d]{6}$/,
  };

  const isFutureDate = (dateString) => {
  const [day, month, year] = dateString.split("/");
  
  const inputDate = new Date(`${year}-${month}-${day}`);
  const today = new Date("2025-01-01");
  
  today.setHours(0, 0, 0, 0); 

  return inputDate > today;
};

  const [formData, setFormData] = React.useState(defaultFormState);
  const [error, setError] = React.useState(defaultErrorState);
  const hasError = Object.values(error).some(Boolean)

  const handleInputChange = (e) => {
    const {name, value} = e.target;
    setError((prev)=>({
      ...prev,
      [name]: name !=='joiningDate' ? !validationRegex[name].test(value) : isFutureDate(value)
    }))
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }))
  }
  const onSubmit = () => {
    setFormData(defaultFormState)
    setError(defaultErrorState)
  }

  return (
    <div className="layout-column align-items-center mt-20 ">
      <div className="layout-column align-items-start mb-10 w-50" data-testid="input-name">
        <input
          className="w-100"
          type="text"
          name="name"
          value={formData.name}
          placeholder="Name"
          data-testid="input-name-test"
          onChange={handleInputChange}
        />
        {error.name && <p className="error mt-2" style={{color:'RED', fontSize:'12px'}}>
          Name must be at least 4 characters long and only contain letters and spaces
        </p>}
      </div>
      <div className="layout-column align-items-start mb-10 w-50" data-testid="input-email">
        <input
          className="w-100"
          type="text"
          name="email"
          value={formData.email}
          placeholder="Email"
          onChange={handleInputChange}
        />
        {error.email && <p className="error mt-2" style={{color:'RED', fontSize:'12px'}}>
Email must be a valid email address</p>}
      </div>
      <div className="layout-column align-items-start mb-10 w-50" data-testid="input-employee-id">
        <input
          className="w-100"
          type="text"
          name="employeeId"
          value={formData.employeeId}
          placeholder="Employee ID"
          onChange={handleInputChange}
        />
        {error.employeeId && <p className="error mt-2" style={{color:'RED', fontSize:'12px'}}>
          Employee ID must be exactly 6 digits</p>}
      </div>
      <div className="layout-column align-items-start mb-10 w-50" data-testid="input-joining-date">
        <input
          className="w-100"
          type="date"
          name="joiningDate"
          value={formData.joiningDate}
          placeholder="Joining Date"
          onChange={handleInputChange}
        />
        {error.joiningDate && <p className="error mt-2" style={{color:'RED', fontSize:'12px'}}>
          Joining Date cannot be in the future</p>}
      </div>
      <button data-testid="submit-btn" type="submit" onClick={onSubmit} disabled={hasError}>
        Submit
      </button>
    </div>
  );
}

export default EmployeeValidationForm;