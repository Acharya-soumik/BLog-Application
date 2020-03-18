import React, { useState, useEffect } from "react";
import { Avatar } from "antd";
import { Upload, message, Icon } from "antd";
import axios from "axios";

function UserProfile() {
  const [img, setImg] = useState("");
  const { Dragger } = Upload;
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
        .then(res => setImg(res.data.image));
    }
    // GETTING USER
  }, []);
  const user_id = JSON.parse(window.localStorage.getItem("user_id"));
  const data = {
    name: "picture",
    userName: "soumik",
    multiple: false,
    action: "http://127.0.0.1:5000/uploader/" + user_id,
    onChange(info) {
      const { status } = info.file;
      if (status === "done") {
        message.success(`${info.file.name} file uploaded successfully.`);
        setImg(info.file.response.path);
      } else if (status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
    }
  };
  return (
    <div className="m-auto text-center">
      <h2>Profile Settings</h2>
      <img
        style={{
          height: 100,
          width: 100,
          borderRadius: 50
        }}
        src={img}
        alt="profile picture"
      />
      <hr />
      <div className="col-md-5 m-auto">
        <Dragger {...data}>
          <p className="ant-upload-drag-icon">
            <Icon type="inbox" />
          </p>
          <p className="ant-upload-text">
            Click or drag file to this area to upload
          </p>
          <p className="ant-upload-hint">
            Support for a single or bulk upload. Strictly prohibit from
            uploading company data or other band files
          </p>
        </Dragger>
      </div>
    </div>
  );
}

export default UserProfile;
