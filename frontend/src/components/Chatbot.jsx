import React from 'react';

function Chatbot() {
    return(
        <div className="bot">
            <iframe
                className="chat-bot"
                allow="microphone;"
                src="https://console.dialogflow.com/api-client/demo/embedded/ec30069b-f075-4c81-9ca2-b07d7d47383a"
            ></iframe>
        </div>
    )
}

export default Chatbot;