import React, { useState } from 'react';
import Authentication from './Authentication.jsx';
import Chatbot from './Chatbot.jsx';
import Portfolio from './Portfolio.jsx';

function Home() {
    const [isLogged, setIsLogged] = useState(false);
    const [isUpload, setIsUpload] = useState(false);
    const [isStonks, setStonks] = useState(true);
    const [isAbout, setIsAbout] = useState(false);

    const handleUpload = () => {
        setIsUpload(true);
        setStonks(false);
        setIsAbout(false);
    }

    const handleStonks = () => {
        setIsUpload(false);
        setStonks(true);
        setIsAbout(false);
    }

    const handleAbout = () => {
        setIsUpload(false);
        setStonks(false);
        setIsAbout(true);
    }
    
    return(
        <div>
            {!isLogged ? 
                <Authentication setIsLogged={setIsLogged}/> :
                <div>
                    <div className="navbar">
                        <div className="nav-wrapper">
                            <div className="logo">LO</div>
                            <div className="nav-link" onClick={handleUpload}>Upload</div>
                            <div className="nav-link" onClick={handleStonks}>Stonks</div>
                            <div className="nav-link" onClick={handleUpload}>About</div>
                        </div>
                        <div className="sign-out-nav"><Authentication setIsLogged={setIsLogged}/></div>
                    </div>
                    {isUpload && <Portfolio/>}
                    {isStonks && <Chatbot/>}
                </div>
            }
        </div>
    )
}

export default Home;
