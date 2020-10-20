import React, { useState, useEffect } from 'react';
import {generateActionBasic, generateActionJump, checkWinState} from './HalmaService';
import './Board.css';

const DisplayBoard = ({ P1, P2, time, turn, setTurn, board, setBoard, size, isInBaseA, isInBaseB, win, setWin}) => {
    const [hasJump, setHasJump] = useState(false);
    const [hasStep, setHasStep] = useState(false);
    const [currPos, setCurrPos] = useState({
        i: -1,
        j: -1
    });
    const [clicked, setClicked] = useState({
        i: -1,
        j: -1
    });

    const [canMove, setCanMove] = useState([]);

    useEffect(() => {
        const winCondition = checkWinState(board, size);
        console.log(winCondition);
        if(winCondition !== 0){
            setWin(winCondition);
        }
    }, [board]);

    useEffect( () => {
        const getMinimax = async () => {
            const params = {
                state : board,
                player : turn%2 + 1,
                timelimit : time
            }
            const res = await fetch('/best-decision-minimax', {
                method: 'POST',
                headers : {
                    'Content-Type' : 'application/json'
                },
                body: JSON.stringify(params)
            }).then(response => response.json());
            const minimax = res;
            console.log(minimax);
            setBoard(minimax.next_state);
            changeTurn();
        }

        const getMinimaxLocalSearch = async () => {
            const params = {
                state : board,
                player : turn%2 + 1,
                timelimit : time
            }
            const res = await fetch('/minimax-local', {
                method: 'POST',
                headers : {
                    'Content-Type' : 'application/json'
                },
                body: JSON.stringify(params)
            }).then(response => response.json());

            const minimax = res;
            console.log(minimax);
            setBoard(minimax.next_state);
            changeTurn();
        }

        if(turn === 0){
            if(P1 === "Minimax"){
                getMinimax();
            }else if(P1 === "Minimax with local search"){
                getMinimaxLocalSearch();
            }
        }else{
            if(turn%2 === 0){
                if(P1 === "Minimax"){
                    getMinimax();
                }else if(P1 === "Minimax with local search"){
                    getMinimaxLocalSearch();
                }
            }else{
                if(P2 === "Minimax"){
                    getMinimax();
                }else if(P2 === "Minimax with local search"){
                    getMinimaxLocalSearch();
                }
            }
        }
        console.log('yee turn ganti');
    }, [turn]);

    // TODO : nanti ganti pake yang dari backend
    // bikin lagi cuma buat testing
    const generateValidAction = (x, y) => {
        if (hasStep) {
            return [];
        }
        if(hasJump){
            return generateActionJump(x, y, board, size);
        }else{
            var listOfValidAction = generateActionBasic(x, y, board, size);
            return listOfValidAction.concat(generateActionJump(x, y, board, size));
        }
    }

    const handleClick = (i,j) => {
        // console.log(currPos.i);
        // console.log(currPos.j);
        // console.log("clicked");
        // console.log(clicked.i);
        // console.log(clicked.j);
        if(clicked.i === i && clicked.j === j){ //cancel click
            setClicked({
                i: -1,
                j: -1
            });
            // setCurrPos({
            //     i: -1,
            //     j: -1
            // });
            setCanMove([]);
        }else{
            if(clicked.i === -1 && clicked.j === -1){ //not clicked yet
                if(board[i][j] === turn%2 + 1){ // click pion player sesuai turn
                    if (((i === currPos.i && j === currPos.j) && hasJump) || !hasJump) {
                        setClicked({
                            i,
                            j
                        });
                        setCanMove(generateValidAction(i, j));
                    }
    
                }
            }else{ // already clicked
                setCurrPos({
                    i,
                    j
                });
                // TODO : cek valid move
                var isCanMove = checkCanMove(i, j);
                if(isCanMove.found){
                    for(var a=clicked.i-1; a<clicked.i+2; a++){
                        if(a>=0 && a<size){
                            for(var b=clicked.j-1; b<clicked.j+2; b++){
                                if(b>=0 && b<size){
                                    if(board[a][b] === 0){
                                        if (i === a && j === b) {
                                            setHasStep(true);
                                        }
                                    }
                                }
                            }
                        }
                    }
                    handleMove({
                        i: clicked.i,
                        j: clicked.j
                    }, {
                        i,
                        j
                    });
                    
                    setCanMove([]);
                    if(isCanMove.hasJump){ 
                        setHasJump(true);
                    }
                }
            }
        }
    }

    const checkCanMove = (x, y) => {
        for(var it=0; it<canMove.length; it++){
            if(canMove[it].i === x && canMove[it].j === y){
                return {
                    found: true,
                    hasJump: canMove[it].hasJump
                }
            }
        }
        return {
            found: false,
            hasJump: false
        };
    }

    const handleMove = (before, after) => {
        setBoard(board => {
            board[after.i][after.j] = board[before.i][before.j];
            board[before.i][before.j] = 0;
            return board;
        })
        setClicked({
            i: -1,
            j: -1
        });
    }

    const changeTurn = () => {
        console.log(win);
        if(win === 0){
            setTurn(turn => turn + 1);
            setHasJump(false);
            setHasStep(false);
            setCurrPos({
                i: -1,
                j: -1
            });
            setClicked({
                i: -1,
                j: -1
            });
        }
        
    };

    const boardComponent = board.map((row, i) => {
        const cells = row.map((cell, j) => {
            var styles = "cell-board ";
            if(isInBaseA(i, j, size)){
                styles = styles + "green ";
            }else if(isInBaseB(i, j, size)){
                styles = styles + "red ";
            }else{
                styles = styles + "blank ";
                if(cell === 1){
                    styles = styles + "player-A ";
                }
                if(cell === 2){
                    styles = styles + "player-B ";
                }
            }
            if(checkCanMove(i, j).found){
                styles = styles + "can-move ";
            }

            styles = (clicked.i === i && clicked.j === j) ? styles+ "cell-clicked" : styles; 
            return (
                <span onClick={() => handleClick(i,j)} className={styles} key={j}>
                    <div>
                        {cell !== 0 ? cell : "0"}
                    </div>
                </span>
            );
        });

        return (
            <div key={i}>
                {cells}
            </div>
        );
    })

    return ( 
        <div className="board-container">
            <div>
                {(turn%2 === 0 && win === 0) ? "Player 1's Turn" : 
                (win === 0) ? "Player 2's Turn" : ""}
                {(win === 1) ? "Player 1 Win" : 
                (win === 2) ? "Player 2 Win" : ""}
            </div>
            {boardComponent}
            <button onClick={changeTurn} className="btn">
                <span>
                    Next
                </span>
            </button>
        </div>
    );
}

export default DisplayBoard;