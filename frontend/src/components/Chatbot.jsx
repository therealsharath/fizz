import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

import { useForm } from "react-hook-form";

import fizzlogo from './images/fizzlogo.png';
import userpic from './images/stonksuser.png';

function Chatbot(props) {
    const [messageBoard, setMessageBoard] = useState([...props.messageBoard])
    
    const sendMessage = (message) => {
        if (message.length > 0) {
            var data = JSON.stringify({
                "userId": props.user.uid,
                "userEmail" : props.user.email,
                "query": message,
            });
            var config = {
                method: 'post',
                url: 'https://maelstrom.pythonanywhere.com/chatbot/query',
                headers: { 
                    'Content-Type': 'application/json'
            },
                data : data
            };
            axios(config)
            .then(function (response) {
                let newMessages = [...messageBoard];
                newMessages.push(['user', message])
                if (JSON.stringify(response.data.response) !== "") {
                    newMessages.push(['bot', JSON.stringify(response.data.response)]);
                } else {
                    newMessages.push(['bot', "I'm not sure what you mean?"]);
                }
                setMessageBoard(newMessages)
                props.setMessageBoard(newMessages)
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }

    const { register, handleSubmit, reset } = useForm();
    const onSubmit = (data) => {
        sendMessage(data.message);
        reset();
    }

    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(scrollToBottom, [messageBoard]);
    
    return(
        <div className="bot">
            <div className="message-container">
                <div className="message-board">
                    {messageBoard !== [] && messageBoard.map((item) => <div className={"container " + item[0] + "-message"} key={messageBoard.indexOf(item)}>
                        <img src={item[0] === 'bot' ? fizzlogo : userpic} alt="Avatar"/>
                        <font className={item[0] + "-text"}>{item[1]}</font>
                    </div>)}
                    <div ref={messagesEndRef} />
                </div>
                <form className="chat-form" onSubmit={handleSubmit(onSubmit)}>
                        <div className="chat-container">
                            <input className="chat-text" name="message" ref={register} />
                        </div>
                        <input className="chat-send" type="submit" value="🚀"/>
                </form>
            </div>
        </div>
    )
}

export default Chatbot;