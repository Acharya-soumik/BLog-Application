import React, { useEffect, useState } from "react";
import axios from "axios";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
function NewBlog(props) {
  const [catagory, setCatagory] = useState([]);
  const [user, setUser] = useState([]);
  const [details, setDetails] = useState({
    title: "",
    content: "",
    catagory: ""
  });

  useEffect(() => {
    let status = localStorage.getItem("isLoggedIn");
    if (status == "true") {
      let token = JSON.parse(localStorage.getItem("token"));
      let data = {};
      axios
        .post("http://localhost:5000/details", data, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `bearer ${token}`
          }
        })
        .then(res => setUser(res.data));
    }
    // GETTING USER
    axios
      .get("http://127.0.0.1:5000/catagories")
      .then(res => setCatagory(res.data));
  }, []);

  const clickHandle = () => {
    alert("post added");
    let obj = {
      title: details.title,
      content: details.content,
      user_id: user.id,
      catagory_id: details.catagory
    };
    axios
      .post("http://127.0.0.1:5000/new_post", obj)
      .then(res => console.log(res));
  };
  return (
    <div>
      {props.login ? (
        <div className="p-3">
          <h2 className="text-center">Add A New Post</h2>
          <div className="col-md-5 m-auto border border-dark rounded">
            <input
              className="form-control my-3"
              placeholder="Add Title"
              onChange={e => setDetails({ ...details, title: e.target.value })}
            />
            <textarea
              className="form-control my-3"
              placeholder="Enter Feed Here..."
              type="text"
              cols="10"
              rows="5"
              onChange={e =>
                setDetails({ ...details, content: e.target.value })
              }
            />
            <label>Select Category</label>
            <select
              className="form-control mb-3"
              onChange={e =>
                setDetails({ ...details, catagory: e.target.value })
              }
            >
              {catagory.map(ele => (
                <option key={ele.id} value={ele.id}>
                  {ele.catagories}
                </option>
              ))}
            </select>
            <button className="btn btn-outline-dark mb-4" onClick={clickHandle}>
              Add Post
            </button>
          </div>
        </div>
      ) : (
        <Redirect to="/login"></Redirect>
      )}
    </div>
  );
}
const mapStateToProps = state => ({
  login: state.auth
});

const mapDispatchToProps = dispatch => ({});

export default connect(mapStateToProps, mapDispatchToProps)(NewBlog);
