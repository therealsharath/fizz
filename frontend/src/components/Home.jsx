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
    const [messageBoard, setMessageBoard] = useState([
        ['bot', 'Hey there! I’m Fizz, your personal financial consultant!'], 
        ['bot', 'I can help you with some of the following: analyzing your current portfolio, providing you with suggestions about the stocks you may want to transact, and even recommending potential assets to invest in!'],
        ['bot', 'For example, get started by asking me "What is AMZN??!"'],
    ]);

    const [navClass, setNavClass] = useState("burger-container")
    const [navWrapperClass, setNavWrapperClass] = useState("nav-wrapper")

    const handlePortfolio = () => {
        setIsUpload(true);
        setStonks(false);
    }

    const handleFizz = () => {
        setIsUpload(false);
        setStonks(true);
    }
    
    const open = () => {
        navClass === "burger-container" ? setNavClass("change") : setNavClass("burger-container")
        navWrapperClass === "nav-wrapper" ? setNavWrapperClass("open-wrapper-class") : setNavWrapperClass("nav-wrapper")
    }

    const handleOpenFizz = () => {
        handleFizz();
        open();
    }

    const handleOpenPortfolio = () => {
        handlePortfolio();
        open();
    }

    return(
        <div className="home">
            {!isLogged ?
                <Authentication setIsLogged={setIsLogged} setUser={setUser}/> :
                <div>
                    <div className="navbar">
                        <img src={fizz} className="logo-image" alt="fizzLogo"></img>
                        <div className="nav-wrapper">
                            <div className="nav-link" onClick={handleFizz}>Fizz</div>
                            <div className="nav-link" onClick={handlePortfolio}>Portfolio</div>
                            <a className="nav-link" href="https://docs.google.com/document/d/1aeIvsM8bKKWKqaCXBCv7tIAwjWvPFJ6s40DcxDTlx7Q/" target="_blank" rel="noopener noreferrer">Docs</a>
                            <div className="nav-link" onClick={() => console.log(4)}>About Us</div>
                        </div>
                        <div className="sign-out-nav"><Authentication setIsLogged={setIsLogged} setUser={setUser}/></div>
                        <div className={navClass} onClick={open}>
                            <div className="bar1"></div>
                            <div className="bar2"></div>
                            <div className="bar3"></div>
                        </div>
                    </div>
                    <div className={navWrapperClass}>
                            <div className="open-nav-link" onClick={handleOpenFizz}>Fizz</div>
                            <div className="open-nav-link" onClick={handleOpenPortfolio}>Portfolio</div>
                            <a className="open-nav-link" href="https://docs.google.com/document/d/1aeIvsM8bKKWKqaCXBCv7tIAwjWvPFJ6s40DcxDTlx7Q/" target="_blank" rel="noopener noreferrer" onClick={open}>Docs</a>
                            <div className="open-nav-link" onClick={() => console.log(4)}>About Us</div>
                    </div>
                    {isUpload && <Portfolio user={user} portfolio={portfolio} setPortfolio={setPortfolio}/>}
                    {isStonks && <Chatbot user={user} messageBoard={messageBoard} setMessageBoard={setMessageBoard}/>}
                </div>
            }
        </div>
    )
}

export default Home;
