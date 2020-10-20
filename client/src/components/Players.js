import React from 'react';
import './Board.css';

const Players = ({ P1, setP1, P2, setP2, isStart, setIsStart, handleReset, size }) => {
    
    const handleP1SelectChange = e => {
        const algP1 = e.target.value;
        setP1(algP1);
    }
    const handleP2SelectChange = e => {
        const algP2 = e.target.value;
        setP2(algP2);
    }

    const handleBtnGame = () => {
        setIsStart(prev => !prev);
        handleReset(size);
    }

    return ( 
        <>
        <div className="row">
            <div className="column">
                <div>
                    Player 1
                </div>
                <select value={P1} onChange={handleP1SelectChange}>
                    <option value="None">None</option>
                    <option value="Human">Human</option>
                    <option value="Minimax">Minimax</option>
                    <option value="Minimax with local search">Minimax with local search</option>
                </select>
                <div>
                    Player 1: {P1}
                </div>
            </div>
            <div className="column">
                <div>
                    Player 2
                </div>
                <select value={P2} onChange={handleP2SelectChange}>
                    <option value="None">None</option>
                    <option value="Human">Human</option>
                    <option value="Minimax">Minimax</option>
                    <option value="Minimax with local search">Minimax with local search</option>
                </select>
                <div>
                    Player 2: {P2}
                </div>
            </div>
        </div>
        <div>
            <button onClick={handleBtnGame} className="btn" disabled={P1 === "None" || P2 === "None"}>
                <span>
                    {isStart ? "Reset" : "Start"}
                </span>
            </button>
        </div>
        </>
    );
}

export default Players;