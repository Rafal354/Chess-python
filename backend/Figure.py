import copy
from backend.Vector import Vector


class Element:
    def __init__(self, position):
        self.color = 'black' if position.black_or_white_cell() else 'white'
        self.image = 'frontend/assets/blank.png' if position.black_or_white_cell() else 'frontend/assets/blank.png'
        self.position = position

    def print_in_console(self):
        return self.image[9:]


class Figure(Element):
    def __init__(self, position):
        Element.__init__(self, position)
        self.position = position
        self.moves = []

    def one_line(self, destination):
        return self.position.one_line(destination)

    def one_row(self, destination):
        return self.position.one_row(destination)

    def one_diagonal(self, destination):
        return self.position.one_diagonal(destination)

    def direction(self, destination):
        if self.one_line(destination):
            return Vector(-1, 0) if self.position.move_line_up(destination) else Vector(1, 0)
        if self.one_row(destination):
            return Vector(0, 1) if self.position.move_row_right(destination) else Vector(0, -1)
        if self.one_diagonal(destination):
            if self.position.move_line_up(destination):
                return Vector(-1, 1) if self.position.move_row_right(destination) else Vector(-1, -1)
            else:
                return Vector(1,  1) if self.position.move_row_right(destination) else Vector(1, -1)

    def calculate(self, engine):
        for i in range(8):
            for j in range(8):
                if engine.chessboard.is_possible_move(self, Vector(i, j)):
                    old_eng = copy.deepcopy(engine)
                    old_eng.move(self.position, Vector(i, j))
                    king_position = old_eng.chessboard.white_king_position if old_eng.current_player == 'white'\
                        else old_eng.chessboard.black_king_position
                    col = 'white' if old_eng.current_player == 'black' else 'black'
                    if not old_eng.chessboard.is_check(king_position, col):
                        self.moves.append(Vector(i, j))

    def check_if_in_moves(self, position):
        for move in self.moves:
            if move.equal(position):
                return True
        return False


class Pawn(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = 'frontend/assets/pw.png' if self.color == 'white' else 'frontend/assets/pb.png'
        self.en_passant = Vector(20, 20)

    def is_starting_row(self):
        return self.position.is_second_row() if self.color == 'white' else self.position.is_seventh_row()


class Knight(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = 'frontend/assets/kw.png' if self.color == 'white' else 'frontend/assets/kb.png'


class Bishop(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = 'frontend/assets/bw.png' if self.color == 'white' else 'frontend/assets/bb.png'

    def correct_move(self, destination):
        return self.one_diagonal(destination)


class Rook(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.right_to_castling = 'yes'
        self.image = 'frontend/assets/rw.png' if self.color == 'white' else 'frontend/assets/rb.png'

    def correct_move(self, destination):
        return self.one_row(destination) or self.one_line(destination)


class Queen(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.image = 'frontend/assets/qw.png' if self.color == 'white' else 'frontend/assets/qb.png'

    def correct_move(self, destination):
        return self.one_row(destination) or self.one_line(destination) or self.one_diagonal(destination)


class King(Figure):
    def __init__(self, color, position):
        Figure.__init__(self, position)
        self.color = color
        self.position = position
        self.right_to_castling = 'yes'
        self.image = 'frontend/assets/kingw.png' if self.color == 'white' else 'frontend/assets/kingb.png'

    def initial_position(self):
        return self.position.equal(Vector(7, 4)) or self.position.equal(Vector(0, 4))

    def is_castle_move(self, destination):
        return self.initial_position() and self.position.column_distance(destination, 2)
