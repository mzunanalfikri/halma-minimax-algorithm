import React, { useState, useEffect } from 'react';
import DisplayBoard from './DisplayBoard';
import Players from './Players'
import HalmaConfig from './HalmaConfig';

const Halma = () => {
    const [win, setWin] = useState(0);
    const [P1, setP1] = useState("None");
    const [P2, setP2] = useState("None");
    const [turn, setTurn] = useState(0);
    const [time, setTime] = useState(20);

    const [bSize, setBSize] = useState(0);
    const [board, setBoard] = useState([]);
    const [page, setPage] = useState(1);
    const [startTime, setStartTime] = useState(null);
    

    const nextPage = () => {
        if (page === 3) {
            setPage(1);
            setBoard([]);
            setWin(0);
            setTurn(0);
            setBSize(0);
            setP1("None");
            setP2("None");
            setTime(20);
        } else {
            setPage(page + 1);
        }
    }

    const previousPage = () => {
        setPage(page - 1);
    }



    return ( 
        <div>
            <br></br>
            <br></br>
            <div>
                Halma Bebek Goreng
            </div>
            <br></br>
            <br></br>
            <div>
                {page === 1 &&
                    <HalmaConfig
                        bSize={bSize}
                        time={time}
                        setBSize={setBSize}
                        setTime={setTime}
                        nextPage={nextPage}
                        setBoard={setBoard}
                    />
                }
                {page === 2 &&
                    <Players 
                        P1={P1}
                        setP1={setP1}
                        P2={P2}
                        setP2={setP2}
                        previousPage={previousPage}
                        nextPage={nextPage}
                        setStartTime={setStartTime}
                    />
                }
                {page === 3 &&
                    <DisplayBoard 
                        board={board} 
                        size={bSize}
                        P1={P1}
                        P2={P2}
                        time={time}
                        turn={turn}
                        setTurn={setTurn}
                        setBoard={setBoard}
                        win={win}
                        setWin={setWin}
                        nextPage={nextPage}
                        startTime={startTime}
                    />
                }
            </div>
        </div>
    );
}

export default Halma;