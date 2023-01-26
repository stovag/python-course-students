class ClientMsgHello:
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __str__(self):
        return f'ClientMsgHello: {self.name}, {self.version}'

class ClientMsgExitServer:
    # Order the server to exit
    def __init__(self, msg, exit_id):
        self.msg = msg
        self.exit_id = exit_id

    def __str__(self):
        return f'ClientMsgExitServer: {self.msg}, {self.exit_id}'

class ServerMsgExitClient:
    # Order a client to exit
    def __init__(self, msg, exit_id):
        self.msg = msg
        self.exit_id = exit_id

    def __str__(self):
        return f'ServerMsgExitClient: {self.msg}, {self.exit_id}'

class ServerMsgHello:
    def __init__(self, name, client_id):
        self.name = name
        self.client_id = client_id

    def __str__(self):
        return f'ServerMsgHello: {self.name}, {self.client_id}'

class ServerMsgDuelReadyToStart:
    def __init__(self):
        pass

    def __str__(self):
        return f'ServerMsgDuelReadyToStart'

class ServerMsgRoundStart:
    def __init__(self, round_num):
        self.round_num = round_num

    def __str__(self):
        return f'ServerMsgRoundStart: {self.round_num}'

class ServerMsgPrepareForNextRound:
    def __init__(self, round_num):
        self.round_num = round_num

    def __str__(self):
        return f'ServerMsgPrepareForNextRound: {self.round_num}'

class ClientMsgRoundMove:
    def __init__(self, move):
        self.move = move

    def __str__(self):
        return f'ClientMsgRoundMove: {self.move}'

class ClientMsgOK:
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f'ClientMsgOK: {self.msg}'

class ServerMsgRoundResult:
    def __init__(self, player_one_id, player_one_move, player_two_id, player_two_move, result):
        self.player_one_id = player_one_id
        self.player_one_move = player_one_move
        self.player_two_id = player_two_id
        self.player_two_move = player_two_move
        self.result = result

    def __str__(self):
        return f'ServerMsgRoundResult: {self.player_one_id}, {self.player_one_move}, {self.player_two_id}, {self.player_two_move}, {self.result}'