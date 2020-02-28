import React, { useState } from "react";
import { Avatar } from "antd";

function UserProfile() {
  const [img, setImg] = useState("");
  console.log(img);
  return (
    <div className="m-auto text-center">
      <h2>Profile Settings</h2>
      <Avatar size={300} icon="user" />
    </div>
  );
}

export default UserProfile;
