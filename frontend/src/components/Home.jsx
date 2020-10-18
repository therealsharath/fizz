import React, { useState } from 'react';
import Authentication from './Authentication.jsx';
import Chatbot from './Chatbot.jsx';
import Portfolio from './Portfolio.jsx';
import fizz from './images/fizzlogo.png';

function Home() {
    const [isLogged, setIsLogged] = useState(false);
    const [isUpload, setIsUpload] = useState(false);
    const [isStonks, setStonks] = useState(true);

    const [user, setUser] = useState(null);
    const [portfolio, setPortfolio] = useState([]);

    const handleUpload = () => {
        setIsUpload(true);
        setStonks(false);
    }

    const handleStonks = () => {
        setIsUpload(false);
        setStonks(true);
    }
    
    return(
        <div>
            {!isLogged ?
                <Authentication setIsLogged={setIsLogged} setUser={setUser}/> :
                <div>
                    <div className="navbar">
                        <div className="nav-wrapper">
                            <div className="logo"><img src={fizz} className="logo-image"></img></div>
                            <div className="nav-link" onClick={handleUpload}>Upload</div>
                            <div className="nav-link" onClick={handleStonks}>Stonks</div>
                        </div>
                        <div className="sign-out-nav"><Authentication setIsLogged={setIsLogged} setUser={setUser}/></div>
                    </div>
                    {isUpload && <Portfolio portfolio={portfolio} setPortfolio={setPortfolio}/>}
                    {isStonks && <Chatbot user={user}/>}
                </div>
            }
        </div>
    )
}

export default Home;
