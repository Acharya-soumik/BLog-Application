import React, { useState, useEffect } from "react";
import axios from "axios";
import { Card, Icon, Avatar, Modal } from "antd";

function EditUserBlogs() {
  const [blogs, setBLogs] = useState([]);
  const [visible, setVisible] = useState(false);
  const [user_details, setUser] = useState({});
  const [input, setInput] = useState({
    title: "",
    content: ""
  });
  const [loading, setLoading] = useState(false);
  const { Meta } = Card;
  useEffect(() => {
    let user_id = localStorage.getItem("user_id");
    if (user_id) {
      axios
        .post("http://localhost:5000/user_blogs", {
          user_id: user_id
        })
        .then(res => setBLogs(res.data));
    }
  }, [loading]);

  const showModal = obj => {
    setUser(obj);
    setInput({ title: obj.title, content: obj.content });
    setVisible(true);
  };

  const handleOk = async obj => {
    let m_user = {
      ...user_details,
      title: input.title,
      content: input.content
    };
    setVisible(false);
    setLoading(true);
    await axios
      .post("http://127.0.0.1:5000/edit_post", m_user)
      .then(res => console.log(res));
    setLoading(false);
  };

  const handleCancel = e => {
    setVisible(false);
  };
  if (loading) {
    return <h2>Loading....</h2>;
  } else {
    return (
      <div className="text-center">
        <h2>User Blogs : </h2>
        {blogs.map(ele => {
          return (
            <>
              <Card
                style={{ width: 300 }}
                className="m-auto"
                cover={
                  <img
                    alt="example"
                    src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
                  />
                }
                actions={[
                  <Icon type="edit" key="edit" onClick={() => showModal(ele)} />
                ]}
              >
                <Meta
                  avatar={
                    <Avatar src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png" />
                  }
                  title={ele.title}
                  description={ele.content}
                />
                <Modal
                  title="Edit User Details"
                  visible={visible}
                  onOk={handleOk}
                  onCancel={handleCancel}
                >
                  <input
                    className="form-control"
                    onChange={e =>
                      setInput({ ...input, title: e.target.value })
                    }
                    value={input.title}
                  />
                  <input
                    className="form-control"
                    onChange={e =>
                      setInput({ ...input, content: e.target.value })
                    }
                    value={input.content}
                  />
                  <small>Craeted at: {ele.created_at}</small>
                </Modal>
              </Card>
            </>
          );
        })}
      </div>
    );
  }
}

export default EditUserBlogs;
