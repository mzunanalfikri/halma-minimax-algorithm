import React, { useState, useEffect } from 'react';
import './Board.css';

const DisplayBoard = ({ P1, P2, time, turn, setTurn, board, setBoard, size, isInBaseA, isInBaseB}) => {
    const [hasJump, setHasJump] = useState(false);
    const [clicked, setClicked] = useState({
        i: -1,
        j: -1
    });

    const [canMove, setCanMove] = useState([]);

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
        if(hasJump){
            return generateActionJump(x, y);
        }else{
            var listOfValidAction = generateActionBasic(x, y);
            return listOfValidAction.concat(generateActionJump(x, y));
        }
    }

    // TODO : pake dari backend
    const generateActionBasic = (x, y) => {
        var listOfValidAction = [];
        for(var i=x-1; i<x+2; i++){
            if(i>=0 && i<size){
                for(var j=y-1; j<y+2; j++){
                    if(j>=0 && j<size){
                        if(board[i][j] === 0){
                            listOfValidAction.push({
                                i,
                                j,
                                hasJump : false
                            });
                        }
                    }
                }
            }
        }

        return listOfValidAction;
    }


    // TODO : pake dari backend
    const generateActionJump = (x, y) => {
        var listOfValidAction = [];
        for(var i=x-1; i<x+2; i++){
            const dif_i = i - x;

            if(i>=0 && i<size){
                for(var j=y-1; j<y+2; j++){
                    if(j>=0 && j<size){
                        const dif_j = j - y;
                        const jump_i = i + dif_i;
                        const jump_j = j + dif_j;
                        if(jump_i >= 0 && jump_i < size && jump_j >= 0 && jump_j < size){
                            if(board[jump_i][jump_j] === 0 && board[i][j] !== 0)
                            listOfValidAction.push({
                                i: jump_i,
                                j: jump_j,
                                hasJump : true
                            });
                        }
                    }
                }
            }
        }
        
        return listOfValidAction;
    }

    const handleClick = (i,j) => {
        if(clicked.i === i && clicked.j === j){ //cancel click
            setClicked({
                i: -1,
                j: -1
            });
            setCanMove([]);
        }else{
            if(clicked.i === -1 && clicked.j === -1){ //not clicked yet
                if(board[i][j] === turn%2 + 1){ // click pion player sesuai turn
                    setClicked({
                        i,
                        j
                    });
    
                    setCanMove(generateValidAction(i, j));
                }
            }else{ // already clicked

                // TODO : cek valid move
                var isCanMove = checkCanMove(i, j);
                if(isCanMove.found){
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
                    }else{
                        changeTurn();
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

    const changeTurn = () => setTurn(turn => turn + 1);

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
                {turn%2 === 0 ? "Player A's Turn" : "Player B's Turn"}
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