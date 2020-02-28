import {
  LOGIN_SUCCESS,
  REGISTER_SUCCESS,
  LOGGED_IN,
  LOG_OUT
} from "./actionType";
import axios from "axios";
import swal from "sweetalert";

export const loggedIn = () => {
  return {
    type: LOGGED_IN
  };
};
export const log_out = () => {
  console.log("called action");
  return {
    type: LOG_OUT
  };
};

export const userLogin = item => {
  if (item.token !== undefined) {
    localStorage.setItem("token", JSON.stringify(item.token));
    localStorage.setItem("isLoggedIn", JSON.stringify(true));
    localStorage.setItem("user_id", JSON.stringify(item.u_id));
  }
  swal(item.status);
  return {
    type: LOGIN_SUCCESS,
    payload: item
  };
};

export const userRegister = item => {
  swal(item);
  return {
    type: REGISTER_SUCCESS,
    payload: item
  };
};

export const fetchLogin = ({ email, pass }) => {
  return dispatch => {
    axios
      .post("http://localhost:5000/login", {
        email,
        password: pass
      })
      .then(res => dispatch(userLogin(res.data)));
  };
};

export const fetchRegister = ({ email, pass, name }) => {
  return dispatch => {
    axios
      .post("http://localhost:5000/signup", {
        email: email,
        password: pass,
        username: name
      })
      .then(res => dispatch(userRegister(res.data)))
      .catch(err => console.log(err));
  };
};
