import itertools

def inv_c(color):
    if color == 'white':
        return 'black'
    else:
        return 'white'

class PossibleMove:
    '''
    Search possible moves for pieces  
    Use get() method for normal moves  
    Use get_castle() for castle moves
    '''
    ChessGame = None
    static_moves = []

    @classmethod
    def get(cls, piece, is_attacking, kingcheck=True):
        '''
        Return the possible moves for a piece
        '''

        # first store the opponent static moves
        if kingcheck:
            cls.get_static_opp_moves(piece.color)

        if piece.name == 'pawn':
            coords = cls.get_pawn(piece, is_attacking, kingcheck=kingcheck)
        elif piece.name == 'bishop':
            coords = cls.get_bishop(piece, is_attacking, kingcheck=kingcheck)
        elif piece.name == 'rock':
            coords = cls.get_rock(piece, is_attacking, kingcheck=kingcheck)
        elif piece.name == 'queen':
            coords = cls.get_queen(piece, is_attacking, kingcheck=kingcheck)
        elif piece.name == 'knight':
            coords = cls.get_knight(piece, is_attacking, kingcheck=kingcheck)
        elif piece.name == 'king':
            coords = cls.get_king(piece, is_attacking, kingcheck=kingcheck)
        return coords
    
    @classmethod
    def in_dim(cls, coord):
        if not (0 > coord[0] or coord[0] > 7 or 0 > coord[1] or coord[1] > 7):
            return True

    @classmethod
    def get_static_opp_moves(cls, color):
        '''
        Get the possible moves of the opponent pawns and knights, 
        this moves can be calulated only one time as they can't give discover checks.  
        Kingcheck are ignored as the purpose of this moves is to look for kingcheck on our own king
        '''
        cls.static_moves = []
        for piece in cls.ChessGame.players[inv_c(color)].pieces:
            if piece.name == 'pawn' or piece.name == 'knight':
                cls.static_moves += cls.get(piece, True, kingcheck=False)

    @classmethod
    def get_coord_state(cls, coord, piece, kingcheck=False):
        '''
        Check for blocking piece and for kingcheck
        Returs:
            - block, opponent, kingcheck, None (no piece)
        '''
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
            # check if taking opponent piece cause a kingcheck
            if opponent_piece:
                if cls.is_kingcheck(coord, piece, True):
                    return 'kingcheck'
                else:
                    return 'opponent'
            # case where there's no piece on coord
            if cls.is_kingcheck(coord, piece, False):
                return 'kingcheck'
        else:
            # check opponent piece
            if opponent_piece:
                return 'opponent'
        
    @classmethod
    def _is_check(cls, color):
        '''
        Check if the king of the selected player is on a attacked case
        '''

        king_coord = tuple(cls.ChessGame.players[color].king.coord)

        if king_coord in cls.static_moves:
            return True

        # check with bishop, rock, queen
        for piece in cls.ChessGame.players[inv_c(color)].pieces:
            if piece.name == 'bishop' or piece.name == 'rock' or piece.name == 'queen':
                if king_coord in cls.get(piece, True, kingcheck=False):
                    return True

        return False

    @classmethod
    def is_kingcheck(cls, coord, piece, attack):
        '''
        Check if movement cause kingcheck
        Return True if the move cause a kingcheck
        '''
        original_coord = piece.coord
        if not attack:
            piece.coord = coord
            # check if there is a kingcheck
            is_check = cls._is_check(piece.color)

            # revert changes
            piece.coord = original_coord
            
            return is_check
        else:
            # remove temporarily the attacked piece
            attacked_piece = cls.ChessGame.get_piece(coord)
            cls.ChessGame.players[attacked_piece.color].pieces.remove(attacked_piece)
            # move the attacking piece AFTER
            piece.coord = coord
            # check if there is a kingcheck
            is_check = cls._is_check(piece.color)
            # revert changes
            piece.coord = original_coord
            cls.ChessGame.players[attacked_piece.color].pieces.append(attacked_piece)
            
            return is_check
                
    @classmethod
    def create_coords(cls, dy, dx, coords, piece, is_attacking=True, kingcheck=True):
        for i in range(8):
            
            coord = (piece.x + (i+1)*dx, piece.y + (i+1)*dy)
            if not cls.in_dim(coord):
                break
            else:
                coord_state = cls.get_coord_state(coord, piece, kingcheck)
                if coord_state == 'block': # own piece on coord
                    break
                elif coord_state == 'opponent': # opponent piece on coord
                    # add depending on if attacking
                    if is_attacking:
                        coords.append(coord)
                    break
                elif coord_state == 'kingcheck':
                    pass
                else: # no piece on coord
                    coords.append(coord)
    
    @classmethod
    def get_line(cls, color):
        if color == 'white':
            return 7
        else:
            return 0

    @classmethod
    def get_pawn_att(cls, piece, kingcheck=True):
        '''
        Get attacking pawn moves (diagonale moves)
        '''

        if piece.color == 'white':
            dy = -1
        else:
            dy = 1

        coords = [
            (piece.x + 1, piece.y + dy),
            (piece.x - 1, piece.y + dy)
            ]
        
        for coord in coords:
            if not cls.in_dim(coord):
                coords.remove(coord)
            else:
                coord_state = cls.get_coord_state(coord, piece, kingcheck)
                if coord_state == 'block' or coord_state == 'kingcheck':
                    coords.remove(coord)
        
        return coords

    @classmethod
    def get_pawn_move(cls, piece, kingcheck=True):
        
        if piece.color == 'white':
            dy = -1
        else:
            dy = 1

        coords = [ (piece.x, piece.y + dy) ]

        if not piece.moved:
            # add the double move
            coords.append( (piece.x, piece.y + 2*dy) )
        
        final_coords = []

        for coord in coords:
            if cls.in_dim(coord):
                coord_state = cls.get_coord_state(coord, piece, kingcheck)
                if coord_state == None:
                    final_coords.append(coord)
                else:
                    break # if can't move of one case -> can't move of two case
            else:
                break # if can't move of one case -> can't move of two case
        
        return final_coords
        
    @classmethod
    def get_pawn(cls, piece, is_attacking, kingcheck=True):
        if is_attacking:
            return cls.get_pawn_att(piece, kingcheck=kingcheck)
        else:
            return cls.get_pawn_move(piece, kingcheck=kingcheck)

    @classmethod
    def get_bishop(cls, piece, is_attacking, kingcheck=True):
        coords = []
        dx, dy = -1, 1
        cls.create_coords(dy, dx, coords, piece, is_attacking=is_attacking, kingcheck=kingcheck)
        dx, dy = 1, 1
        cls.create_coords(dy, dx, coords, piece, is_attacking=is_attacking, kingcheck=kingcheck)
        dx, dy = -1, -1
        cls.create_coords(dy, dx, coords, piece, is_attacking=is_attacking, kingcheck=kingcheck)
        dx, dy = 1, -1
        cls.create_coords(dy, dx, coords, piece, is_attacking=is_attacking, kingcheck=kingcheck)
        return coords
    
    @classmethod
    def get_rock(cls, piece, is_attacking, kingcheck=True):
        coords = []
        dx, dy = 0, 1
        cls.create_coords(dy, dx, coords, piece, is_attacking=is_attacking, kingcheck=kingcheck)
        dx, dy = 0, -1
        cls.create_coords(dy, dx, coords, piece, is_attacking=is_attacking, kingcheck=kingcheck)
        dx, dy = -1, 0
        cls.create_coords(dy, dx, coords, piece, is_attacking=is_attacking, kingcheck=kingcheck)
        dx, dy = 1, 0
        cls.create_coords(dy, dx, coords, piece, is_attacking=is_attacking, kingcheck=kingcheck)
        return coords
    
    @classmethod
    def get_knight(cls, piece, is_attacking, kingcheck=True):
        coords = []
        for x, y in itertools.permutations([-2, -1, 1, 2], 2): # get all combinations of knight moves
            coord = (piece.x + x, piece.y + y)
            if abs(x) != abs(y) and cls.in_dim(coord):
                coord_state = cls.get_coord_state(coord, piece, kingcheck)
                if coord_state == None:
                    coords.append(coord)
                elif is_attacking and coord_state == 'opponent':
                    coords.append(coord)
       
        return coords
    
    @classmethod
    def get_queen(cls, piece, is_attacking, kingcheck=True):
        coords = cls.get_bishop(piece, is_attacking, kingcheck)
        coords += cls.get_rock(piece, is_attacking, kingcheck)
        return coords

    @classmethod
    def get_king(cls, piece, is_attacking, kingcheck=True):
        coords = []
        for x, y in itertools.product([0,1, -1], [0, 1, -1]): # get all combinations of king moves
            coord = (piece.x + x, piece.y + y)
            if (x != 0 or y != 0) and cls.in_dim(coord):
                coord_state = cls.get_coord_state(coord, piece, kingcheck)
                if coord_state == None:
                    coords.append(coord)
                elif is_attacking and coord_state == 'opponent':
                    coords.append(coord)
        
        return coords

    @classmethod
    def get_en_passant(cls, piece):
        '''
        Look for en passant move, if found one, return pawn target coord
        '''
        if piece.color == 'white':
            line = 3
            dy = -1
        else:
            line = 4
            dy = 1
        
        if piece.coord[1] == line:
            # look for opp pawn
            coord = [piece.coord[0] + 1, line]
            opp_piece = cls.ChessGame.players[inv_c(piece.color)].get_piece(coord)

            if opp_piece:
                if opp_piece.name == 'pawn' and opp_piece.just_moved:
                    # dont return the coord of the pawn -> return the coord where the pawn "should" go
                    return (coord[0], coord[1] + dy)
            
            coord = [piece.coord[0] - 1, line]
            opp_piece = cls.ChessGame.players[inv_c(piece.color)].get_piece(coord)

            if opp_piece:
                if opp_piece.name == 'pawn' and opp_piece.just_moved:
                    # dont return the coord of the pawn -> return the coord where the pawn "should" go
                    return (coord[0], coord[1] + dy)
        

    @classmethod
    def get_castle(cls, color):
        '''
        Return if can long castle, can short castle
        '''
        can_long_castle, can_short_castle = False, False

        if cls.is_setup_long_castle(color):
            can_long_castle = cls.check_kingcheck_long_castle(color)
        if cls.is_setup_short_castle(color):
            can_short_castle = cls.check_kingcheck_short_castle(color)
        
        return can_long_castle, can_short_castle

    @classmethod
    def check_kingcheck_long_castle(cls, color):
        line = cls.get_line(color)
        
        rock = cls.ChessGame.players[color].get_piece((0,line))
        king = cls.ChessGame.players[color].king
        # simul move and look if there's a check
        king.coord = (2,line)
        rock.coord = (3,line)
        is_check = cls.ChessGame.check_for_check(color, False)
        # reset coord
        king.coord = (4,line)
        rock.coord = (0,line)
        
        return not is_check

    @classmethod
    def is_setup_long_castle(cls, color):
        line = cls.get_line(color)

        # check if king is in right place
        if not cls.ChessGame.players[color].king.coord == (4, line):
            return

        # check king and rocks didn't move
        rock = cls.ChessGame.players[color].get_piece((0,line))
        if rock:
            if rock.name == 'rock' and not rock.moved and not cls.ChessGame.players[color].king.moved:
                # check that no piece are blocking
                for i in range(3):
                    piece = cls.ChessGame.players[color].get_piece((1+i, line))
                    if piece:
                        return
                return True
        
    @classmethod
    def is_setup_short_castle(cls, color):
        line = cls.get_line(color)
        
        # check if king is in right place
        if not cls.ChessGame.players[color].king.coord == (4, line):
            return

        # check king and rocks didn't move
        rock = cls.ChessGame.players[color].get_piece((7,line))
        if rock:
            if rock.name == 'rock' and not rock.moved and not cls.ChessGame.players[color].king.moved:
                # check that no piece are blocking
                for i in range(2):
                    piece = cls.ChessGame.players[color].get_piece((6-i, line))
                    if piece:
                        return
                return True
    
    @classmethod
    def check_kingcheck_short_castle(cls, color):
        line = cls.get_line(color)
        
        rock = cls.ChessGame.players[color].get_piece((7,line))
        king = cls.ChessGame.players[color].king
        # simul move and look if there's a check
        king.coord = (6,line)
        rock.coord = (5,line)
        is_check = cls.ChessGame.check_for_check(color, False)
        # reset coord
        king.coord = (4,line)
        rock.coord = (7,line)
        if is_check:
            # check so can't move piece
            return False
        return True