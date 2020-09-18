# 2 player chess
# Author: Mihir Ravi
##########################################################

class Chess:
    SQUARE_SIZE = 40

    def __init__(self):
        import turtle
        turtle.colormode(255)
        self.pen = turtle.Turtle()
        self.window = turtle.Screen()
        self.board = ChessBoard(self.pen, Chess.SQUARE_SIZE)
        self.piece = ChessPiece(self.board)
        self.update = turtle.update
        self.user_input = Input(self.board, self.piece,
                                self.window, self.update)
        turtle.tracer(0, 0)
        self.pen.speed(0)
        self.pen.ht()
        self.pen.pensize(.5)

    def _select_piece(self, row, col):
        self.board.select_piece(row, col)
        self.update()

    def _move_piece(self, frow, fcol, trow, tcol):
        self.board.move_piece(frow, fcol, trow, tcol)
        self.update()

    def run(self):
        import time
        self.board.draw_board()
        self.piece.start_at_beginning()
        self.update()
        self.window.listen()


class ChessBoard:

    def __init__(self, pen, square_side_size):

        self.border_color = (30, 44, 87)

        self.square_dark = (84, 102, 161)

        self.square_light = (255, 255, 255)

        self.not_select_color = (0, 0, 0)

        self.select_color = (0, 0, 255)

        self.pen = pen

        self.next_square = square_side_size + 1

        self.board_side = square_side_size*8 + 7

        self.board_top_y = self.next_square*4

        self.board_lft_x = self.next_square*-4

        self.square_side_size = square_side_size

        self.border_size = square_side_size*1.2

        self.squares = [[None for col in range(8)] for row in range(8)]

    def _draw_square(self, left_x, top_y, side, color, fill):

        self.pen.up()

        self.pen.color(color)

        self.pen.goto(left_x, top_y)

        self.pen.down()

        self.pen.begin_fill()

        for i in range(4):
            self.pen.forward(side)
            self.pen.right(90)

        self.pen.end_fill()

    def _goto_piece_xy(self, row, col, adjustment_x=0):

        self.pen.up()

        x = (self.board_lft_x + col*(self.next_square) +
             self.square_side_size*.05) + adjustment_x*self.square_side_size

        y = (self.board_top_y - row*(self.next_square) -
             self.square_side_size*.8)

        self.pen.goto(x, y)

    def _put_chr_at(self, char, row, col, color, adjustment_x=0):

        self._goto_piece_xy(row, col, adjustment_x)

        self.pen.color(color)

        self.pen.write(char, font=("Courier", round(self.square_side_size*.7),
                                   "normal"))

    def xy_to_rowcol(self, x, y):

        col = int((x - self.board_lft_x) / self.next_square)
        row = int((self.board_top_y - y) / self.next_square)

        return [row, col]

    def overwrite_board_square(self, row, col):

        x = self.board_lft_x + col*self.next_square
        y = self.board_top_y - row*self.next_square
        color = self.square_light if (row+col) % 2 == 0 else self.square_dark
        self._draw_square(x, y, self.square_side_size, color, True)

    def put_piece(self, piece, row, col):

        self.squares[row][col] = piece

        self._put_chr_at(piece, row, col, self.not_select_color, 0)

    def draw_board(self):

        # Clears screen of all turtle drawings
        self.pen.clear()

        # Draw border and fill everything.
        self._draw_square(self.board_lft_x - self.border_size,
                          self.board_top_y + self.border_size,
                          self.board_side + 2*self.border_size,
                          self.border_color, True)

        # Draw white squares of board.
        self._draw_square(self.board_lft_x, self.board_top_y,
                          self.board_side, self.square_light, True)

        # Draw dark squares of board.
        for row in range(8):
            x = self.board_lft_x + self.next_square - row % 2*self.next_square
            y = self.board_top_y - row*self.next_square
            for col in range(4):
                self._draw_square(x, y, self.square_side_size, self.square_dark,
                                  True)
                x += 2*self.next_square

        # Draw Notation 1-8 on border.
        for row in range(8):
            self._put_chr_at(chr(ord(str(8-row))), row, -1, (0, 0, 0), .2)

        # Draw Notation a-h on border.
        for col in range(8):
            self._put_chr_at(chr(ord('a')+col), 8, col, (0, 0, 0), .2)

        # Draw White Turn.
        self._put_chr_at("Turn: White", 9, 1, (0, 0, 0), .2)

    def move_piece(self, from_row, from_col, to_row, to_col):

        # Get piece from-square
        piece = self.squares[from_row][from_col]

        # overwrite from-square and update board to relect nothing.
        self.squares[from_row][from_col] = None

        self.overwrite_board_square(from_row, from_col)

        # Overwrite to-square (including any pieces taken).
        self.overwrite_board_square(to_row, to_col)

        self.put_piece(piece, to_row, to_col)

        self.squares[to_row][to_col] = piece

        return True

    def select_piece(self, row, col):

        piece = self.squares[row][col]
        if piece != None:
            self._put_chr_at(piece, row, col, self.select_color)

        return piece

    def unselect_piece(self, row, col):

        piece = self.squares[row][col]

        self.overwrite_board_square(row, col)

        self._put_chr_at(piece, row, col, self.not_select_color)


class ChessPiece:

    W_KING = u'♔'
    W_QUEEN = u'♕'
    W_ROOK = u'♖'
    W_BISHOP = u'♗'
    W_KNIGHT = u'♘'
    W_PAWN = u'♙'
    B_KING = u'♚'
    B_QUEEN = u'♛'
    B_ROOK = u'♜'
    B_BISHOP = u'♝'
    B_KNIGHT = u'♞'
    B_PAWN = u'♟'

    def __init__(self, chess_board):

        self.board = chess_board

    def start_at_beginning(self):

        b_pieces = [ChessPiece.B_ROOK,
                    ChessPiece.B_KNIGHT,
                    ChessPiece.B_BISHOP,
                    ChessPiece.B_QUEEN,
                    ChessPiece.B_KING,
                    ChessPiece.B_BISHOP,
                    ChessPiece.B_KNIGHT,
                    ChessPiece.B_ROOK]
        w_pieces = [ChessPiece.W_ROOK,
                    ChessPiece.W_KNIGHT,
                    ChessPiece.W_BISHOP,
                    ChessPiece.W_QUEEN,
                    ChessPiece.W_KING,
                    ChessPiece.W_BISHOP,
                    ChessPiece.W_KNIGHT,
                    ChessPiece.W_ROOK]

        for i in range(8):
            self.board.put_piece(b_pieces[i], 0, i)
            self.board.put_piece(ChessPiece.B_PAWN, 1, i)
            self.board.put_piece(w_pieces[i], 7, i)
            self.board.put_piece(ChessPiece.W_PAWN, 6, i)

    def piece_color(self, piece):

        if piece == None:
            return None

        if ord(ChessPiece.W_KING) <= ord(piece) <= ord(ChessPiece.W_PAWN):
            return "white"

        return "black"

    def _is_taking_own_piece(self, from_row, from_col, to_row, to_col):

        # Get piece being moved
        piece = self.board.squares[from_row][from_col]
        piece_color = self.piece_color(piece)

        # is piece trying to take it's own piece?
        to_piece = self.board.squares[to_row][to_col]
        if to_piece != None:
            if self.piece_color(to_piece) == piece_color:
                return True

        return False

    def _any_piece_in_way(self, from_row, from_col, dr, dc, dm):

        for i in range(1, dm):
            if self.board.squares[from_row+i*dr][from_col+i*dc] != None:
                return False

        return True

    def _is_rook_move_valid(self, from_row, from_col, to_row, to_col):

        # if not on same column or row
        if ((from_row != to_row and from_col != to_col) or
                (from_row == to_row and from_col == to_col)):
            return False

        # check if any pieces are in the way of destination
        if from_row != to_row:
            dc = 0
            dr = 1 if to_row - from_row > 0 else -1

        if from_col != to_col:
            dr = 0
            dc = 1 if to_col - from_col > 0 else -1

        dm = abs(to_row - from_row)

        return self._any_piece_in_way(from_row, from_col, dr, dc, dm)

    def _is_knight_move_valid(self, from_row, from_col, to_row, to_col):

        # check for valid move
        if ((abs(from_row - to_row) == 1 and abs(from_col - to_col) == 2) or
                (abs(from_row - to_row) == 2 and abs(from_col - to_col) == 1)):
            return True

        return False

    def _is_bishop_move_valid(self, from_row, from_col, to_row, to_col):

        # if not on same colored diagonal exit.
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False

        # check if any pieces are in the way of destination
        dr = 1 if to_row - from_row > 0 else -1
        dc = 1 if to_col - from_col > 0 else -1
        dm = abs(to_row - from_row)

        return self._any_piece_in_way(from_row, from_col, dr, dc, dm)

    def _is_queen_move_valid(self, from_row, from_col, to_row, to_col):

        # if not on same colored diagonal
        if abs(from_row - to_row) != abs(from_col - to_col):

            # if on same row? (like rook)
            if from_row != to_row:
                dc = 0
                dr = 1 if to_row - from_row > 0 else -1

            # elif on same col?
            elif from_col != to_col:
                dr = 0
                dc = 1 if to_col - from_col > 0 else -1
            else:
                # if not on same col or row
                return False
        else:
            # on same colored diagonal (moves like bishop)
            dr = 1 if to_row - from_row > 0 else -1
            dc = 1 if to_col - from_col > 0 else -1

        # check if any pieces are in the way of destination
        dm = abs(to_row - from_row)
        return self._any_piece_in_way(from_row, from_col, dr, dc, dm)

    def _is_king_move_valid(self, from_row, from_col, to_row, to_col):

        if abs(to_row - from_row) <= 1 and abs(to_col - from_col) <= 1:
            return True
        return False

    def _is_pawn_move_valid(self, from_row, from_col, to_row, to_col):

        # Setup variables used
        piece = self.board.squares[from_row][from_col]
        to_piece = self.board.squares[to_row][to_col]
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        dc = 0

        # Set flag for first move of pawn
        first_move = True if from_row == 6 or from_row == 1 else False

        # If direction is not correct for white, exit
        if to_row - from_row > 0:
            dr = 1
            if self.piece_color(piece) == "white":
                return False

        # If direction is not correct for black, exit
        if to_row - from_row < 0:
            dr = -1
            if self.piece_color(piece) == "black":
                return False

        # If moving straight
        if from_col == to_col:
            # if not legal straight move, exit
            if not (row_diff == 1 or (first_move and row_diff == 2)):
                return False

            # make sure to move has no pieces on straight path
            dm = row_diff + 1

            return self._any_piece_in_way(from_row, from_col, dr, dc, dm)

            # otherwise legal move
            # return True

        # else move must be taking piece move
        # if legal taking piece move and (opponent-already check for own piece) piece at to-square
        if col_diff == 1 and row_diff == 1 and to_piece != None:
            return True

        return False

    def is_move_valid(self, from_row, from_col, to_row, to_col):

        # check is taking own piece?
        if self._is_taking_own_piece(from_row, from_col, to_row, to_col):
            return False

        piece = self.board.squares[from_row][from_col]
        if piece == ChessPiece.W_ROOK or piece == ChessPiece.B_ROOK:
            return self._is_rook_move_valid(from_row, from_col,
                                            to_row, to_col)
        if piece == ChessPiece.W_KNIGHT or piece == ChessPiece.B_KNIGHT:
            return self._is_knight_move_valid(from_row, from_col,
                                              to_row, to_col)
        if piece == ChessPiece.W_BISHOP or piece == ChessPiece.B_BISHOP:
            return self._is_bishop_move_valid(from_row, from_col,
                                              to_row, to_col)
        if piece == ChessPiece.W_QUEEN or piece == ChessPiece.B_QUEEN:
            return self._is_queen_move_valid(from_row, from_col,
                                             to_row, to_col)
        if piece == ChessPiece.W_KING or piece == ChessPiece.B_KING:
            return self._is_king_move_valid(from_row, from_col,
                                            to_row, to_col)
        if piece == ChessPiece.W_PAWN or piece == ChessPiece.B_PAWN:
            return self._is_pawn_move_valid(from_row, from_col,
                                            to_row, to_col)

    def is_check_or_mate(self, color_move):

        # Get all pieces of color_move and get opposing king
        pieces = []  # a tuple (row,col) of where piece is located
        krow = None  # row of opposing king
        kcol = None  # col of opposing king
        for row in range(8):
            for col in range(8):
                piece = self.board.squares[row][col]
                if self.piece_color(piece) == color_move:
                    pieces.append((row, col))
                elif piece == ChessPiece.W_KING or piece == ChessPiece.B_KING:
                    krow = row
                    kcol = col

        # Check if place in Check
        num_piece_check = 0
        return_result = 0

        for piece_rowcol in pieces:
            frow, fcol = piece_rowcol
            if self.is_move_valid(frow, fcol, krow, kcol):
                num_piece_check += 1
            if num_piece_check == 2:
                break
        if num_piece_check > 0:
            return_result += 1

        return return_result


class Input:

    def __init__(self, chess_board, pieces, window, update):

        self.pieces = pieces

        self.update = update

        self.is_piece_selected = False

        self.selected_row = -1

        self.selected_col = -1

        self.turn_color = "white"

        self.check_color = None

        window.onclick(self.onclick)

    def onclick(self, x, y):
        # Check to see if within board for x. Do nothing if not.
        board_x = x - self.board.board_lft_x
        if (board_x < 0 or
                board_x >= 8*self.board.next_square):
            return

        # Checks to see if within board for y. Do nothing if not.
        board_y = self.board.board_top_y - y
        if (board_y < 0 or
                board_y >= 8*self.board.next_square):
            return

        # Get the row, col from x, y.
        row, col = self.board.xy_to_rowcol(x, y)

        # if first time selecting piece
        if self.is_piece_selected == False:
            selected_piece = self.board.select_piece(row, col)
            # if selected piece is not a piece then exit
            if selected_piece == None:
                return

            # if piece is not correct turn color then exit
            piece_color = self.pieces.piece_color(selected_piece)
            if self.turn_color is not piece_color:
                self.board.unselect_piece(row, col)
                return

            # update selected piece
            print("update selected piece")  # debug
            self.update()  # update selected color in self.board.select_piece(row,col)
            self.is_piece_selected = True
            self.selected_row = row
            self.selected_col = col
            return

        # (then must have piece already selected)
        # if new row,col is the same as selected one, then unselect
        if row == self.selected_row and col == self.selected_col:
            self.board.unselect_piece(row, col)
            self.update()
            self.is_piece_selected = False
            self.selected_row = -1
            self.selected_col = -1
            return

        # check if valid move
        if self.pieces.is_move_valid(self.selected_row,
                                     self.selected_col, row, col) == False:
            return

        # if in check, check if move would get out of check
        pass

        # save original board just in case can't move there
        org_selected_row = self.selected_row
        org_selected_col = self.selected_col
        org_selected_piece = self.board.squares[self.selected_row][self.selected_col]
        org_row = row
        org_col = col
        org_to_piece = self.board.squares[row][col]

        # move piece
        self.board.move_piece(self.selected_row, self.selected_col, row, col)
        print(self.board.squares)
        self.update()
        self.is_piece_selected = False
        self.selected_row = -1
        self.selected_col = -1

        # if in check, check if move would get out of check or move would result in check or mate

        # switch player
        self.turn_color = "black" if self.turn_color == "white" else "white"

        # display turn before next selected piece begins
        if self.turn_color == "white":
            self.board._put_chr_at("Turn: Black", 9, 1, (255, 255, 255), .2)
            self.board._put_chr_at("Turn: White", 9, 1, (0, 0, 0), .2)
        else:
            self.board._put_chr_at("Turn: White", 9, 1, (255, 255, 255), .2)
            self.board._put_chr_at("Turn: Black", 9, 1, (0, 0, 0), .2)

        # if turn to move is in check
        if self.turn_color == self.check_color:
            self.board._put_chr_at("Check", 10, 3, (0, 0, 0), .2)
        else:
            self.board._put_chr_at("Check", 10, 3, (255, 255, 255), .2)

        self.update()


if __name__ == "__main__":
    while True:
        chess = Chess()
        chess.run()
