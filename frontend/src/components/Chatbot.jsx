import React from 'react';
import { useForm } from "react-hook-form";

function Chatbot() {
    const { register, handleSubmit, watch, errors } = useForm();
    const onSubmit = data => console.log(data.message);

    return(
        // <div className="bot">
        //     <div className="bot-container">
        //         <div className="chat">WTF</div>
        //     </div>
        //     <form onSubmit={handleSubmit(onSubmit)}>
        //         {/* register your input into the hook by invoking the "register" function */}
        //         <input name="message" defaultValue="test" ref={register} />
            
        //         {/* errors will return when field validation fails  */}
        //         {errors.exampleRequired && <span>This field is required</span>}
        //         <input type="submit" />
        //     </form>
        // </div>
        <iframe
            allow="microphone;"
            width="350"
            height="430"
            src="https://console.dialogflow.com/api-client/demo/embedded/ec30069b-f075-4c81-9ca2-b07d7d47383a">
        </iframe>
    )
}

export default Chatbot;