import React, { useState, useEffect } from 'react';
import DisplayBoard from './DisplayBoard';
import Players from './Players'

const Halma = () => {
    const [P1, setP1] = useState("None");
    const [P2, setP2] = useState("None");
    const [turn, setTurn] = useState(0);
    const [time, setTime] = useState(1);
    const [isStart, setIsStart] = useState(false);

    const [bSize, setBSize] = useState(0);
    const [board, setBoard] = useState([]);
    // const [seconds, setSeconds] = useState(10);

    // useEffect(() => {
    //     tick();
    // });

    // function tick() {
    //     if (seconds > 0) {
    //         setTimeout(() => setSeconds(seconds - 1), 1000);
    //     } else {
    //         setSeconds('TIME'S UP!');
    //     }
    // }

    const isInBaseA = (i, j, size) => {
        return i<size/2 && j<size/2 - i
    }

    const isInBaseB = (i, j, size) => {
        return i>=size/2 && j>=size*3/2 - 1 - i;
    }

    const handleReset = (size) => {
        setBoard([]);
        const arr = initBoard(size);
        setBoard(arr);

        setTurn(0);
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

        handleReset(size);
    }

    return ( 
        <div>
            <div>
                Halma
            </div>
            <input type="number" onChange={(e) => setTime(e.target.value)} value={time} />
            <Players 
                P1={P1}
                setP1={setP1}
                P2={P2}
                setP2={setP2}
                isStart={isStart}
                setIsStart={setIsStart}
                size={bSize}
                handleReset={handleReset}
            />
            <div>
                select board size
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
            {(board.length > 0 && isStart) && (
                <DisplayBoard board={board} size={bSize}
                P1={P1}
                P2={P2}
                time={time}
                turn={turn}
                setTurn={setTurn}
                setBoard={setBoard}
                isInBaseA={isInBaseA}
                isInBaseB={isInBaseB}
                />
            )}
            {/* <div>
                {seconds}
            </div> */}
        </div>
    );
}

export default Halma;