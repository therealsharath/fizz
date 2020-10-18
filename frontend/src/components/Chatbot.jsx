import React, { useState } from 'react';
import axios from 'axios';

import { useForm } from "react-hook-form";

function Chatbot(props) {
    const [messageBoard, setMessageBoard] = useState([])
    
    const sendMessage = (message) => {
        var data = JSON.stringify({
            "userId": props.user.uid,
            "userEmail" : props.user.email,
            "query": message,
        });
        var config = {
            method: 'post',
            url: 'http://maelstrom.pythonanywhere.com/chatbot/query',
            headers: { 
                'Content-Type': 'application/json'
        },
            data : data
        };
        axios(config)
        .then(function (response) {
            let newMessages = [...messageBoard];
            newMessages.push(message)
            newMessages.push(JSON.stringify(response.data.response))
            setMessageBoard(newMessages)
            console.log(JSON.stringify(response.data.response));
        })
        .catch(function (error) {
            console.log(error);
        });
    }

    const { register, handleSubmit, reset } = useForm();
    const onSubmit = (data) => {
        sendMessage(data.message);
        reset();
    }

    return(
        <div className="bot">
            {messageBoard !== [] && messageBoard.map((item) => <div>{item}</div>)}
            <form onSubmit={handleSubmit(onSubmit)}>
                <input name="message" ref={register} />
                <input type="submit" value="Send"/>
            </form>
        </div>
    )
}

export default Chatbot;

// <iframe
//                 className="chat-bot"
//                 allow="microphone;"
//                 src="https://console.dialogflow.com/api-client/demo/embedded/ec30069b-f075-4c81-9ca2-b07d7d47383a"
//             ></iframe>