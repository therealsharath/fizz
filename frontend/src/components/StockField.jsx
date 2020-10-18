import React, { useState } from 'react';
import { useForm, Controller } from "react-hook-form";
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from "yup";

import ReactDatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const schema = yup.object().shape({
    ticker: yup.string().required(),
    quantity: yup.number().positive().integer().required(),
    slp: yup.number(),
});

function StockField(props) {
    const { register, handleSubmit, errors, reset, control } = useForm({
        resolver: yupResolver(schema)
    });

    const [selected, setSelected] = useState(new Date());

    const onSubmit = (data) => {
        reset();
        let newPortfolio = [...props.portfolio]
        data.date = data.date.toString()
        newPortfolio.push(data)
        console.log(newPortfolio);
        props.setPortfolio(newPortfolio)
    }

    return(
        <form className="new-stock" onSubmit={handleSubmit(onSubmit)}>
            <div className="form-item">
                <label className="label">Stock Ticker</label>
                <input id="ticker" name="ticker" type="text" ref={register} placeholder="Eg. AAPL"/>
            </div>

            <div className="form-item">
                <label className="label">Stock Quantity</label>
                <input name="quantity" type="text" ref={register} placeholder="Number of shares you own"/>
            </div>

            <div className="form-item">
                <label className="label">Date Purchased</label>
                <Controller
                    as={ReactDatePicker}
                    control={control}
                    valueName={selected.getDate()} // DateSelect value's name is selected
                    onChange={(chosen) => setSelected(chosen)}
                    name="date"
                    className="input"
                    placeholderText="Select date"
                    dateFormat="yyyy/MM/dd"
                    maxDate={new Date()}
                />
            </div>

            <div className="form-item">
                <label className="label">Stop-loss Point/Downside Put</label>
                <input name="slp" type="text" ref={register} placeholder="Eg. 5" defaultValue={0}/>
            </div>

            <div className="form-item">
                <label className="hide label"></label>
                <button className="form-button" type="submit" >Add Stock</button>
            </div>
        </form>
    )
}

export default StockField;