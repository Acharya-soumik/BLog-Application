import {
  LOGIN_SUCCESS,
  REGISTER_SUCCESS,
  LOGGED_IN,
  LOG_OUT
} from "./actionType";

const initialState = {
  auth: false,
  login: "",
  register: ""
};
const reducer = (state = initialState, action) => {
  console.log("called reducer here");
  switch (action.type) {
    case LOGIN_SUCCESS:
      let cond = false;
      if (action.payload.status == "login succesfull") {
        cond = true;
      }
      return {
        ...state,
        login: action.payload,
        auth: cond
      };

    case REGISTER_SUCCESS:
      return {
        ...state,
        register: action.payload
      };

    case LOGGED_IN:
      return {
        ...state,
        auth: true,
        token: ""
      };

    case LOG_OUT:
      return {
        ...state,
        auth: false
      };

    default:
      console.log("default redcer");
      return state;
  }
};

export default reducer;
