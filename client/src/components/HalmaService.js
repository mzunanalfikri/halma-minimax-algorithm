// TODO : pake dari backend
export function generateActionBasic(x, y, board, size){
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
    // const res = await fetch('possible-one-move-jump', {
    //     method: 'POST',
    //     headers : {
    //         'Content-Type' : 'application/json'
    //     },
    //     body : {
    //         state: board,
    //         position: [x,y]
    //     }
    // }).then(response => response.json());
    // res.map(pos => {
    //     return {
    //         i: pos[0],
    //         j: pos[1],
    //         hasJump: false
    //     };
    // });
    

    return listOfValidAction;
}

// TODO : pake dari backend
export function generateActionJump(x, y, board, size) {
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

export function checkWinState(board, size){
    
    let pion1 = []
    let pion2 = []
    for(var i=0; i<size; i++){
        for(var j=0;j<size;j++){
            if(board[i][j] === 1){
                pion1.append({
                    x: i,
                    y: j
                });
            }else if(board[i][j] === 2){
                pion2.append({
                    x: i,
                    y: j
                });
            }
        }
    }

    let win1 = true;
    let win2 = true;
    for(var i=0;i<pion1.length;i++){
        if(pion1[i].x + pion1[i].y < size*3/2 - 1){
            win1= false;
        }
    }
    for(var i=0;i<pion2.length;i++){
        if(pion2[i].x + pion2[i].y > size/2 - 1){
            win2= false;
        }
    }

    if(win1){
        return 1;
    }else if(win2){
        return 2;
    }else{
        return 0;
    }
}