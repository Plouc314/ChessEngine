
class Tests:
    MSG_LENGTH = 20

    @classmethod
    def run(cls, Game):
        cls.test_setup(Game)
        cls.test_move(Game)
        cls.test_display(Game)

    @classmethod
    def exec_test(cls, name, cond):
        if cond:
            cls.print(name, 'passed')
        else:
            cls.print(name, 'failed')

    @classmethod
    def test_setup(cls, Game):
        # verify that Game and LivePlay have the same players
        cond = Game.players['white'] is Game.controls['white'].player
        cls.exec_test('player white', cond)

        cond = Game.players['black'] is Game.controls['black'].player
        cls.exec_test('player black', cond)

    @classmethod
    def test_move(cls, Game):
        # verify that piece movement work
        name = 'piece movement '

        # get a piece (pawn)
        pawn = Game.get_piece((0,6))

        # move the piece
        Game.handeln_movement(pawn, (0,4))

        # verify that new coord are correct
        cond = pawn.coord == (0,4)

        cls.exec_test(name+'1' ,cond)

        # verify that coord in player is correct

        # get player
        player = Game.players['white']

        try:
            player_pawn = player.get_piece((0,4))
        except:
            cls.print(name+'2', 'failed')

        # get player of control
        control_player = Game.controls['white'].player

        try:
            control_player_pawn = control_player.get_piece((0,4))
        except:
            cls.print(name+'2', 'failed')

        cond = pawn.coord == player_pawn.coord == control_player_pawn.coord

        cls.exec_test(name+'2', cond)

        cond = pawn is player_pawn and pawn is control_player_pawn

        cls.exec_test(name+'3', cond)

        # reset piece attributs
        pawn.coord = (0,6)
        pawn.moved = False

    @classmethod
    def test_display(cls, Game):
        # verifiy that display of player work
        name = 'display '

        player = Game.players['white']

        # get a piece (pawn)
        pawn = player.get_piece((0,6))

        # move the piece
        done = Game.handeln_movement(pawn, (0,4))

        # display the piece
        try:
            pawn.display()
            cls.print(name+'1','passed')
        except:
            cls.print(name+'1','failed')

        # verify the coord
        cond = pawn.coord == (0,4)
        
        cls.exec_test(name+'2', cond)

        # reset piece attributs
        pawn.coord = (0,6)
        pawn.moved = False
        

    @classmethod
    def print(cls, test_name, r):
        while len(test_name) < cls.MSG_LENGTH:
            test_name += ' '
        
        test_name += ':'
        
        theme = '[TEST]'

        print(theme, test_name, r)