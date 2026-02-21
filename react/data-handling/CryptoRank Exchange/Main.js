import React, { useState } from "react";
import Table from "./Table";

const AVAILABLE_BALANCE = 17042.67;

function Main() {
  const [amount, setAmount] = useState("");
  const [error, setError] = useState("");

  const validateAmount = (value) => {
    if (value === "") {
      setError("Amount cannot be empty");
      return false;
    }

    const num = parseFloat(value);

    if (num < 0.01) {
      setError("Amount cannot be less than $0.01");
      return false;
    }

    if (num > AVAILABLE_BALANCE) {
      setError("Amount cannot exceed the available balance");
      return false;
    }

    setError("");
    return true;
  };

  const handleChange = (e) => {
    const value = e.target.value;
    setAmount(value);
    validateAmount(value);
  };

  const isValid =
    amount !== "" &&
    parseFloat(amount) >= 0.01 &&
    parseFloat(amount) <= AVAILABLE_BALANCE;

  return (
    <div className="layout-column align-items-center mx-auto">
      <h1>CryptoRank Exchange</h1>

      <section>
        <div className="card-text layout-column align-items-center mt-12 px-8 flex text-center">
          <label>
            I want to exchange ${" "}
            <input
              className="w-10"
              data-testid="amount-input"
              type="number"
              placeholder="USD"
              value={amount}
              onChange={handleChange}
            />{" "}
            of my $<span>{AVAILABLE_BALANCE}</span>:
          </label>

          {error && (
            <p
              data-testid="error"
              className="form-hint error-text mt-3 pl-0 ml-0"
            >
              {error}
            </p>
          )}
        </div>
      </section>

      <Table amount={amount} isValid={isValid} />
    </div>
  );
}

export default Main;
