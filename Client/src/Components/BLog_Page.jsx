import React, { useEffect, useState } from "react";
import axios from "axios";
import { Comment, Icon, Tooltip, Avatar, Collapse } from "antd";

function BLog_Page(props) {
  const { Panel } = Collapse;

  function callback(key) {}
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState({});
  const [comment, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  useEffect(() => {
    setLoading(true);
    setUser(props.location.state.data);
    let b_id = parseInt(props.match.params.id);

    axios
      .post("http://localhost:5000/comments", {
        b_id
      })
      .then(res => setComments(res.data));
    setLoading(false);
  }, [loading]);

  const clickHandler = () => {
    let b_id = props.match.params.id;
    let data = {
      comment: newComment,
      user_id: user.user_id,
      blog_id: parseInt(b_id),
      catagory_id: user.catagory_id
    };
    console.log(data);
    setLoading(true);
    axios
      .post("http://localhost:5000/new_comment", data)
      .then(res => setComments(res.data));

    setLoading(false);
  };
  console.log(comment);

  if (loading) {
    return <h2>Loading...</h2>;
  } else {
    return (
      <div className="text-center  p-4">
        <div className="card m-auto col-md-6 rounded p-4">
          <h2 className="text-light bg-dark p-4 rounded">{user.title}</h2>
          <p className="text-light bg-dark p-4 rounded ">{user.content}</p>
          <Collapse defaultActiveKey={user.id}>
            <Panel header="comment box" key={user.id}>
              <div className="row text-center">
                <input
                  className=" m-auto col-md-6 form-control"
                  placeholder="add a new comment"
                  onChange={e => setNewComment(e.target.value)}
                />
                <button
                  className="btn btn-outline-dark m-auto"
                  onClick={clickHandler}
                >
                  Add
                </button>
              </div>
              {comment.map(ele => (
                <Comment
                  author={<a>User</a>}
                  avatar={
                    <Avatar
                      src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                      alt="Han Solo"
                    />
                  }
                  content={<p>{ele.comment}</p>}
                  datetime={
                    <Tooltip title={ele.created_at}>
                      <p>Posted few minutes ago...</p>
                    </Tooltip>
                  }
                />
              ))}
            </Panel>
          </Collapse>
        </div>
      </div>
    );
  }
}

export default BLog_Page;
