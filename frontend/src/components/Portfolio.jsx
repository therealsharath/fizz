import React from 'react';
import { useState } from 'react';
import StockField from './StockField.jsx';

function Portfolio() {
    const [stockNumber, setStockNumber] = useState(0)
    const [portfolio, setPortfolio] = useState([])

    return(
        <div>
            <StockField/>
        </div>
    )
}

export default Portfolio;