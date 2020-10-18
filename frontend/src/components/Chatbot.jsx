import React, { useState } from 'react';
import axios from 'axios';

import { useForm } from "react-hook-form";

import fizzlogo from './images/fizzlogo.png';

function Chatbot(props) {
    const [messageBoard, setMessageBoard] = useState([
        ['bot', 'Hey there! I’m Fizz, your personal financial consultant!'], 
        ['bot', 'I can help you with some of the following: analyzing your current portfolio, providing you with suggestions about the stocks you may want to transact, and even recommending potential assets to invest in!'],
        ['bot', 'Where would you like to start?'],
    ])
    
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
            newMessages.push(['user', message])
            if (JSON.stringify(response.data.response) != "") {
                newMessages.push(['bot', JSON.stringify(response.data.response)]);
            } else {
                newMessages.push(['bot', "I'm not sure what you mean?"]);
            }
            setMessageBoard(newMessages)
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
            <div>
            {messageBoard !== [] && messageBoard.map((item) => <div className={"container" + " " + item[0] + "-message"}>
                <img src={fizzlogo} alt="Avatar"/>
                <font className={item[0] + "-text"}>{item[1]}</font>
            </div>)}
            </div>
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