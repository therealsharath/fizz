import React from 'react';
import { useState } from 'react';
import StockField from './StockField.jsx';

function Portfolio(props) {
    const [portfolio, setPortfolio] = useState(props.portfolio);

    const submitPortFolio = () => {
        props.setPortfolio(portfolio);
        console.log(portfolio)
    }

    return(
        <div>
            {portfolio !== [] && portfolio.map((item) => <div>{item.ticker}</div>)}
            <StockField portfolio={portfolio} setPortfolio={setPortfolio}/>
            <button onClick={submitPortFolio}>Submit Portfolio</button>
        </div>
    )
}

export default Portfolio;