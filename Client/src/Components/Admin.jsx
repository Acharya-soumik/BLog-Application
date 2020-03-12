import React, { useState } from "react";
import axios from "axios";

function Admin() {
  const [category, setCategory] = useState("");
  const submitHandler = () => {
    let data = {
      category: category
    };
    axios
      .post("http://localhost:5000/new_category", data)
      .then(res => console.log(res.data));
  };
  return (
    <div className="text-center container">
      <h2>Admin Panel</h2>
      <hr />
      <p className="lead text-center">Add A new Category</p>
      <div className="col-md-4 m-auto">
        <input
          className="form-control"
          value={category}
          onChange={e => setCategory(e.target.value)}
        />
        <button className="btn btn-outline-danger my-4" onClick={submitHandler}>
          Add
        </button>
      </div>
    </div>
  );
}

export default Admin;
