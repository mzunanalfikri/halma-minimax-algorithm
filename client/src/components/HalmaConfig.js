import React, { useState, useEffect } from 'react';
import {initBoard} from './HalmaService';

const HalmaConfig = ({ nextPage, bSize, time, setBSize, setTime, setBoard }) => {

    

    const handleSelectChange = e => {
        const size = e.target.value;
        setBSize(size);
        const arr = initBoard(size);
        setBoard(arr);
    }

    return ( 
        <>
            <div className="row">
                <div className="column">
                    <div>
                        T-Limit
                    </div>
                    <input type="number" onChange={(e) => setTime(e.target.value)} value={time} />
                </div>
                <div className="column">
                    <div>
                        Board Size
                    </div>
                    <select value={bSize} onChange={handleSelectChange}>
                        <option value="0"></option>
                        <option value="8">8</option>
                        <option value="10">10</option>
                        <option value="16">16</option>
                    </select>
                </div>
            </div>
            <div>
                <button onClick={nextPage} className="btn" >
                    <span>
                        Next
                    </span>
                </button>
            </div>
        </>
    );
}

export default HalmaConfig;