import React, { useState } from "react";
import { connect } from "react-redux";
import { fetchRegister } from "../Redux/auth_action";
import { Link, Redirect } from "react-router-dom";
import Loading from "../Components/Loading";

function Register({ fetchRegister, login }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const clickHandler = () => {
    let obj = {
      name,
      email,
      pass: password
    };
    setLoading(true);
    const timer = setTimeout(() => {
      setLoading(false);
      fetchRegister(obj);
    }, 1000);
    return () => clearTimeout(timer);
  };

  if (loading) {
    return <Loading />;
  } else if (login) {
    return <Redirect to="/" />;
  }

  return (
    <div className="">
      <div className="text-center">
        <h2 className="mb-4">Registration Page</h2>
        <div className="col-md-5 border border-danger p-4 m-auto">
          <label>Name</label>
          <input
            className="form-control "
            placeholder="Enter Your Name"
            onChange={e => setName(e.target.value)}
          />
          <label>Email</label>
          <input
            className="form-control"
            placeholder="Enter your Email"
            type="email"
            onChange={e => setEmail(e.target.value)}
          />
          <label>Password</label>
          <input
            className="form-control"
            placeholder="Enter Your Password"
            type="password"
            onChange={e => setPassword(e.target.value)}
          />
          <button className="btn btn-success my-4" onClick={clickHandler}>
            Register
          </button>
          <p>
            Already Registered ?
            <small>
              <Link to="/login"> Click Here To Sign In </Link>
            </small>
          </p>
        </div>
      </div>
    </div>
  );
}

const mapDispatchToProps = dispatch => ({
  fetchRegister: item => dispatch(fetchRegister(item))
});
const mapStateToProps = state => ({
  login: state.auth
});

export default connect(mapStateToProps, mapDispatchToProps)(Register);
