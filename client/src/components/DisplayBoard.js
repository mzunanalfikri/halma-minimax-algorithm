import React, { useState } from 'react';
import './Board.css';

const DisplayBoard = ({ board, setBoard, size, isInBaseA, isInBaseB}) => {
    const [clicked, setClicked] = useState({
        i: -1,
        j: -1
    });

    const handleClick = (i,j) => {
        if(clicked.i === i && clicked.j === j){ //cancel click
            setClicked({
                i: -1,
                j: -1
            });
        }else{
            if(clicked.i === -1 && clicked.j === -1){ //not clicked yet
                setClicked({
                    i,
                    j
                })
            }else{ // already clicked

                // TODO : cek valid move
                handleMove({
                    i: clicked.i,
                    j: clicked.j
                }, {
                    i,
                    j
                })
            }
        }
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
            {boardComponent}
        </div>
    );
}

export default DisplayBoard;