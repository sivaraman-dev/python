document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const statusText = document.getElementById('status');
    const resetBtn = document.getElementById('reset-btn');
    const modalResetBtn = document.getElementById('modal-reset-btn');
    const modal = document.getElementById('winner-modal');
    const winnerText = document.getElementById('winner-text');

    let isProcessing = false;

    // Fetch the initial game state from python API
    async function fetchState() {
        try {
            const response = await fetch('/api/state');
            const data = await response.json();
            updateBoard(data);
        } catch (error) {
            console.error("Error fetching state:", error);
            statusText.innerText = "Error connecting to server";
            statusText.style.color = "red";
        }
    }

    function updateBoard(state) {
        state.board.forEach((val, index) => {
            const cell = cells[index];
            if (val !== " ") {
                if (!cell.classList.contains('filled')) {
                    cell.innerText = val;
                    cell.classList.add('filled', val.toLowerCase());
                }
            } else {
                cell.innerText = "";
                cell.className = "cell"; // Reset to default class
            }
        });

        if (state.game_over) {
            let winClass = '';
            if (state.winner === 'X') {
                winnerText.innerText = 'PLAYER X WINS!';
                winClass = 'win-x';
            } else if (state.winner === 'O') {
                winnerText.innerText = 'PLAYER O WINS!';
                winClass = 'win-o';
            } else {
                winnerText.innerText = "IT'S A DRAW!";
                winClass = 'draw';
            }
            
            winnerText.className = winClass;
            modal.classList.remove('hidden');
        } else {
            modal.classList.add('hidden');
            statusText.innerText = `Player ${state.current_turn}'s Turn`;
            statusText.className = state.current_turn === 'X' ? 'status-x' : 'status-o';
        }
        
        isProcessing = false;
    }

    async function makeMove(index) {
        if (isProcessing) return;
        isProcessing = true;
        
        try {
            const response = await fetch('/api/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ index })
            });
            const data = await response.json();
            updateBoard(data);
        } catch (error) {
            console.error("Error making move:", error);
            isProcessing = false;
        }
    }

    async function resetGame() {
        if (isProcessing) return;
        isProcessing = true;
        
        try {
            const response = await fetch('/api/reset', { method: 'POST' });
            const data = await response.json();
            updateBoard(data);
        } catch (error) {
            console.error("Error resetting game:", error);
            isProcessing = false;
        }
    }

    // Attach click events to grid cells
    cells.forEach(cell => {
        cell.addEventListener('click', () => {
            if (!cell.classList.contains('filled')) {
                const index = parseInt(cell.getAttribute('data-index'));
                makeMove(index);
            }
        });
    });

    // Attach reset buttons
    resetBtn.addEventListener('click', resetGame);
    modalResetBtn.addEventListener('click', resetGame);

    // Initial setup
    fetchState();
});
