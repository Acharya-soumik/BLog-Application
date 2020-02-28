import React, { useState } from "react";
import { Avatar } from "antd";
import { Upload, message, Icon } from "antd";
import axios from "axios";

function UserProfile() {
  const [img, setImg] = useState("");
  const { Dragger } = Upload;

  const data = {
    name: "picture",
    multiple: false,
    action: "http://127.0.0.1:5000/uploader",
    onChange(info) {
      const { status } = info.file;
      if (status === "done") {
        message.success(`${info.file.name} file uploaded successfully.`);
      } else if (status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
    }
  };
  return (
    <div className="m-auto text-center">
      <h2>Profile Settings</h2>
      <Avatar size={300} icon="user" />
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
