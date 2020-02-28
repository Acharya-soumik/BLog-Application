import React, { useState } from "react";
import { connect } from "react-redux";
import { fetchLogin } from "../Redux/auth_action";
import { Link, Redirect } from "react-router-dom";
import Loading from "../Components/Loading";

function Login(props) {
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const clickHandler = () => {
    let obj = {
      email,
      pass: password
    };
    setLoading(true);
    setEmail("");
    setName("");
    setPassword("");
    const timer = setTimeout(() => {
      props.fetchUser(obj);
      setLoading(false);
      props.history.push("/");
    }, 1000);
  };
  if (loading) {
    return <Loading />;
  } else if (props.login) {
    return <Redirect to="/" />;
  }
  return (
    <div className="text-center">
      <h2 className="mb-4">Login Page</h2>
      <div className="col-md-5 border border-danger p-4 m-auto">
        <label>Email</label>
        <input
          className="form-control"
          placeholder="Enter your Email"
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <label>Password</label>
        <input
          className="form-control"
          placeholder="Enter Your Password"
          onChange={e => setPassword(e.target.value)}
          type="password"
          value={password}
        />
        <button className="btn btn-success my-4" onClick={clickHandler}>
          Login
        </button>
        <p>
          Not Logged In ?
          <small>
            <Link to="/signup"> Click Here To Sign Up </Link>
          </small>
        </p>
      </div>
    </div>
  );
}

const mapStateToProps = state => ({
  login: state.auth
});
const mapDispatchToProps = dispatch => ({
  fetchUser: item => dispatch(fetchLogin(item))
});
export default connect(mapStateToProps, mapDispatchToProps)(Login);
