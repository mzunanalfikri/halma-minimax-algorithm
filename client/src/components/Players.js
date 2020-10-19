import React, { useState, useEffect } from 'react';
import './Board.css';

const Players = () => {
    const [P1, setP1] = useState("None");
    const [P2, setP2] = useState("None");

    const handleP1SelectChange = e => {
        const algP1 = e.target.value;
        setP1(algP1);
    }
    const handleP2SelectChange = e => {
        const algP2 = e.target.value;
        setP2(algP2);
    }
    return ( 
        <div className="row">
            <div className="column">
                <div>
                    Select Player A
                </div>
                <select value={P1} onChange={handleP1SelectChange}>
                    <option value="None">None</option>
                    <option value="Human">Human</option>
                    <option value="Minimax">Minimax</option>
                    <option value="Minimax with local search">Minimax with local search</option>
                </select>
                <div>
                    Player A: {P1}
                </div>
            </div>
            <div className="column">
                <div>
                    Select Player B
                </div>
                <select value={P2} onChange={handleP2SelectChange}>
                    <option value="None">None</option>
                    <option value="Human">Human</option>
                    <option value="Minimax">Minimax</option>
                    <option value="Minimax with local search">Minimax with local search</option>
                </select>
                <div>
                    Player B: {P2}
                </div>
            </div>
        </div>
    );
}

export default Players;