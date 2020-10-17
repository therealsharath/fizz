import React, { useState } from 'react';
import Authentication from './Authentication.jsx';
import Chatbot from './Chatbot.jsx';

function Home() {
    const [isLogged, setIsLogged] = useState(false);

    return(
        <div>
            {!isLogged ? 
                <Authentication setIsLogged={setIsLogged}/> :
                <div>
                    <div className="navbar">
                        <div className="nav-wrapper">
                            <div className="logo">LO</div>
                            <a className="nav-link" href="#">ChatBot</a>
                            <a className="nav-link" href="#">About</a>
                            <a className="nav-link" href="#">Team</a>
                        </div>
                        <div className="sign-out-nav"><Authentication setIsLogged={setIsLogged}/></div>
                    </div>
                    <Chatbot/>
                </div>
            }
        </div>
    )
}

export default Home;
