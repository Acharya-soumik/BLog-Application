import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Card } from "antd";
import axios from "axios";
function Home(props) {
  const [blogs, setBlogs] = useState([]);
  const [comment, setComment] = useState("");
  const [allComments, setAllComments] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(setLoading(true));
    // setting blog
    axios.get("http://localhost:5000/blogs").then(res => setBlogs(res.data));
    axios
      .get("http://localhost:5000/comments")
      .then(res => setAllComments(res.data));
    setLoading(false);
  }, [loading]);
  console.log(props);
  const addComments = user => {
    setLoading(true);
    let obj = {
      comment: comment,
      user_id: user.user_id,
      catagory_id: user.catagory_id,
      blog_id: user.id
    };
    axios
      .post("http://localhost:5000/new_comment", obj)
      .then(res => setAllComments(res.data));
    setLoading(false);
  };
  if (loading == true) {
    return <h2>Loading...</h2>;
  } else {
    return (
      <div className="text-center m-auto">
        <h2>User Feed</h2>
        <div className="row">
          {blogs.map(ele => {
            return (
              <Card
                className="m-4"
                key={ele.id}
                style={{ width: 400 }}
                title={ele.name}
              >
                <h2>{ele.title}</h2>
                <Link
                  className="btn btn-dark"
                  to={{
                    pathname: `/users/${ele.blog_id}`,
                    state: {
                      data: ele
                    }
                  }}
                >
                  View More
                </Link>
                <hr />
                <small>Created At : {ele.created_at}</small>
              </Card>
            );
          })}
        </div>
      </div>
    );
  }
}

export default Home;
