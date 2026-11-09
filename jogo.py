def criar_tabuleiro_grande():
  tab = []
  for i in range(9):
    tabuleiroPequeno = {
      "id": i,
      "vencedor": None,
      "tabuleiro": [' '] * 9
    }
    tab.append(tabuleiroPequeno)
  tab[0]["tabuleiro"][0] = 'x'
  tab[2]["tabuleiro"][5] = 'o'
  tab[4]["tabuleiro"][4] = 'x'
  return tab

def mostrar_tabuleiro(tab):
    # print('  1 | 2 | 3 || 4 | 5 | 6 || 7 | 8 | 9 ')
    count = 0

    for bloco_tab in range(0, 9, 3):
        for sublinha in range(0, 9, 3):
            print(count + 1, end='')
            for i in range(3):
                # idx_tabuleiro = bloco_tab + i
                casas = tab[idx_tabuleiro]["tabuleiro"][sublinha : sublinha + 3]
                
                print(' ' + ' | '.join(casas) + ' ', end='')
                if i < 2:
                    print('||', end='')
            if count == 8:
                print()
                break
            if count % 3 == 2:
                print('\n ===========++===========++===========')
            else:
                print('\n ---+---+---||---+---+---||---+---+---')

            count += 1

def verificar_vitoria(tabuleiro: list):
  # validar linhas
  for i in range(3):
    if tabuleiro[i * 3] == tabuleiro[i * 3 + 1] == tabuleiro[i * 3 + 2] != ' ':
      return True
  # validar colunas
  for i in range(3):
    if tabuleiro[i] == tabuleiro[i + 3] == tabuleiro[i + 6] != ' ':
      return True
  # validar diagonais
  if tabuleiro[0] == tabuleiro[4] == tabuleiro[8] != ' ':
    return True
  if tabuleiro[2] == tabuleiro[4] == tabuleiro[6] != ' ':
    return True
  return False

def realizar_jogada():

  return

def mostrar_regras():
  return

def finalizar_jogo():
  return

def main():
  mostrar_tabuleiro(criar_tabuleiro_grande())
  print("Escolha uma opção")
  print("1: Iniciar jogo")
  print("2: Ver regras do jogo")
  print("3: Finalizar jogo")
  


main()
