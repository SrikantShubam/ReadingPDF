// import "./App.css";
// import React, { useState } from "react";
// import axios from "axios";
// function App() {

//   const [file, setFile] = useState(null);
//   const [conversation, setConversation] = useState([]);
//   const [messageInput, setMessageInput] = useState("");


//   const handleFileUpload = (event) => {
//     const uploadedFile = event.target.files[0];
//     setFile(uploadedFile);
//   };

//   const handleConversationSubmit = async () => {
//     if (file) {
//       const formData = new FormData();
//       formData.append("pdfFile", file);

//       try {
//         const response = await axios.post(
//           "http://localhost:5000/process-pdf",
//           formData
//         );
//         const conversationData = response.data.conversation;
//         setConversation(conversationData);
//       } catch (error) {
//         // Handle any error that occurred during the API call
//         console.error(error);
//       }
//     }
//   };
// import "./App.css";
// import React, { useState } from "react";
// import axios from "axios";

// function App() {

//   const [file, setFile] = useState(null);
//   const [conversation, setConversation] = useState([]);
//   const [messageInput, setMessageInput] = useState("");

//   const handleFileUpload = (event) => {
//     const uploadedFile = event.target.files[0];
//     setFile(uploadedFile);
//   };

//   const handleConversationSubmit = async () => {
//     if (file) {
//       const formData = new FormData();
//       formData.append("pdfFile", file);

//       try {
//         const response = await axios.post(
//           "http://localhost:5000/process-pdf",
//           formData
//         );
//         const conversationData = response.data.conversation;
//         setConversation(conversationData);
//       } catch (error) {
//         console.error(error);
//       }
//     }
//   };

//   const handleMessageSubmit = async () => {
//     if (messageInput.trim() !== "") {
//       try {
//         const response = await axios.post(
//           "http://localhost:5000/send-message",
//           { message: messageInput },
//           {
//             headers: {
//               "Content-Type": "application/json",
//               Accept: "application/json",
//             },}
//         );
//         console.log(response.data)
//         const newMessage = response.data.message;
//         const updatedConversation = [...conversation, newMessage];
//         setConversation(updatedConversation);
//         setMessageInput("");
//       } catch (error) {
//         console.error(error);
//       }
//     }
//   };
import "./App.css";
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [conversation, setConversation] = useState([]);
  const [messageInput, setMessageInput] = useState("");

  const handleFileUpload = (event) => {
    const uploadedFile = event.target.files[0];
    setFile(uploadedFile);
  };

  const handleConversationSubmit = async () => {
    if (file) {
      const formData = new FormData();
      formData.append("pdfFile", file);

      try {
        const response = await axios.post(
          "http://localhost:5000/process-pdf",
          formData
        );
        const conversationData = response.data.conversation;
        setConversation(conversationData);
      } catch (error) {
        console.error(error);
      }
    }
  };

  const handleMessageSubmit = async () => {
    if (messageInput.trim() !== "") {
      try {
        const response = await axios.post(
          "http://localhost:5000/send-message",
          { message: messageInput },
          {
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json",
            },
          }
        );
        const newMessage = response.data.message;
        const updatedConversation = [...conversation, newMessage];
        setConversation(updatedConversation);
        setMessageInput("");
      } catch (error) {
        console.error(error);
      }
    }
  };
  return (
    <div className="container mt-5 text-center">
      <div className="d-block">
        <h1>PDF Chatbot: </h1>
        <h2 className="mt-3 mb-5">
          Instant Answers for Document and Book Queries
        </h2>
        <button className="btn ">
          {" "}
          <label for="files">Select file</label>
        </button>
        <input
          type="file"
          id="files"
          accept=".pdf"
          onChange={handleFileUpload}
          className="hidden"
        />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <button className="btn " onClick={handleConversationSubmit}>
          Submit
        </button>
      </div>
      <div className="conversation-box ">
        <div className="main">
          <div className="content">
            <div style={{ padding: "11px" }}>
              <p>Thur, May 26, 10:41 AM</p>

              {conversation.map((message, index) => (
                <div
                  key={index}
                  className={
                    message.role === "user"
                      ? "sender-msg msg-btn"
                      : "receiver-msg msg-btn"
                  }
                  style={{ marginTop: index !== 0 ? "2rem" : 0 }}
                >
                  {/* {message.role === 'user' ? null : <p>{message.role}</p>} */}
                  <p className="pb-2">{message.message}</p>
                </div>
              ))}
            </div>
          </div>

          {/* <div className="footer" style={{left:'100px'}}>
        <div >
          <input placeholder="Message" className="text-box" name="message" />
          <div class="send-ico">
            <i style={{position:'absolute'}} class="fas fa-paper-plane"></i>
          </div>

        </div>

      </div> */}
       <div class="footer">
    <div>
      <input id="message" placeholder="Message" class="text-box" name="message" value={messageInput}
                onChange={(event) => setMessageInput(event.target.value)}
 />
     
      <div class="send-ico " onClick={handleMessageSubmit}
                style={{ cursor: "pointer" }}>
        <i style={{position:'absolute'}} class="fas fa-paper-plane"></i>
      </div>
      
    </div>

  </div>
        </div>
      </div>
    </div>
  );
}

export default App;
