import React, { useState } from 'react';
import DisplayBoard from './DisplayBoard';

const Halma = () => {
    const [bSize, setBSize] = useState(0);
    const [board, setBoard] = useState([]);

    const isInBaseA = (i, j, size) => {
        return i<size/2 && j<size/2 - i
    }

    const isInBaseB = (i, j, size) => {
        return i>=size/2 && j>=size*3/2 - 1 - i;
    }

    const initBoard = (size) => {
        var arr = [];

        for(var i=0;i<size;i++){
            var rows = [];
            for(var j=0;j<size;j++){
                if(isInBaseA(i, j, size)){
                    rows.push(1);
                }else if(isInBaseB(i, j, size)){
                    rows.push(2);
                }else{
                    rows.push(0);
                }
            }
            arr.push(rows);
        }

        return arr;
    }

    const handleSelectChange = e => {
        const size = e.target.value;
        setBSize(size);
        
        const arr = initBoard(size);
        setBoard(arr);
    }

    return ( 
        <div>
            <div>
                Halma
            </div>
            <select value={bSize} onChange={handleSelectChange}>
                <option value="0"></option>
                <option value="8">8</option>
                <option value="10">10</option>
                <option value="16">16</option>
            </select>
            <div>
                {bSize}
            </div>
            {board.length > 0 && (
                <DisplayBoard board={board} size={bSize}
                setBoard={setBoard}
                isInBaseA={isInBaseA}
                isInBaseB={isInBaseB}
                />
            )}
        </div>
    );
}

export default Halma;