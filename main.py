from math import inf as infinity
import random
import gym
import gym_tictactoe


# Configurações
O = -1 # Usuário
X = +1 # IA
env = gym.make("TicTacToe-v1", symbols=[X, O])
env.reset()

def victory(last_state, player):
    win_state = [
        [last_state[0], last_state[1], last_state[2]],
        [last_state[3], last_state[4], last_state[5]],
        [last_state[6], last_state[7], last_state[8]],
        [last_state[0], last_state[3], last_state[6]],
        [last_state[1], last_state[4], last_state[7]],
        [last_state[2], last_state[5], last_state[8]],
        [last_state[0], last_state[4], last_state[8]],
        [last_state[2], last_state[4], last_state[6]],
    ]
    
    if [player, player, player] in win_state:
        return True
    else:
        return False
    
def gameOver(last_state):
    return victory(last_state, O) or victory(last_state, X)

def scoreMinMax(last_state):
    
    if victory(last_state, X):
        score = +1
    elif victory(last_state, O):
        score = -1
    else:
        score = 0

    return score


def emptyCells(last_state):
    cells = []
    for i in range(len(last_state)):
        if last_state[i] == 0:
            cells.append(i)
    return cells
            

def minmax(player, last_state, depth):
    
    if player == X:
        best = [-1, -infinity]
    else:
        best = [-1, +infinity]

    if depth == 0 or gameOver(last_state):
        score = scoreMinMax(last_state)
        return [-1, score]

    for cell in emptyCells(last_state):
        last_state[cell] = player
        score = minmax(-player, last_state, depth - 1)
        last_state[cell] = 0
        score[0] = cell

        if player == X:
            if score[1] > best[1]:
                best = score
        else:
            if score[1] < best[1]:
                best = score
    
    return best


def action_O(last_state):
    '''
        Gera a ação do usuário.
        last_state = lista de ações realizadas
    '''
    options = [i for i in range(len(last_state)) if last_state[i] == 0]
    print('Options: %s' % options)
    action = int(input('Select a option: '))
    while not action in options:
        action = int(input('Select a option: '))
    return action

def action_X(last_state):
    '''
        Gera a ação da IA.
        Inicialmente é aleatória
        last_state = lista de ações realizadas
    '''
    depth = len(emptyCells(last_state))

    if depth == 0 or gameOver(last_state):
        return

    if depth == 9:
        options = [i for i in range(len(last_state)) if last_state[i] == 0]
        return random.choice(options)
    else:
        setMove = minmax(X, last_state, depth)
        action = setMove[0]
    return action 

# Define o usuário da vez
user = O
# Ultimo estado
last_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
# Inicia o jogo
env.render(mode=None)
while True:
    # Cada usuário tem estratégias diferentes
    if user == O:
        action = action_O(last_state)
    else:
        action = action_X(last_state)

    print('Play: %s Action: %s' % ('O' if user == O else 'X', action))
    state, reward, done, infos = env.step(action, user)
    print(state, reward, done, infos)
    env.render(mode=None)

    # Se terminou mostra o placar
    if done:
        if reward == 10:
            print("Draw !")
        else:
            print("User %s wins! Reward : %s" % ('O' if user == O else 'X', reward, ))
        env.reset()
        break
    # Muda o usuário
    user = O if user == X else X
    last_state = state
env.close()