
class AttCoord:
    ChessGame = None

    @classmethod
    def get(cls, piece, kingcheck=True):
        if piece.name == 'pawn':
            coords = cls.get_pawn(piece, kingcheck)
        elif piece.name == 'bishop':
            coords = cls.get_bishop(piece, kingcheck)
        elif piece.name == 'rock':
            coords = cls.get_rock(piece, kingcheck)
        elif piece.name == 'queen':
            coords = cls.get_queen(piece, kingcheck)
        elif piece.name == 'knight':
            coords = cls.get_knight(piece, kingcheck)
        elif piece.name == 'king':
            coords = cls.get_king(piece, kingcheck)
        return coords

    @classmethod
    def in_dim(cls, coord):
        if not (0 > coord[0] or coord[0] > 7 or 0 > coord[1] or coord[1] > 7):
            return True

    @classmethod
    def get_coord_state(cls, coord, piece, kingcheck=False):
        '''Check for blocking piece and for kingcheck'''
        # check piece of same color
        if piece.color == 'white':
            same_piece = cls.ChessGame.players['white'].get_piece(coord)
            opponent_piece = cls.ChessGame.players['black'].get_piece(coord)
        else:
            same_piece = cls.ChessGame.players['black'].get_piece(coord)
            opponent_piece = cls.ChessGame.players['white'].get_piece(coord)
        if same_piece:
            return 'block'
        
        if kingcheck:
            # check opponent piece
            if opponent_piece:
                if cls.check_kingcheck(coord, piece, True):
                    return 'opponent'
                else:
                    return 'kingcheck'
            # case where there's no piece on coord
            if not cls.check_kingcheck(coord, piece, False):
                return 'kingcheck'
        else:
            # check opponent piece
            if opponent_piece:
                return 'opponent'
        
    @classmethod
    def check_kingcheck(cls, coord, piece, attack):
        '''Check if movement cause kingcheck'''
        original_coord = piece.coord
        if not attack:
            piece.coord = coord
            # check if there is a kingcheck
            is_check = cls.ChessGame.check_for_check(piece.color, False)
            piece.coord = original_coord
            if is_check:
                # check so can't move piece
                return False
        else:
            # remove temporarily the attacked piece
            attacked_piece = cls.ChessGame.get_piece(coord)
            cls.ChessGame.players[attacked_piece.color].pieces.remove(attacked_piece)
            # move the attacking piece AFTER
            piece.coord = coord
            # check if there is a kingcheck
            is_check = cls.ChessGame.check_for_check(piece.color, False)
            # revert changes
            piece.coord = original_coord
            cls.ChessGame.players[attacked_piece.color].pieces.append(attacked_piece)
            if is_check:
                # check so can't move piece
                return False
        return True
                
    @classmethod
    def create_coords(cls, dy, dx, coords, piece, kingcheck=True):
        for i in range(8):
            coord = (piece.x + (i+1)*dx, piece.y + (i+1)*dy)
            if cls.in_dim(coord):
                coord_state = cls.get_coord_state(coord, piece, kingcheck)
                if coord_state == 'block': # own piece on coord
                    break
                elif coord_state == 'opponent': # opponent piece on coord
                    coords.append(coord)
                    break
                elif coord_state == 'kingcheck':
                    pass 
                else: # no piece on coord
                    coords.append(coord)

    @classmethod
    def get_pawn(cls, piece, kingcheck=True):
        coords = []
        if piece.color == 'white':
            if piece.x < 7 and piece.y > 0:
                coords.append((piece.x + 1, piece.y - 1))
            if piece.x > 0 and piece.y > 0:
                coords.append((piece.x - 1, piece.y - 1))
        else:
            if piece.x < 7 and piece.y < 7:
                coords.append((piece.x + 1, piece.y + 1))
            if piece.x > 0 and piece.y < 7:
                coords.append((piece.x - 1, piece.y + 1))
        
        final_coords = []
        for coord in coords:
            if cls.in_dim(coord):
                coord_state = cls.get_coord_state(coord, piece, kingcheck)
                if coord_state != 'block' and coord_state != 'kingcheck':
                    final_coords.append(coord)
        return final_coords
    
    @classmethod
    def get_bishop(cls, piece, kingcheck=True):
        coords = []
        dy = 1
        dx = -1
        cls.create_coords(dy, dx, coords, piece, kingcheck)
        dx = 1
        cls.create_coords(dy, dx, coords, piece, kingcheck)
        dy = -1
        dx = -1
        cls.create_coords(dy, dx, coords, piece, kingcheck)
        dx = 1
        cls.create_coords(dy, dx, coords, piece, kingcheck)
        return coords
    
    @classmethod
    def get_rock(cls, piece, kingcheck=True):
        coords = []
        dy = 1
        dx = 0
        cls.create_coords(dy, dx, coords, piece, kingcheck)
        dy = -1
        cls.create_coords(dy, dx, coords, piece, kingcheck)
        dy = 0
        dx = -1
        cls.create_coords(dy, dx, coords, piece, kingcheck)
        dx = 1
        cls.create_coords(dy, dx, coords, piece, kingcheck)
        return coords
    
    @classmethod
    def get_queen(cls, piece, kingcheck=True):
        coords = cls.get_bishop(piece, kingcheck)
        coords += cls.get_rock(piece, kingcheck)
        return coords
    
    @classmethod
    def get_knight(cls, piece, kingcheck=True):
        coords = []
        coords.append((piece.x+1,piece.y+2))
        coords.append((piece.x-1,piece.y+2))
        coords.append((piece.x+1,piece.y-2))
        coords.append((piece.x-1,piece.y-2))
        coords.append((piece.x+2,piece.y+1))
        coords.append((piece.x-2,piece.y-1))
        coords.append((piece.x+2,piece.y-1))
        coords.append((piece.x-2,piece.y+1))
        final_coords = []
        for coord in coords:
            if cls.in_dim(coord):
                coord_state = cls.get_coord_state(coord, piece, kingcheck)
                if coord_state != 'block' and coord_state != 'kingcheck':
                    final_coords.append(coord)
        return final_coords
    
    @classmethod
    def get_king(cls, piece, kingcheck=True):
        coords = []
        coords.append((piece.x+1,piece.y+1))
        coords.append((piece.x-1,piece.y+1))
        coords.append((piece.x-1,piece.y-1))
        coords.append((piece.x+1,piece.y-1))
        coords.append((piece.x,piece.y+1))
        coords.append((piece.x,piece.y-1))
        coords.append((piece.x+1,piece.y))
        coords.append((piece.x-1,piece.y))
        final_coords = []
        for coord in coords:
            if cls.in_dim(coord):
                coord_state = cls.get_coord_state(coord, piece, kingcheck)
                if coord_state != 'block' and coord_state != 'kingcheck':
                    final_coords.append(coord)
        return final_coords

class PossibleMove:
    players = None

    @classmethod
    def get(cls, piece):
        if piece.name == 'pawn':
            coords = cls.get_pawn(piece)
        elif piece.name == 'bishop':
            coords = cls.get_bishop(piece)
        elif piece.name == 'rock':
            coords = cls.get_rock(piece)
        elif piece.name == 'queen':
            coords = cls.get_queen(piece)
        elif piece.name == 'knight':
            coords = cls.get_knight(piece)
        elif piece.name == 'king':
            coords = cls.get_king(piece)
        return coords
    
    @classmethod
    def rem_opp_piece(cls, coords, piece):
        to_rem = []
        
        for coord in coords:
            if AttCoord.get_coord_state(coord, piece) == 'opponent':
                to_rem.append(coord)
        
        for coord in to_rem:
            coords.remove(coord)
        
        return coords
    
    @classmethod
    def get_line(cls, color):
        if color == 'white':
            return 7
        else:
            return 0

    @classmethod
    def get_pawn(cls, piece):
        coords = []
        if piece.color == 'white':
            coord = (piece.x, piece.y-1)
            if not AttCoord.get_coord_state(coord, piece):
                coords.append(coord)
            if not piece.moved:
                coord = (piece.x, piece.y-2)
                # check inter coord too
                if not AttCoord.get_coord_state((piece.x, piece.y-1), piece):
                    if not AttCoord.get_coord_state(coord, piece):
                        coords.append(coord)
        else:
            coord = (piece.x, piece.y+1)
            if not AttCoord.get_coord_state(coord, piece):
                coords.append(coord)
            if not piece.moved:
                coord = (piece.x, piece.y+2)
                # check inter coord too
                if not AttCoord.get_coord_state((piece.x, piece.y+1), piece):
                    if not AttCoord.get_coord_state(coord, piece):
                        coords.append(coord)
        
        # check for kingcheck
        to_rem = []
        for coord in coords:
            if not AttCoord.check_kingcheck(coord, piece, False):
                to_rem.append(coord)
        for coord in to_rem:
            coords.remove(coord)
        
        return coords
        
    @classmethod
    def get_bishop(cls, piece):
        coords = AttCoord.get_bishop(piece)
        coords = cls.rem_opp_piece(coords, piece)
        
        return coords
    
    @classmethod
    def get_rock(cls, piece):
        coords = AttCoord.get_rock(piece)
        coords = cls.rem_opp_piece(coords, piece)
        
        return coords
    
    @classmethod
    def get_knight(cls, piece):
        coords = AttCoord.get_knight(piece)
        coords = cls.rem_opp_piece(coords, piece)
        
        return coords
    
    @classmethod
    def get_queen(cls, piece):
        coords = AttCoord.get_queen(piece)
        coords = cls.rem_opp_piece(coords, piece)
        
        return coords

    @classmethod
    def get_king(cls, piece):
        coords = AttCoord.get_king(piece)
        coords = cls.rem_opp_piece(coords, piece)
        
        return coords

    @classmethod
    def get_castle(cls, color):
        can_castle = [False, False] #long, short
        # first long castle
        if cls.can_long_castle(color) and cls.check_kingcheck_long_castle(color):
            can_castle[0] = True
        if cls.can_short_castle(color) and cls.check_kingcheck_short_castle(color):
            can_castle[1] = True
        
        return can_castle

    @classmethod
    def check_kingcheck_long_castle(cls, color):
        line = cls.get_line(color)
        
        rock = cls.players[color].get_piece((0,line))
        king = cls.players[color].king
        # simul move and look if there's a check
        king.coord = (2,line)
        rock.coord = (3,line)
        is_check = AttCoord.ChessGame.check_for_check(color, False)
        # reset coord
        king.coord = (4,line)
        rock.coord = (0,line)
        if is_check:
            # check so can't move piece
            return False
        return True

    @classmethod
    def can_long_castle(cls, color):
        line = cls.get_line(color)

        # check king and rocks didn't move
        rock1 = cls.players[color].get_piece((0,line))
        if rock1:
            if rock1.name == 'rock' and not rock1.moved and not cls.players[color].king.moved:
                # check that no piece are blocking
                for i in range(3):
                    piece = cls.players[color].get_piece((1+i, line))
                    if piece:
                        return
                return True
        
    @classmethod
    def can_short_castle(cls, color):
        line = cls.get_line(color)
        
        # check king and rocks didn't move
        rock1 = cls.players[color].get_piece((7,line))
        if rock1:
            if rock1.name == 'rock' and not rock1.moved and not cls.players[color].king.moved:
                # check that no piece are blocking
                for i in range(2):
                    piece = cls.players[color].get_piece((6-i, line))
                    if piece:
                        return
                return True
    
    @classmethod
    def check_kingcheck_short_castle(cls, color):
        line = cls.get_line(color)
        
        rock = cls.players[color].get_piece((7,line))
        king = cls.players[color].king
        # simul move and look if there's a check
        king.coord = (6,line)
        rock.coord = (5,line)
        is_check = AttCoord.ChessGame.check_for_check(color, False)
        # reset coord
        king.coord = (4,line)
        rock.coord = (7,line)
        if is_check:
            # check so can't move piece
            return False
        return True