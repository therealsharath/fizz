import React, { useState } from 'react';
import { useForm, Controller } from "react-hook-form";

import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const defaultValues = {
    Native: ""
};

function StockField(props) {
    const { register, handleSubmit, reset, control, errors } = useForm({defaultValues});
    const [selectedDate, setselectedDate] = useState(null);

    const onSubmit = (data) => {
        reset();
        let newPortfolio = [...props.portfolio];
        data.purchaseDate = data.purchaseDate.getDate()+"/"+data.purchaseDate.getMonth()+"/"+data.purchaseDate.getFullYear();
        newPortfolio.push(data);
        props.setPortfolio(newPortfolio);
        props.submitPortfolio(newPortfolio);
    }

    return(
        <form className="new-stock" onSubmit={handleSubmit(onSubmit)}>
            <div className="form-item">
                <label className="label">Stock Ticker</label>
                <input name="ticker" type="text" ref={register({ required: true })} placeholder="Eg. AAPL"/>
                {errors.ticker && <span className="err">This field is required</span>}
            </div>

            <div className="form-item">
                <label className="label">Stock Quantity</label>
                <input name="quantity" type="text" ref={register({ required: true })} placeholder="Number of shares you own"/>
                {errors.quantity && <span className="err">This field is required</span>}
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
                    rules={{ required: true }}
                    defaultValue={null}
                    maxDate={new Date()}
                />
                {errors.purchaseDate && <span className="err">This field is required</span>}
            </section>

            <div className="form-item">
                <label className="label">Stop-loss/Downside (Optional)</label>
                <input name="slp" type="text" ref={register} placeholder="Eg. 5" defaultValue={0}/>
            </div>

            <div className="form-item">
                <label className="hide label">&nbsp;</label>
                <button type="submit" >Add Stock</button>
            </div>
        </form>
    )
}

export default StockField;