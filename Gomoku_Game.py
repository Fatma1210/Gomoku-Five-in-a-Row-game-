import numpy as np

# Direction arrays as NumPy arrays
dx = np.array([1, 0, 1, 1, -1, -1, -1, 0], dtype=np.int8)
dy = np.array([0, 1, -1, 1, -1, 0, 1, -1], dtype=np.int8)

# Create a board of size N x M
N = 15
M = 15

def CreateBoard():
    board = np.full((N, M), '.', dtype=str)
    return board

def isValid(x, y):
    return 0 <= x < N and 0 <= y < M

def GetValidMoves(board, movesplayed, radius=4):
    validMoves = set()
    for x, y in movesplayed:
        for i in range(8):
            for j in range(1, radius + 1):
                nx, ny = x + dx[i] * j, y + dy[i] * j
                if isValid(nx, ny) and board[nx][ny] == '.':
                    validMoves.add((nx, ny))
    return list(validMoves)

def applyMove(board, move, player, movesplayed):
    x, y = move
    new_board = board.copy()
    new_board[x][y] = player
    newMovesplayed = movesplayed + [move]
    return new_board, newMovesplayed



def CountConsecutive(board, x, y, dx, dy, player):
    count = 1
    n = board.shape[0]

    # Check forward
    i = 1
    while True:
        nx, ny = x + dx * i, y + dy * i
        if isValid(nx, ny) and board[nx][ny] == player:
            count += 1
            i += 1
        else:
            break

    # Check backward
    i = 1
    while True:
        nx, ny = x - dx * i, y - dy * i
        if isValid(nx, ny) and board[nx][ny] == player:
            count += 1
            i += 1
        else:
            break

    return count


def EvaluateHeuristic(board, player):
    opponent = 'O' if player == 'X' else 'X'
    score = 0

    values = {
        5: 100000,
        4: 10000,
        3: 1000,
        2: 100,
    }

    for x in range(N):
        for y in range(M):
            for i in range(4):  
                for current_player, sign in [(player, 1), (opponent, -1)]:
                    count = 0
                    open_ends = 0

                    # Check backward
                    nx, ny = x - dx[i], y - dy[i]
                    if isValid(nx, ny) and board[nx][ny] == '.':
                        open_ends += 1

                    for j in range(5):
                        nx, ny = x + dx[i] * j, y + dy[i] * j
                        if isValid(nx, ny):
                            if board[nx][ny] == current_player:
                                count += 1
                            elif board[nx][ny] == '.':
                                open_ends += 1
                                break
                            else:
                                break
                        else:
                            break

                    if count in values:
                        multiplier = 1.5 if open_ends == 2 else 1.0 if open_ends == 1 else 0
                        score += sign * values[count] * multiplier
                    if current_player == opponent and count == 4 and open_ends >= 1:
                        score -= 50000  # Increase penalty

    return score

def Minimax(board, depth, maximizingPlayer, player, movesplayed):
    opponent = 'O' if player == 'X' else 'X'
    
    if depth == 0 or isGameOver(board):
        return EvaluateHeuristic(board, player), None

    valid_moves = GetValidMoves(board, movesplayed)
    if not valid_moves:
        return 0, None

    if maximizingPlayer:
        maxH = -float('inf')
        best_move = None
        for move in valid_moves:
            new_board, new_movesplayed = applyMove(board, move, player, movesplayed)
            
            if isWin(new_board, player):
                return 100000, move
            
            H, _ = Minimax(new_board, depth - 1, False, player, new_movesplayed)
            if H > maxH:
                maxH = H
                best_move = move
        return maxH, best_move
    else:
        minH = float('inf')
        best_move = None
        for move in valid_moves:
            new_board, new_movesplayed = applyMove(board, move, opponent, movesplayed)

            if isWin(new_board, opponent):
                return -100000, move

            H, _ = Minimax(new_board, depth - 1, True, player, new_movesplayed)
            if H < minH:
                minH = H
                best_move = move
        return minH, best_move


def findBestMove(board, player, movesplayed):
    if len(movesplayed) == 0:
        center_x, center_y = board.shape[0] // 2, board.shape[1] // 2
        return (center_x, center_y)
    opponent = 'O' if player == 'X' else 'X'
    valid_moves = GetValidMoves(board, movesplayed)

    # Check for blocking opponent's immediate win
    for move in valid_moves:
        temp_board, temp_moves = applyMove(board, move, opponent, movesplayed)
        if isWin(temp_board, opponent):
            return move  # Block the win
    
    
    _, best_move = Minimax(board, 2, True, player, movesplayed)
    return best_move

def findBestMove_alpha_beta(board, player, movesplayed):
    if len(movesplayed) == 0:
        center_x, center_y = board.shape[0] // 2, board.shape[1] // 2
        return (center_x, center_y)

    opponent = 'O' if player == 'X' else 'X'
    valid_moves = GetValidMoves(board, movesplayed)

    # Check for blocking opponent's immediate win
    for move in valid_moves:
        temp_board, temp_moves = applyMove(board, move, opponent, movesplayed)
        if isWin(temp_board, opponent):
            return move  # Block the win

    _, best_move = Minimax_alpha_beta(board, 2, True, player, movesplayed)
    return best_move


def isWin(board, player):
    rows, cols = board.shape
    n = 5
    # Horizontal check
    for i in range(rows):
        for j in range(cols - n + 1):
            if np.all(board[i, j:j+5] == player):
                return True

    # Vertical check
    for i in range(rows - n + 1):
        for j in range(cols):
            if np.all(board[i:i+n, j] == player):
                return True

    # Diagonal (top-left to bottom-right)
    for i in range(rows - n + 1):
        for j in range(cols - n + 1):
            if all(board[i + k, j + k] == player for k in range(n)):
                return True

    # Diagonal (top-right to bottom-left)
    for i in range(rows - n + 1):
        for j in range(n - 1, cols):
            if all(board[i + k, j - k] == player for k in range(n)):
                return True

    return False

def isDraw(board):
    return np.all(board != '.')

def isGameOver(board):
    return isWin(board, 'X') or isWin(board , 'O') or isDraw(board)

def printBoard(board):
   print(board)
def Minimax_alpha_beta(board, depth, maximizingPlayer, player, movesplayed , alpha = -float('inf'), beta = float('inf')):
        opponent = 'O' if player == 'X' else 'X'
        
        if depth == 0 or isGameOver(board):
            return EvaluateHeuristic(board, player), None

        valid_moves = GetValidMoves(board, movesplayed)
        if not valid_moves:
            return 0, None

        if maximizingPlayer:
            maxH = -float('inf')
            best_move = None
            for move in valid_moves:
                new_board, new_movesplayed = applyMove(board, move, player, movesplayed)
                
                if isWin(new_board, player):
                    return 100000, move
                
                H, _ = Minimax_alpha_beta(new_board, depth - 1, False, player, new_movesplayed,alpha,beta)
                if H > maxH:
                    maxH = H
                    best_move = move
                if maxH >= beta:
                    return maxH, best_move
                alpha = max(alpha,maxH)
            return maxH, best_move
        else:
            minH = float('inf')
            best_move = None
            for move in valid_moves:
                new_board, new_movesplayed = applyMove(board, move, opponent, movesplayed)

                if isWin(new_board, opponent):
                    return -100000, move

                H, _ = Minimax_alpha_beta(new_board, depth - 1, True, player, new_movesplayed,alpha,beta)
                if H < minH:
                    minH = H
                    best_move = move
                if minH <= alpha:
                    return minH, best_move
                beta = min(beta, minH)
            return minH, best_move

def HumanvsAiGame(board):
   playerName = input("Enter Your Name :)")
   print("Welcome to Gomoku!" + playerName)
   movesplayed = []
   current_player = 'X'
   while not isGameOver(board):
         printBoard(board)
         if current_player == 'X':
             x , y = map(int, input("Enter your move (row and column): ").split())
             while not isValid(x, y) or board[x][y] != '.':
                print("Invalid move. Try again.")
                x, y = map(int, input("Enter your move (row and column): ").split())
             board[x][y] = current_player    
             movesplayed.append((x, y))
             if(isGameOver(board)):
                printBoard(board)
                if isWin(board, current_player):
                    print(f"Player {current_player} wins!")
                elif isDraw(board):
                    print("It's a draw!")
             current_player = 'O'       
         else : 
                print("AI is thinking...")
                best_move = findBestMove(board, current_player, movesplayed)
                if best_move:
                    x, y = best_move
                    board[x][y] = current_player
                    movesplayed.append((x, y))
                    print(f"AI played at ({x}, {y})")
                    if(isGameOver(board)):
                        printBoard(board)
                        if isWin(board, current_player):
                            print(f"AI Player {current_player} wins!")
                        elif isDraw(board):
                            print("It's a draw!")           
                current_player = 'X'


def AIvsAIGame(board):
   print("Welcome to Gomoku!")
   movesplayed = []
   current_player = 'X'
   while not isGameOver(board):
         printBoard(board)
         if current_player == 'X':
             print("AI-1 is thinking...")
             
             best_move = findBestMove_alpha_beta(board, current_player, movesplayed)
             if best_move:
                x, y = best_move
                board[x][y] = current_player
                movesplayed.append((x, y))
                print(f"AI played at ({x}, {y})")
             if(isGameOver(board)):
                printBoard(board)
                if isWin(board, current_player):
                    print(f"AI-1 Player {current_player} wins!")
                elif isDraw(board):
                    print("It's a draw!")
             current_player = 'O'       
         else : 
                print("AI-2 is thinking...")
                best_move = findBestMove(board, current_player, movesplayed)
                if best_move:
                    x, y = best_move
                    board[x][y] = current_player
                    movesplayed.append((x, y))
                    print(f"AI played at ({x}, {y})")
                    if(isGameOver(board)):
                        printBoard(board)
                        if isWin(board, current_player):
                            print(f"AI-2 Player {current_player} wins!")
                        elif isDraw(board):
                            print("It's a draw!")           
                current_player = 'X'

def main():
 board = CreateBoard()
 print("Welcome to our Game Space...","please Choose the number for the version Of Gomoku To start \n"
 "1. Human VS AI.\n"
 "2. AI VS AI\n"
 "3. quit")
 choice = input("Enter your choice: ")
 if choice == "1":
    HumanvsAiGame(board)
 elif choice =="2":
     print("AI VS AI")
     AIvsAIGame(board)
 else:
     quit = input("Are you sure you want to quit(Yes or No)\n")
     if quit.lower() == "yes":
         print("Good Bye")
     


if __name__ == "__main__":
    main()