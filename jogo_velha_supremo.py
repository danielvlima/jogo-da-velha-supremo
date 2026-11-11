# Jogo da Velha Supremo - TCC00355 Laboratorio de Resolucao de Problemas
# Integrantes: Daniel Lima Verginio e Larissa Soares Reis
import sys

def criar_tabuleiro():
  #tabuleiro grande = lista com 9 tabuleiros pequenos (indices 0 a 8, da esquerda pra direita, de cima pra baixo)
  #"vencedor" guarda o estado do tabuleiro pequeno: None = em andamento, 'x' ou 'o' = ganho, 'velha' = empatado
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
    "estado": "EM_ANDAMENTO",
    "tabuleiro": criar_tabuleiro(),
    "jogadores": {'x': '', 'o': ''},
    "destino": None, #indice do tabuleiro pequeno onde o proximo jogador deve jogar, None = escolha livre
    "vencedor": None, #'x', 'o' ou 'velha' quando a partida termina
    "historico": []
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

def mostrar_vencedores(tab):
  #mostra quem ja ganhou cada tabuleiro pequeno, como se fosse o tabuleiro grande
  print("Tabuleiros ganhos ( - = deu velha):")
  for linha in range(3):
    simbolos = []
    for coluna in range(3):
      vencedor = tab[linha * 3 + coluna]["vencedor"]
      if vencedor is None:
        simbolos.append(' ')
      elif vencedor == 'velha':
        simbolos.append('-')
      else:
        simbolos.append(vencedor)
    print(' ' + ' | '.join(simbolos))
    if linha < 2:
      print('---+---+---')
  print()

def posicao(linha, coluna):
  #converte linha e coluna (1 a 3) para o indice da lista (0 a 8)
  return (linha - 1) * 3 + (coluna - 1)

def linha_coluna(indice):
  #faz o caminho contrario de posicao: indice (0 a 8) para linha e coluna (1 a 3)
  return indice // 3 + 1, indice % 3 + 1

def verificar_vencedor(tabuleiro, caractere):
  #verifica no array as condicoes de vitoria (linhas, colunas e diagonais), retorna True se o caractere venceu
  #serve para o tabuleiro pequeno e tambem para a lista de vencedores do tabuleiro grande
  for i in range(3):
    if all(tabuleiro[i * 3 + j] == caractere for j in range(3)):
      return True
    if all(tabuleiro[j * 3 + i] == caractere for j in range(3)):
      return True
  if all(tabuleiro[i * 4] == caractere for i in range(3)): #diagonal principal: 0, 4, 8
    return True
  if all(tabuleiro[i * 2 + 2] == caractere for i in range(3)): #diagonal secundaria: 2, 4, 6
    return True
  return False

def tabuleiro_cheio(tabuleiro):
  return ' ' not in tabuleiro

def atualizar_tabuleiro_pequeno(tab, indiceGrande, jogador):
  #depois de uma jogada, verifica so o tabuleiro pequeno onde ela foi feita
  #(os outros nao mudaram, e um tabuleiro ja ganho nunca troca de dono)
  tabuleiroPequeno = tab[indiceGrande]
  if verificar_vencedor(tabuleiroPequeno["tabuleiro"], jogador):
    tabuleiroPequeno["vencedor"] = jogador
  elif tabuleiro_cheio(tabuleiroPequeno["tabuleiro"]):
    tabuleiroPequeno["vencedor"] = 'velha'

def verificar_vitoria_grande(tabuleiro, jogador):
  #monta a lista de vencedores dos tabuleiros pequenos e verifica se o jogador fez 3 em linha nela
  tabuleiro_vencedores = [tabuleiro[i]["vencedor"] for i in range(9)]
  return verificar_vencedor(tabuleiro_vencedores, jogador)

def partida_empatada(tab):
  #empata quando todos os tabuleiros pequenos foram decididos (ganhos ou velha) sem vencedor no grande
  return all(tab[i]["vencedor"] is not None for i in range(9))

def proximo_destino(tab, indicePequeno):
  #regra do destino: a casa jogada indica o tabuleiro do adversario
  #se esse tabuleiro ja foi decidido, a escolha fica livre (None)
  if tab[indicePequeno]["vencedor"] is None:
    return indicePequeno
  return None

def converter_jogada(jogada, destino):
  #transforma a string ja validada nos indices (tabuleiro grande, casa do pequeno)
  numeros = [int(numero) for numero in jogada.split()]
  if destino is None:
    indiceGrande = posicao(numeros[0], numeros[1])
    indicePequeno = posicao(numeros[2], numeros[3])
  else:
    indiceGrande = destino
    indicePequeno = posicao(numeros[0], numeros[1])
  return indiceGrande, indicePequeno

def validar_jogada(tab, jogada, destino):
  #escolha livre: "LG CG L C" (4 numeros), destino definido: "L C" (2 numeros)
  quantidade = 4 if destino is None else 2
  partes = jogada.split()
  if len(partes) != quantidade:
    print(f"Jogada inválida. Digite {quantidade} números separados por espaço.")
    return False
  for parte in partes:
    #isdecimal e nao isdigit: isdigit aceita '²', que quebra o int()
    if not parte.isdecimal():
      print("Jogada inválida. Digite apenas números.")
      return False
    if int(parte) < 1 or int(parte) > 3:
      print("Jogada inválida. Digite números entre 1 e 3.")
      return False
  indiceGrande, indicePequeno = converter_jogada(jogada, destino)
  if tab[indiceGrande]["vencedor"] is not None:
    print("Esse tabuleiro já foi decidido. Escolha outro tabuleiro.")
    return False
  if tab[indiceGrande]["tabuleiro"][indicePequeno] != ' ':
    print("Posição já ocupada. Escolha outra posição.")
    return False
  return True

def realizar_jogada(partida, jogador):
  tab = partida["tabuleiro"]
  destino = partida["destino"]
  print(f"Vez de {partida['jogadores'][jogador]} ({jogador.upper()}).")
  if destino is None:
    print("Escolha livre: jogue em qualquer tabuleiro que ainda esteja em andamento.")
    mensagem = "Digite linha e coluna do tabuleiro e linha e coluna da casa (LG CG L C): "
  else:
    linhaDestino, colunaDestino = linha_coluna(destino)
    print(f"Jogue no tabuleiro {linhaDestino},{colunaDestino}.")
    mensagem = "Digite linha e coluna da casa (L C): "
  while True:
    jogada = input(mensagem)
    if validar_jogada(tab, jogada, destino):
      indiceGrande, indicePequeno = converter_jogada(jogada, destino)
      tab[indiceGrande]["tabuleiro"][indicePequeno] = jogador
      break
  return indiceGrande, indicePequeno

def registrar_jogada(partida, jogador, indiceGrande, indicePequeno):
  #guarda a jogada no historico, ex.: "3. Miguel (X): tabuleiro 2,2 / casa 1,3"
  numero = len(partida["historico"]) + 1
  nome = partida["jogadores"][jogador]
  linhaGrande, colunaGrande = linha_coluna(indiceGrande)
  linhaPequeno, colunaPequeno = linha_coluna(indicePequeno)
  partida["historico"].append(f"{numero}. {nome} ({jogador.upper()}): tabuleiro {linhaGrande},{colunaGrande} / casa {linhaPequeno},{colunaPequeno}")

def mostrar_historico(historico):
  print("Histórico da partida:")
  if len(historico) == 0:
    print("Nenhuma partida jogada ainda.\n")
    return
  for jogada in historico:
    print(jogada)
  print()

def ler_nome(mensagem):
  #pede o nome ate o jogador digitar algo que nao seja vazio
  while True:
    nome = input(mensagem).strip()
    if nome != '':
      return nome
    print("O nome não pode ser vazio.")

def trocar_jogador(jogador):
  if jogador == 'x':
    return 'o'
  return 'x'

def mostrar_regras():
  print("Regras do jogo:")
  print("1. O jogo é jogado em um tabuleiro grande, que contém 9 tabuleiros pequenos (grade 3x3).")
  print("2. O jogador X começa e pode jogar em qualquer casa de qualquer tabuleiro pequeno.")
  print("3. A casa (linha, coluna) escolhida indica em qual tabuleiro pequeno o adversário deve jogar.")
  print("   Ex.: X jogou na casa 1,3 de qualquer tabuleiro, então O joga no tabuleiro 1,3.")
  print("4. Se esse tabuleiro já foi ganho ou está cheio, a escolha é livre.")
  print("5. Quem faz linha, coluna ou diagonal em um tabuleiro pequeno ganha esse tabuleiro.")
  print("   Tabuleiro pequeno cheio sem vencedor não é de ninguém.")
  print("6. Vence quem ganhar 3 tabuleiros pequenos em linha, coluna ou diagonal.")
  print("   Se todos forem decididos sem isso, a partida empata.")
  print("Como jogar (números de 1 a 3 separados por espaço):")
  print("- Tabuleiro definido: L C (linha e coluna da casa). Ex.: 2 3")
  print("- Escolha livre: LG CG L C (tabuleiro e depois casa). Ex.: 2 2 1 1 \n")
  return

def criar_placar():
  #placar da sessao: vitorias por nome de jogador e empates
  placar = {
    "vitorias": {},
    "empates": 0
  }
  return placar

def registrar_placar(placar, partida):
  for jogador in ['x', 'o']:
    nome = partida["jogadores"][jogador]
    if nome not in placar["vitorias"]:
      placar["vitorias"][nome] = 0
  if partida["vencedor"] == 'velha':
    placar["empates"] += 1
  else:
    placar["vitorias"][partida["jogadores"][partida["vencedor"]]] += 1

def mostrar_placar(placar):
  print("Placar da sessão:")
  if len(placar["vitorias"]) == 0:
    print("Nenhuma partida jogada ainda.\n")
    return
  for nome in placar["vitorias"]:
    print(f"{nome}: {placar['vitorias'][nome]} vitória(s)")
  print(f"Empates: {placar['empates']}\n")

def finalizar_jogo():
  print("Jogo finalizado. Até a próxima!")
  return

def limpar_tela():
    # \033[H = vai pro topo | \033[J = limpa o resto da tela
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

def jogar():
  limpar_tela()
  partida = criar_partida()
  tab = partida["tabuleiro"]
  partida["jogadores"]['x'] = ler_nome("Nome do jogador X: ")
  partida["jogadores"]['o'] = ler_nome("Nome do jogador O: ")
  #nomes iguais misturariam as vitorias dos dois no placar
  while partida["jogadores"]['o'] == partida["jogadores"]['x']:
    print("Os jogadores precisam ter nomes diferentes.")
    partida["jogadores"]['o'] = ler_nome("Nome do jogador O: ")

  jogador = 'x'
  while partida["estado"] == "EM_ANDAMENTO":
    limpar_tela()
    mostrar_tabuleiro(tab)
    mostrar_vencedores(tab)
    indiceGrande, indicePequeno = realizar_jogada(partida, jogador)
    registrar_jogada(partida, jogador, indiceGrande, indicePequeno)
    atualizar_tabuleiro_pequeno(tab, indiceGrande, jogador)

    if verificar_vitoria_grande(tab, jogador):
      partida["vencedor"] = jogador
      partida["estado"] = "FINALIZADO"
    elif partida_empatada(tab):
      partida["vencedor"] = 'velha'
      partida["estado"] = "FINALIZADO"
    else:
      partida["destino"] = proximo_destino(tab, indicePequeno)
      jogador = trocar_jogador(jogador)

  limpar_tela()
  mostrar_tabuleiro(tab)
  mostrar_vencedores(tab)
  if partida["vencedor"] == 'velha':
    print("Todos os tabuleiros foram decididos. A partida empatou!\n")
  else:
    print(f"{partida['jogadores'][jogador]} ({jogador.upper()}) venceu a partida!\n")
  mostrar_historico(partida["historico"])
  return partida

def main():
  placar = criar_placar()
  ultimaPartida = None
  while True:
    print("Escolha uma opção, digitando o número correspondente:")
    print("1: Iniciar jogo")
    print("2: Ver regras do jogo")
    print("3: Finalizar jogo")
    print("4: Ver placar")
    print("5: Ver histórico da última partida")
    input_usuario = input("Digite sua escolha: ")
    if input_usuario == "1":
      ultimaPartida = jogar()
      registrar_placar(placar, ultimaPartida)
    elif input_usuario == "2":
      limpar_tela()
      mostrar_regras()
    elif input_usuario == "3":
      limpar_tela()
      finalizar_jogo()
      break
    elif input_usuario == "4":
      limpar_tela()
      mostrar_placar(placar)
    elif input_usuario == "5":
      limpar_tela()
      if ultimaPartida is None:
        mostrar_historico([])
      else:
        mostrar_historico(ultimaPartida["historico"])
    else:
      print("Opção inválida. Digite um número de 1 a 5.\n")


main()
