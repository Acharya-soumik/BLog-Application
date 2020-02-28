import React from "react";
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import Loader from "react-loader-spinner";

function Loading() {
  return (
    <div className="m-auto full-width">
      <h2 className="display-3 text-info mt-4">Loading...</h2>
      <Loader
        type="ThreeDots"
        color="#00BFFF"
        height={200}
        width={200}
        timeout={1000} //3 secs
      />
    </div>
  );
}

export default Loading;
