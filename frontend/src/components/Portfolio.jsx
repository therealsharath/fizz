import React from 'react';
import { useState } from 'react';
import StockField from './StockField.jsx';
import axios from 'axios';

function Portfolio(props) {
    const [portfolio, setPortfolio] = useState(props.portfolio);

    const submitPortFolioHelper = () => {
        var data = JSON.stringify({
            "userId": props.user.uid,
            "userEmail" : props.user.email,
            "portfolio" : portfolio,
        });
        var config = {
            method: 'post',
            url: 'https://maelstrom.pythonanywhere.com/portfolio/upload',
            headers: { 
                'Content-Type': 'application/json'
        },
            data : data
        };
        axios(config)
        .then(function (response) {
            JSON.stringify(response.data.response);
        })
        .catch(function (error) {
            console.log(error);
        });
    }

    const submitPortFolio = () => {
        props.setPortfolio(portfolio);
        if(props.user) {
            console.log("Great Success")
            submitPortFolioHelper(portfolio);
        } else {
            console.log("oops")
        }
    }

    return(
        <div className="portfolio-container">
            <h1>Your Portfolio</h1>
            <div className="main-folio">
                {(portfolio.length >= 1) ? portfolio.map((item) => <div key={portfolio.indexOf(item)}>
                    {"Stock:" + item.ticker + "| Quantity: " + item.quantity + "| Purchase date: " + item.purchaseDate + "| Stop-loss/Downside put: " + item.slp}
                </div>) : <h2>Your portfolio is empty <span role="img" aria-label="cry">😭</span></h2>}
            </div>

            <div className="add-new">
                <h2>Add additional stocks</h2>
                <StockField portfolio={portfolio} setPortfolio={setPortfolio}/>
                <button onClick={submitPortFolio}>Submit Portfolio</button>
            </div>
        </div>
    )
}

export default Portfolio;