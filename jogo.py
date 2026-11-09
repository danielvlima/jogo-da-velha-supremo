import sys
ESTADOS = {
    "AGUARDANDO_INICIO": "AGUARDANDO_INICIO",
    "EM_ANDAMENTO": "EM_ANDAMENTO",
    "FINALIZADO": "FINALIZADO"
}
def criar_tabuleiro():
  tabuleiroGrande = []
  for i in range(9):
    tabuleiroPequeno = {
      "id": i,
      "vencedor": None,
      "tabuleiro": [' '] * 9
    }
    tabuleiroGrande.append(tabuleiroPequeno)
  return tabuleiroGrande

def criar_partida():
  partida = {
    "estado": ESTADOS["EM_ANDAMENTO"],
    "tabuleiro": criar_tabuleiro()
  }
  return partida

def mostrar_tabuleiro(tab):
    print('\n =====================================')
    count = 0

    for bloco_tab in range(0, 9, 3):
        for sublinha in range(0, 9, 3):
            print(' ', end='')
            for i in range(3):
                idx_tabuleiro = bloco_tab + i
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
    print(' =====================================')

def verificar_vitoria_grande(tabuleiro, jogador):
  #verifica vitoria em cada tabuleiro pequeno e atualiza o vencedor para x ou o dependendo do jogador que venceu
  vencedor = None
  for i in range(9):
    if verificar_vencedor(tabuleiro[i]["tabuleiro"], jogador):
      tabuleiro[i]["vencedor"] = jogador
  tabuleiro_vencedores = [tabuleiro[i]["vencedor"] for i in range(9)]

  verificar_vencedor(tabuleiro_vencedores, jogador)
  if verificar_vencedor(tabuleiro_vencedores, jogador):
    vencedor = jogador
  print(f"Vencedor do tabuleiro grande: {vencedor}")
  return vencedor

def verificar_vencedor(tabuleiro, caractere):
  #verifica no array as condicoes de vitoria venceu e retorna o vencedor, caso não haja vencedor retorna None
  for i in range(3):
    if all(tabuleiro[i * 3 + j] == caractere for j in range(3)):
      return True
    if all(tabuleiro[j * 3 + i] == caractere for j in range(3)):
      return True
  return False

def validar_jogada(tab, jogada):
  if len(jogada.split()) != 2:
    print("Jogada inválida. Digite dois números separados por espaço.")
    return False
  if not jogada.split()[0].isdigit() or not jogada.split()[1].isdigit():
    print("Jogada inválida. Digite apenas números.")
    return False
  jogadaGrande, jogadaPequeno = int(jogada.split()[0]), int(jogada.split()[1])
  if jogadaGrande < 1 or jogadaGrande > 9 or jogadaPequeno < 1 or jogadaPequeno > 9:
    print("Jogada inválida. Digite números entre 1 e 9 para o tabuleiro grande e 1 e 9 para o tabuleiro pequeno.")
    return False
  if tab[jogadaGrande - 1]["tabuleiro"][jogadaPequeno - 1] != ' ':
    print("Posição já ocupada. Escolha outra posição.")
    return False
  return True

def realizar_jogada(tab, jogador): 
  while True:
    jogada = input("Vez do jogador " + jogador + ", escolha a posição do tabuleiro grande (1-9), a posição do tabuleiro pequeno (1-9):")
    if validar_jogada(tab, jogada):
      jogada1, jogada2 = int(jogada.split()[0]), int(jogada.split()[1])
      tab[jogada1 - 1]["tabuleiro"][jogada2 - 1] = jogador
      break
  return tab

def mostrar_regras():
  print("Regras do jogo:")
  print("1. O jogo é jogado em um tabuleiro grande, que contém 9 tabuleiros pequenos.")
  print("2. Cada jogador escolhe um símbolo (X ou O) e joga alternadamente.")
  print("3. Para fazer uma jogada, o jogador deve escolher um tabuleiro pequeno e uma posição dentro desse tabuleiro. \n")
  return

def finalizar_jogo():
  exit()
  return

def limpar_tela():
    # \033[H = vai pro topo | \033[J = limpa o resto da tela
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

def jogar():
  limpar_tela()
  partida = criar_partida()
  tab = partida["tabuleiro"]
  mostrar_tabuleiro(tab)
  while partida["estado"] == "EM_ANDAMENTO":
    tab = realizar_jogada(tab, 'x')
    limpar_tela()
    verificar_vitoria_grande(tab, 'x')
    mostrar_tabuleiro(tab)
    if verificar_vitoria_grande(tab, 'x'):
      print("Jogador X venceu!")
      break
    tab = realizar_jogada(tab, 'o')
    limpar_tela()
    verificar_vitoria_grande(tab, 'o')
    mostrar_tabuleiro(tab)
    if verificar_vitoria_grande(tab, 'o'):
      print("Jogador O venceu!")
      break
    limpar_tela()
    mostrar_tabuleiro(tab)
  return

def main():
  print("Escolha uma opção, digitando o número correspondente:")
  print("1: Iniciar jogo")
  print("2: Ver regras do jogo")
  print("3: Finalizar jogo")
  input_usuario = input("Digite sua escolha: ")
  if input_usuario == "1":
    limpar_tela()
    jogar()
  elif input_usuario == "2":
    limpar_tela()
    mostrar_regras()
    main()
  elif input_usuario == "3":
    limpar_tela()
    finalizar_jogo()
  else:
    print("Opção inválida. Encerrando o jogo.")  
    finalizar_jogo()


main()
