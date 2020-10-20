import React, { useState, useEffect } from 'react';
import DisplayBoard from './DisplayBoard';
import { checkWinState } from './HalmaService';
import Players from './Players'
import HalmaConfig from './HalmaConfig';

const Halma = () => {
    const [win, setWin] = useState(0);
    const [P1, setP1] = useState("None");
    const [P2, setP2] = useState("None");
    const [turn, setTurn] = useState(0);
    const [time, setTime] = useState(5);

    const [bSize, setBSize] = useState(0);
    const [board, setBoard] = useState([]);
    const [page, setPage] = useState(1);
    

    const nextPage = () => {
        if (page === 3) {
            setPage(1);
            setBoard([]);
            setWin(0);
            setTurn(0);
            setBSize(0);
            setP1("None");
            setP2("None");
            setTime(5);
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
                    />
                }
            </div>
        </div>
    );
}

export default Halma;