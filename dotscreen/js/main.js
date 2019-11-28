/*----- constants -----*/
const winningCombos = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
    ];

/*----- app's state (variables) -----*/

let board;
let turn = 'X';
let win;
let vic_o = 0;
let vic_x = 0;

/*----- cached element references -----*/

const squares = Array.from(document.querySelectorAll('#board div'));

/*----- event listeners -----*/
document.getElementById('board').addEventListener('click', handleTurn);
const messages = document.querySelector('h2');
const recap = document.querySelector('h3');
document.getElementById('reset-button').addEventListener('click', init);


/*----- functions -----*/

function getWinner() {
    let winner = null;
    winningCombos.forEach(function(combo, index) {
        if (board[combo[0]] && board[combo[0]] === board[combo[1]] && board[combo[0]] === board[combo[2]]) winner = board[combo[0]];
        });
		if (winner === 'X')
			vic_x = vic_x + 1;
		if (winner === 'O')
			vic_o = vic_o + 1;
        return winner ? winner : board.includes('') ? null : 'T';
};

function handleTurn() {
    let idx = squares.findIndex(function(square) {
        return square === event.target;
    });
	if (board[idx] === '')
	{
	    board[idx] = turn;
	    turn = turn === 'X' ? 'O' : 'X';
	    win = getWinner();
	    render();
		if (win != null)
			init()
	}
};

function init() {
    board = [
    '', '', '',
    '', '', '',
    '', '', ''
    ];
    render();
};

function render() {
    board.forEach(function(mark, index) {
    //this moves the value of the board item into the squares[idx]
    squares[index].textContent = mark;
    });
	messages.textContent = win === 'T' ? `That's a tie, queen!` : win ? `${win} wins the game!` : `It's ${turn}'s turn!`;
	if (turn === 'O')
	{
		recap.setAttribute('style', 'white-space: pre;');
		recap.textContent =  `→ O: ${vic_o}\n`;
		recap.textContent += `     X: ${vic_x}`;
	}
	else
	{
		recap.setAttribute('style', 'white-space: pre;');
		recap.textContent =  `     O: ${vic_o}\n`;
		recap.textContent += `→ X: ${vic_x}`;
	}
};

init();
