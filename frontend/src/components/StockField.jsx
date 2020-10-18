import React from 'react';
import { useForm } from "react-hook-form";

function StockField() {
    const { register, handleSubmit, watch, errors } = useForm();
    const onSubmit = data => console.log(data);

    return(
        <form onSubmit={handleSubmit(onSubmit)}>
            <input name="ticker" ref={register({ required: true })}/>
            {errors.ticker && <span>This field is required</span>}
            <input name="quantity" ref={register({ required: true })} />
            {errors.quantity && <span>This field is required</span>}
            <input name="date" ref={register({ required: true })} />
            {errors.date && <span>This field is required</span>}
            <input type="submit" />
        </form>
    )
}

export default StockField;