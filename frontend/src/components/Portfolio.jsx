import React from 'react';
import { useState } from 'react';
import StockField from './StockField.jsx';
import PortfolioStock from './PortfolioStock.jsx'
import axios from 'axios';

function Portfolio(props) {
    const [portfolio, setPortfolio] = useState(props.portfolio);
    const [rows, setRows] = useState(props.rows)

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

    const createData = (name, quantity, purchaseDate, slp) => {
        return { name, quantity, purchaseDate, slp};
    }

    const submitPortFolio = (newPortfolio) => {
        if (newPortfolio) {
            let newRows = [...rows]
            let item = newPortfolio[newPortfolio.length - 1]
            item && newRows.push(createData(item.ticker, item.quantity, item.purchaseDate, item.slp));
            setRows(newRows);
            props.setRows(newRows);
            props.setPortfolio(newPortfolio);
            if(props.user) {
                submitPortFolioHelper(newPortfolio);
            }
        }
    }

    const deleteStock = (selected) => {
        if (selected && selected.length > 0) {
            let newRows = []
            let newPortfolio = []
            rows.forEach((item) => {
                if (selected.indexOf(item.name) < 0) {
                    newRows.push(createData(item.name, item.quantity, item.purchaseDate, item.slp))
                }
            })
            props.portfolio.forEach((item) => {
                if (selected.indexOf(item.ticker) < 0) {
                    newPortfolio.push(item)
                }
            })
            setRows(newRows);
            props.setRows(newRows);
            setPortfolio(newPortfolio);
            props.setPortfolio(newPortfolio);
            if(props.user) {
                submitPortFolioHelper(newPortfolio);
            }
        }
    }

    return(
        <div className="portfolio-container">
            <h1>Your Portfolio</h1>
            {
                (portfolio.length >= 1) ? 
                <PortfolioStock rows={rows} deleteStock={deleteStock}/> 
                : 
                <div className="main-folio"> <h2>Your portfolio is empty <span role="img" aria-label="cry">😭</span></h2> </div>
            }

            <div className="add-new">
                <h2>Add additional stocks</h2>
                <StockField portfolio={portfolio} setPortfolio={setPortfolio} submitPortfolio={submitPortFolio}/>
                <div className="buffer"/>
            </div>
        </div>
    )
}

export default Portfolio;