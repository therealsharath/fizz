import React, { useState } from 'react';
import { useForm, Controller } from "react-hook-form";

import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const defaultValues = {
    Native: ""
};

function StockField(props) {
    const { register, handleSubmit, reset, control } = useForm({defaultValues});
    const [selectedDate, setselectedDate] = useState(null);

    const onSubmit = (data) => {
        reset();
        let newPortfolio = [...props.portfolio]
        data.purchaseDate = data.purchaseDate.getDate()+"/"+data.purchaseDate.getMonth()+"/"+data.purchaseDate.getFullYear()
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

            <section className="form-item">
                <label className="label">Date Purchased</label>
                <Controller
                    as={DatePicker}
                    control={control}
                    valueName="selected"
                    selected={selectedDate}
                    onChange={([selected]) => {
                        setselectedDate(selected);
                        return selected;
                    }}
                    dateFormat="dd/MM/yyyy"
                    placeholderText="Select Date"
                    name="purchaseDate"
                    defaultValue={null}
                    maxDate={new Date()}
                />
            </section>

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