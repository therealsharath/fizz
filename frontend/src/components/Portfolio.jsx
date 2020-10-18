import React from 'react';
import { useState } from 'react';
import StockField from './StockField.jsx';
import axios from 'axios';

function Portfolio(props) {
    const [portfolio, setPortfolio] = useState(props.portfolio);

    const submitPortFolioHelper = () => {
        var data = JSON.stringify({
            "userId": "HuXTITuGVlXZmwNsyNZlNIsjDky1",
            "userEmail" : "sharathbabu16@gmail.com",
            "portfolio" : portfolio,
        });
        var config = {
            method: 'post',
            url: 'http://maelstrom.pythonanywhere.com/portfolio/upload',
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
        submitPortFolioHelper(portfolio);
    }

    return(
        <div>
            {portfolio !== [] && portfolio.map((item) => <div>
                {item.ticker + "," + item.quantity + "," + item.date.toString() + "," + item.spl}
            </div>)}
            <StockField portfolio={portfolio} setPortfolio={setPortfolio}/>
            <button onClick={submitPortFolio}>Submit Portfolio</button>
        </div>
    )
}

export default Portfolio;