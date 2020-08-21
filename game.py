from pieces import Pawn, Bishop, King, Queen, Rock, Knight
from move import PossibleMove


# classic pieces placement
white_config = [
    {'name':'pawn','coord':(0,6),'c':'white'},
    {'name':'pawn','coord':(1,6),'c':'white'},
    {'name':'pawn','coord':(2,6),'c':'white'},
    {'name':'pawn','coord':(3,6),'c':'white'},
    {'name':'pawn','coord':(4,6),'c':'white'},
    {'name':'pawn','coord':(5,6),'c':'white'},
    {'name':'pawn','coord':(6,6),'c':'white'},
    {'name':'pawn','coord':(7,6),'c':'white'},
    {'name':'king','coord':(4,7),'c':'white'},
    {'name':'bishop','coord':(2,7),'c':'white'},
    {'name':'bishop','coord':(5,7),'c':'white'},
    {'name':'knight','coord':(1,7),'c':'white'},
    {'name':'knight','coord':(6,7),'c':'white'},
    {'name':'rock','coord':(0,7),'c':'white'},
    {'name':'rock','coord':(7,7),'c':'white'},
    {'name':'queen','coord':(3,7),'c':'white'},
]

black_config = [
    {'name':'pawn','coord':(0,1),'c':'black'},
    {'name':'pawn','coord':(1,1),'c':'black'},
    {'name':'pawn','coord':(2,1),'c':'black'},
    {'name':'pawn','coord':(3,1),'c':'black'},
    {'name':'pawn','coord':(4,1),'c':'black'},
    {'name':'pawn','coord':(5,1),'c':'black'},
    {'name':'pawn','coord':(6,1),'c':'black'},
    {'name':'pawn','coord':(7,1),'c':'black'},
    {'name':'king','coord':(4,0),'c':'black'},
    {'name':'bishop','coord':(2,0),'c':'black'},
    {'name':'bishop','coord':(5,0),'c':'black'},
    {'name':'knight','coord':(1,0),'c':'black'},
    {'name':'knight','coord':(6,0),'c':'black'},
    {'name':'rock','coord':(0,0),'c':'black'},
    {'name':'rock','coord':(7,0),'c':'black'},
    {'name':'queen','coord':(3,0),'c':'black'},
]

class Player:
    '''
    Store and display piece of player
    '''
    in_check = False
    def __init__(self, config):
        self.create_pieces(config)

    def create_pieces(self, config):
        self.pieces = []
        self.king = None
        for pdict in config:
            if pdict['name'] == 'pawn':
                pawn = Pawn(pdict['coord'], pdict['c'])
                self.pieces.append(pawn)
            elif pdict['name'] == 'bishop':
                bishop = Bishop(pdict['coord'], pdict['c'])
                self.pieces.append(bishop)
            elif pdict['name'] == 'queen':
                queen = Queen(pdict['coord'], pdict['c'])
                self.pieces.append(queen)
            elif pdict['name'] == 'rock':
                rock = Rock(pdict['coord'], pdict['c'])
                self.pieces.append(rock)
            elif pdict['name'] == 'knight':
                knight = Knight(pdict['coord'], pdict['c'])
                self.pieces.append(knight)
            elif pdict['name'] == 'king':
                king = King(pdict['coord'], pdict['c'])
                self.pieces.append(king)
                self.king = king
        
        # get player's color
        self.color = self.king.color

    def get_piece(self, coord):
        for piece in self.pieces:
            if piece.coord[0] == coord[0] and piece.coord[1] == coord[1]:
                return piece    

    def get_piece_by_name(self, name):
        for piece in self.pieces:
            if piece.name == name:
                return piece

    def display(self):
        '''Piece.display must be implemented'''
        for piece in self.pieces:
            piece.display()

def inv_c(color):
    if color == 'white':
        return 'black'
    else:
        return 'white'

class ChessGame:
    '''
    Manage game: Execute turns, check game's end, use move's Objects to handeln piece movements

    Can set control objects:
        LivePlay
        bruteforce.Agent (in dev)
        other: must have play_turn(), promote(piece) methods
    
    Set start configuration:
        pass configurations in set_players() methods
    
    Can set a menu:
        update at each end of turn
        call menu attribute: pass color and n pos moves
    '''
    menu = None
    # conf - change white/black conf to change pieces a start
    white_config = white_config
    black_config = black_config
    # func that are execute when players play
    controls = None
    control_white = None
    control_black = None
    last_move = None
    
    @classmethod
    def init(cls, players):
        # set or reset Game states
        cls.turn = True
        cls.winner = None
        cls.ended = False
        cls.players = players
        if cls.controls:
            cls.controls['white'].set_player(players['white'])
            cls.controls['black'].set_player(players['black'])

        # set ChessGame/players in other 'static' object
        PossibleMove.ChessGame = cls
            
    @classmethod
    def set_players(cls, white_config=None, black_config=None):
        '''If no arguments: classic set up'''
        
        if not white_config:
            white_player = Player(cls.white_config)
        else:
            white_player = Player(white_config)
            cls.white_config = white_config
        
        if not black_config:
            black_player = Player(cls.black_config)
        else:
            black_player = Player(black_config)
            cls.black_config = black_config

        cls.init({'white':white_player, 'black':black_player})

    @classmethod
    def set_control_methods(cls, control_white, control_black):
        cls.control_white = control_white
        cls.control_black = control_black
        cls.controls = {'white':cls.control_white, 'black':cls.control_black}
        # check that on turn methods are set
        if not cls.control_white or not cls.control_black:
            raise ValueError('ChessGame: must set on_turn methods.')

    @classmethod
    def play_turn(cls):
        # execute turn
        if cls.turn:
            cls.control_white.play_turn()
        else:
            cls.control_black.play_turn()

    @classmethod
    def check_for_check(cls, color, kingcheck=True):
        '''Check if king is attacked by an opponent piece'''
        king_coord = cls.players[color].king.coord
        # check if king coord is attack by an opponent piece
        for piece in cls.players[inv_c(color)].pieces:
            if king_coord in PossibleMove.get(piece, True, kingcheck=kingcheck):
                return True

    @classmethod
    def handeln_movement(cls, piece, coord):
        '''Handeln pieces movement'''
        
        coord = tuple(coord)
        is_attacking = cls.is_attacking(piece, coord)

        # first look for castle
        if piece.name == 'king':
            if cls.check_castle_moves(piece):
                return True
        
        if cls.check_can_move(piece, coord, is_attacking):
            cls.move(piece, coord, is_attacking)
            return True

    @classmethod
    def is_attacking(cls, piece, coord):
        if cls.players[inv_c(piece.color)].get_piece(coord):
            return True

    @classmethod
    def check_can_move(cls, piece, coord, is_attacking):
        '''
        Check if the given piece can move at the given destination
        '''
        # first check if other pieces on coord
        if cls.players[piece.color].get_piece(coord):
            # other piece of same color on destination case -> can't move
            return False

        if coord in PossibleMove.get(piece, is_attacking):
            return True
        

    @classmethod
    def move(cls, piece, coord, is_attacking):
        '''
        Play the given move
        '''
        if is_attacking:
            # remove the attacked piece
            attacked_piece = cls.get_piece(coord)
            cls.players[attacked_piece.color].pieces.remove(attacked_piece)
                
        # store last move
        cls.last_move = (piece.coord, coord)

        # move piece
        piece.move(coord)

        # look for pawn promotion
        if piece.name == 'pawn':
            cls.check_pawn_promotion(piece)
        
        # pass the turn
        cls.end_turn(piece.color)

    @classmethod
    def check_castle_moves(cls, king):
        line = PossibleMove.get_line(king.color)
        
        can_long, can_short = PossibleMove.get_castle(king.color)

        if can_long:
            rock = cls.players[king.color].get_piece((0, line))
            # execute long castle
            king.move((2,line))
            rock.move((3, line))
            # pass a turn
            cls.end_turn(king.color)
            return True
        
        if can_short:
            rock = cls.players[king.color].get_piece((7, line))
            # execute short castle
            king.move((6,line))
            rock.move((5, line))
            # pass a turn
            cls.end_turn(king.color)
            return True

    @classmethod
    def check_pawn_promotion(cls, piece):
        '''Check if pawn is promoting -> exec control: promote(piece) func'''
        # line of promotion
        line = PossibleMove.get_line(inv_c(piece.color))

        if piece.y == line:
            # promote
            cls.controls[piece.color].promote(piece)

    @classmethod
    def get_possibles_moves(cls, piece):
        '''Get all possible moves (for a piece)'''
        if piece.name == 'pawn':
            movements = PossibleMove.get(piece, False) # for pawn attacking and non-attacking moves are completely differents
            attacks = PossibleMove.get(piece, True)
            for coord in attacks:
                if cls.players[inv_c(piece.color)].get_piece(coord):
                    movements.append(coord)
        else:
            movements = PossibleMove.get(piece, True) # get movements as if the piece was attacking -> include capture moves
        return movements

    @classmethod
    def get_piece(cls, coord):
        '''Return piece corresponding coord (of both color)'''
        piece = cls.players['white'].get_piece(coord)
        if piece:
            return piece
        piece = cls.players['black'].get_piece(coord)
        if piece:
            return piece

    @classmethod
    def end_turn(cls, color):
        cls.turn = not cls.turn
        # check if the game is over
        cls.check_end_game(inv_c(color))

    @classmethod
    def check_end_game(cls, color):
        poss_moves = []
        # get every possible moves for the player
        for piece in cls.players[color].pieces:
            pmoves = cls.get_possibles_moves(piece)
            poss_moves.extend(pmoves)
        
        if cls.menu:
            # send turn infos to menu
            cls.menu(color, len(poss_moves))

        if not poss_moves: # player can't move
            if cls.check_for_check(color): # if player in check and can't move -> checkmate
                cls.winner = inv_c(color)
            else: # player can't move but not in check -> stalemate
                pass
            cls.ended = True

    @classmethod
    def get_board_state(cls):
        '''Return dict with coord x,y, piecename,color for each case'''
        coords_states = []
        for x in range(8):
            for y in range(8):
                piece = cls.get_piece((x,y))
                if piece:
                    d = {'x':x,'y':y,'piece':piece.name,'color':piece.color}
                else:
                    d = {'x':x,'y':y,'piece':None,'color':None}
                coords_states.append(d)
        return coords_states

    @classmethod
    def display(cls):
        '''If display method of Piece is implemented: display pieces'''
        cls.players['white'].display()
        cls.players['black'].display()
        
