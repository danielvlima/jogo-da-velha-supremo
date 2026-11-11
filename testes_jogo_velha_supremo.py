# Testes do Jogo da Velha Supremo
# Integrantes: Daniel Lima Vergilio e Larissa Soares Reis
#
# Como rodar (na pasta do projeto):
#   python testes_jogo_velha_supremo.py                    -> roda todos os testes
#   python testes_jogo_velha_supremo.py --partida          -> mostra uma partida simulada inteira
#   python testes_jogo_velha_supremo.py --partida --pausar -> mesma partida, Enter a cada jogada
#
# Este arquivo NAO faz parte da entrega; serve para conferir e apresentar o jogo.
import contextlib
import io
import sys

ARQUIVO_JOGO = 'jogo_velha_supremo.py'

total_testes = 0
testes_ok = 0

# Partida em que X ganha a diagonal do tabuleiro grande (tabuleiros 1,1 / 2,2 / 3,3).
# A jogada 34 cai em escolha livre (4 numeros).
PARTIDA_VITORIA_X = [
  '1 1 1 1', '2 2', '1 1', '3 3', '1 1', '1 2', '1 2', '1 1', '1 3', '1 1',
  '2 1', '1 1', '2 3', '1 1', '3 1', '2 2', '2 2', '3 3', '2 2', '1 2',
  '1 3', '2 2', '1 3', '1 2', '2 1', '2 2', '2 1', '1 2', '2 3', '2 2',
  '2 3', '1 2', '2 2', '1 3 2 1', '1 3', '3 3', '3 3',
]

# ---------------------------------------------------------------------------
# Ferramentas dos testes
# ---------------------------------------------------------------------------

def carregar_jogo():
  #o jogo termina com a chamada main(), que abriria o menu. Para testar as funcoes,
  #lemos o codigo, tiramos essa ultima chamada e executamos o resto
  with open(ARQUIVO_JOGO, encoding='utf-8') as arquivo:
    codigo = arquivo.read()
  codigoSemMain = codigo.rsplit('main()', 1)[0]
  funcoes = {}
  exec(codigoSemMain, funcoes)
  return funcoes

def titulo(texto):
  print()
  print('=' * 60)
  print(' ' + texto)
  print('=' * 60)

def conferir(descricao, condicao):
  global total_testes, testes_ok
  total_testes += 1
  if condicao:
    testes_ok += 1
    print(f'  [OK]     {descricao}')
  else:
    print(f'  [FALHOU] {descricao}')

def entradas_simuladas(jogo, respostas, mostrar=False, pausar=False):
  #troca o input() do jogo por uma lista de respostas prontas, como se alguem estivesse digitando
  fila = list(respostas)

  def input_falso(mensagem=''):
    if not fila:
      raise RuntimeError('O jogo pediu mais entradas do que o teste preparou.')
    resposta = fila.pop(0)
    if mostrar:
      if pausar:
        input('   (Enter para a proxima jogada)')
      print(mensagem + resposta)
    return resposta

  jogo['input'] = input_falso
  return fila

def rodar_em_silencio(funcao, *argumentos):
  #executa a funcao escondendo o que ela imprime; devolve (retorno, texto impresso)
  saida = io.StringIO()
  with contextlib.redirect_stdout(saida):
    retorno = funcao(*argumentos)
  return retorno, saida.getvalue()

def jogada_valida(jogo, tab, texto, destino):
  valido, _ = rodar_em_silencio(jogo['validar_jogada'], tab, texto, destino)
  return valido

# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

def testar_criacao(jogo):
  titulo('1. Criacao do tabuleiro')
  tab = jogo['criar_tabuleiro']()
  conferir('tabuleiro grande tem 9 tabuleiros pequenos', len(tab) == 9)
  conferir('cada pequeno tem 9 casas vazias e comeca sem vencedor',
           all(tab[i]["tabuleiro"] == [' '] * 9 and tab[i]["vencedor"] is None for i in range(9)))
  #se as listas fossem copias da mesma, mudar uma casa mudaria varias
  tab[0]["tabuleiro"][0] = 'x'
  marcadas = sum(tab[i]["tabuleiro"].count('x') for i in range(9))
  conferir('marcar uma casa muda SO aquela casa (listas independentes)', marcadas == 1)
  conferir('posicao(linha, coluna) converte 1..3 para indice 0..8',
           jogo['posicao'](1, 1) == 0 and jogo['posicao'](2, 3) == 5 and jogo['posicao'](3, 3) == 8)
  conferir('linha_coluna(indice) faz o caminho contrario',
           jogo['linha_coluna'](5) == (2, 3) and jogo['linha_coluna'](0) == (1, 1))

def testar_vencedor(jogo):
  titulo('2. Vencedor (tabuleiro pequeno e lista do grande)')
  v = jogo['verificar_vencedor']
  conferir('linha de x', v(['x', 'x', 'x', ' ', 'o', ' ', 'o', ' ', ' '], 'x'))
  conferir('coluna de o', v(['o', 'x', ' ', 'o', 'x', ' ', 'o', ' ', 'x'], 'o'))
  conferir('diagonal principal (0, 4, 8)', v(['x', 'o', ' ', 'o', 'x', ' ', ' ', ' ', 'x'], 'x'))
  conferir('diagonal secundaria (2, 4, 6)', v([' ', ' ', 'o', ' ', 'o', ' ', 'o', 'x', 'x'], 'o'))
  conferir('sem vencedor', not v(['x', 'o', 'x', 'x', 'o', 'o', 'o', 'x', 'x'], 'x')
           and not v(['x', 'o', 'x', 'x', 'o', 'o', 'o', 'x', 'x'], 'o'))
  conferir('tres tabuleiros "velha" em linha NAO e vitoria de ninguem',
           not v(['velha', 'velha', 'velha', None, None, None, None, None, None], 'x'))

def testar_cheio_e_empate(jogo):
  titulo('3. Tabuleiro cheio e empates')
  conferir('tabuleiro pequeno cheio e reconhecido',
           jogo['tabuleiro_cheio'](['x', 'o', 'x', 'x', 'o', 'o', 'o', 'x', 'x']))
  conferir('tabuleiro com casa vazia nao esta cheio',
           not jogo['tabuleiro_cheio'](['x', 'o', 'x', 'x', ' ', 'o', 'o', 'x', 'x']))

  tab = jogo['criar_tabuleiro']()
  tab[0]["tabuleiro"] = ['x', 'o', 'x', 'x', 'o', 'o', 'o', 'x', 'x']
  jogo['atualizar_tabuleiro_pequeno'](tab, 0, 'x')
  conferir('pequeno cheio sem vencedor vira "velha"', tab[0]["vencedor"] == 'velha')

  tab = jogo['criar_tabuleiro']()
  vencedores = ['x', 'o', 'x', 'velha', 'o', 'x', 'o', 'x', 'velha']
  for i in range(9):
    tab[i]["vencedor"] = vencedores[i]
  conferir('todos decididos sem 3 em linha -> partida empatada',
           jogo['partida_empatada'](tab)
           and not jogo['verificar_vitoria_grande'](tab, 'x')
           and not jogo['verificar_vitoria_grande'](tab, 'o'))
  tab[8]["vencedor"] = None
  conferir('com tabuleiro em andamento a partida NAO esta empatada', not jogo['partida_empatada'](tab))

def testar_conquista(jogo):
  titulo('4. Conquista de tabuleiro pequeno e do grande')
  tab = jogo['criar_tabuleiro']()
  tab[5]["tabuleiro"][0] = 'o'
  tab[5]["tabuleiro"][4] = 'o'
  tab[5]["tabuleiro"][8] = 'o'
  jogo['atualizar_tabuleiro_pequeno'](tab, 5, 'o')
  conferir('o fecha a diagonal e ganha o tabuleiro 2,3', tab[5]["vencedor"] == 'o')
  conferir('os outros tabuleiros continuam em andamento',
           sum(tab[i]["vencedor"] is None for i in range(9)) == 8)
  conferir('tabuleiro ja ganho nao aceita mais jogadas (dono nao muda)',
           not jogada_valida(jogo, tab, '2 3 1 2', None))

  tab[2]["vencedor"] = 'o'
  tab[8]["vencedor"] = 'o'
  conferir('3 tabuleiros em coluna (1,3 / 2,3 / 3,3) -> o vence a partida',
           jogo['verificar_vitoria_grande'](tab, 'o'))

def testar_entrada(jogo):
  titulo('5. Leitura da entrada (tratamento de strings)')
  tab = jogo['criar_tabuleiro']()
  conferir('"2 3" com destino 1,1 -> tabuleiro 0, casa 5', jogo['converter_jogada']('2 3', 0) == (0, 5))
  conferir('"2 2 1 1" com escolha livre -> tabuleiro 4, casa 0',
           jogo['converter_jogada']('2 2 1 1', None) == (4, 0))
  conferir('aceita "2 3" com destino definido', jogada_valida(jogo, tab, '2 3', 0))
  conferir('aceita "2 2 1 1" com escolha livre', jogada_valida(jogo, tab, '2 2 1 1', None))
  conferir('espacos extras sao ignorados', jogada_valida(jogo, tab, '   1    3  ', 0))

  invalidas = [
    ('', 0, 'entrada vazia'),
    ('2', 0, 'so um numero quando precisa de dois'),
    ('1 2 3', 0, 'tres numeros quando precisa de dois'),
    ('2 3', None, 'dois numeros quando a escolha e livre (precisa de 4)'),
    ('a 3', 0, 'letra no lugar de numero'),
    ('2,3', 0, 'separado por virgula'),
    ('0 2', 0, 'numero 0 (fora de 1 a 3)'),
    ('4 1', 0, 'numero 4 (fora de 1 a 3)'),
    ('-1 2', 0, 'numero negativo'),
    ('1.5 2', 0, 'numero com casa decimal'),
    ('² 1', 0, 'caractere "²" (isdigit aceitaria e o int() quebraria)'),
  ]
  for texto, destino, descricao in invalidas:
    try:
      conferir(f'rejeita {descricao}', not jogada_valida(jogo, tab, texto, destino))
    except Exception as excecao:
      conferir(f'rejeita {descricao} (QUEBROU: {excecao})', False)

def testar_validacao(jogo):
  titulo('6. Validacao da jogada no tabuleiro')
  tab = jogo['criar_tabuleiro']()
  tab[0]["tabuleiro"][4] = 'x'
  tab[8]["vencedor"] = 'o'
  conferir('casa vazia em tabuleiro em andamento e aceita', jogada_valida(jogo, tab, '1 1', 0))
  conferir('casa ocupada e recusada', not jogada_valida(jogo, tab, '2 2', 0))
  conferir('tabuleiro ja decidido e recusado', not jogada_valida(jogo, tab, '3 3 1 1', None))

def testar_destino(jogo):
  titulo('7. Regra do tabuleiro de destino')
  tab = jogo['criar_tabuleiro']()
  conferir('jogar na casa 1,3 (indice 2) manda o adversario para o tabuleiro 1,3',
           jogo['proximo_destino'](tab, 2) == 2)
  tab[2]["vencedor"] = 'x'
  conferir('se o tabuleiro 1,3 ja foi ganho, a escolha fica livre', jogo['proximo_destino'](tab, 2) is None)
  tab[4]["vencedor"] = 'velha'
  conferir('se o tabuleiro de destino deu velha, a escolha fica livre', jogo['proximo_destino'](tab, 4) is None)

  partida = jogo['criar_partida']()
  partida["jogadores"] = {'x': 'Daniel', 'o': 'Larissa'}
  partida["destino"] = 0
  entradas_simuladas(jogo, ['2 3'])
  jogada, saida = rodar_em_silencio(jogo['realizar_jogada'], partida, 'x')
  conferir('destino 1,1 + entrada "2 3" -> marca o tabuleiro 1,1, casa 2,3',
           jogada == (0, 5) and partida["tabuleiro"][0]["tabuleiro"][5] == 'x')
  conferir('avisa em qual tabuleiro jogar', 'Jogue no tabuleiro 1,1' in saida)

  partida = jogo['criar_partida']()
  partida["jogadores"] = {'x': 'Daniel', 'o': 'Larissa'}
  partida["tabuleiro"][4]["vencedor"] = 'o'
  entradas_simuladas(jogo, ['2 2 1 1', '3 3 1 1'])
  jogada, saida = rodar_em_silencio(jogo['realizar_jogada'], partida, 'x')
  conferir('escolha livre recusa tabuleiro decidido e aceita o proximo valido',
           jogada == (8, 0) and 'já foi decidido' in saida and 'Escolha livre' in saida)

def testar_entradas_ruins_seguidas(jogo):
  titulo('8. O programa nao quebra com entradas invalidas')
  partida = jogo['criar_partida']()
  partida["jogadores"] = {'x': 'Daniel', 'o': 'Larissa'}
  partida["destino"] = 0
  partida["tabuleiro"][0]["tabuleiro"][0] = 'o'
  lixo = ['', 'abc', '1', '1 2 3', '0 1', '4 4', 'x y', '1 1', '2 2']
  fila = entradas_simuladas(jogo, lixo)
  try:
    jogada, saida = rodar_em_silencio(jogo['realizar_jogada'], partida, 'x')
    conferir(f'{len(lixo) - 1} entradas ruins seguidas: explica o erro e pede de novo',
             jogada == (0, 4) and len(fila) == 0
             and saida.count('Jogada inválida') == 7 and 'Posição já ocupada' in saida)
  except Exception as excecao:
    conferir(f'entradas ruins seguidas (QUEBROU: {excecao})', False)

def testar_partida_completa(jogo):
  titulo('9. Partida completa simulada')
  entradas_simuladas(jogo, ['Daniel', 'Larissa'] + PARTIDA_VITORIA_X)
  partida, saida = rodar_em_silencio(jogo['jogar'])
  conferir('37 jogadas com regra do destino e escolha livre: x vence',
           partida["vencedor"] == 'x' and partida["estado"] == "FINALIZADO")
  conferir('anuncia o vencedor pelo nome', 'Daniel (X) venceu a partida!' in saida)
  conferir('informa de quem e a vez pelo nome', 'Vez de Larissa (O).' in saida)
  conferir('avisa quando a escolha e livre', 'Escolha livre' in saida)

  entradas_simuladas(jogo, ['', 'Daniel', '   ', 'Larissa'] + PARTIDA_VITORIA_X)
  partida, saida = rodar_em_silencio(jogo['jogar'])
  conferir('nome vazio e recusado e pedido de novo',
           partida["vencedor"] == 'x' and saida.count('não pode ser vazio') == 2)

  entradas_simuladas(jogo, ['Daniel', 'Daniel', 'Larissa'] + PARTIDA_VITORIA_X)
  partida, saida = rodar_em_silencio(jogo['jogar'])
  conferir('nomes iguais sao recusados (misturariam o placar)',
           partida["jogadores"]['o'] == 'Larissa' and 'nomes diferentes' in saida)

def testar_menu(jogo):
  titulo('10. Menu principal')
  entradas_simuladas(jogo, ['9', 'abc', '2', '3'])
  try:
    _, saida = rodar_em_silencio(jogo['main'])
    conferir('opcao invalida avisa e o menu continua', saida.count('Opção inválida') == 2)
    conferir('opcao 2 mostra as regras e volta ao menu',
             'Regras do jogo' in saida and saida.count('1: Iniciar jogo') == 4)
    conferir('opcao 3 encerra o programa', 'Jogo finalizado' in saida)
  except Exception as excecao:
    conferir(f'menu (QUEBROU: {excecao})', False)

  entradas_simuladas(jogo, ['1', 'Daniel', 'Larissa'] + PARTIDA_VITORIA_X + ['3'])
  _, saida = rodar_em_silencio(jogo['main'])
  conferir('depois da partida o programa volta ao menu',
           'venceu a partida' in saida and 'Jogo finalizado' in saida)

def testar_placar(jogo):
  titulo('11. BONUS: Placar da sessao')
  placar = jogo['criar_placar']()
  _, saida = rodar_em_silencio(jogo['mostrar_placar'], placar)
  conferir('placar vazio avisa que nenhuma partida foi jogada', 'Nenhuma partida' in saida)

  def partida_falsa(nomeX, nomeO, vencedor):
    partida = jogo['criar_partida']()
    partida["jogadores"] = {'x': nomeX, 'o': nomeO}
    partida["vencedor"] = vencedor
    return partida

  jogo['registrar_placar'](placar, partida_falsa('Daniel', 'Larissa', 'x'))
  conferir('vitoria do x soma 1 para quem era x e 0 para o o',
           placar["vitorias"] == {'Daniel': 1, 'Larissa': 0})
  jogo['registrar_placar'](placar, partida_falsa('Larissa', 'Daniel', 'o'))
  conferir('vitoria vai para a pessoa, nao para o simbolo',
           placar["vitorias"] == {'Daniel': 2, 'Larissa': 0})
  jogo['registrar_placar'](placar, partida_falsa('Daniel', 'Miguel', 'velha'))
  conferir('empate soma nos empates e jogador novo entra com 0 vitorias',
           placar["empates"] == 1 and placar["vitorias"]['Miguel'] == 0)

  _, saida = rodar_em_silencio(jogo['mostrar_placar'], placar)
  conferir('placar mostra vitorias de cada jogador e empates',
           'Daniel: 2 vitória(s)' in saida and 'Larissa: 0 vitória(s)' in saida and 'Empates: 1' in saida)

  partida = ['1', 'Daniel', 'Larissa'] + PARTIDA_VITORIA_X
  entradas_simuladas(jogo, partida + partida + ['4', '3'])
  _, saida = rodar_em_silencio(jogo['main'])
  conferir('opcao 4 do menu soma as partidas da sessao (Daniel 2 x 0 Larissa)',
           'Daniel: 2 vitória(s)' in saida and 'Larissa: 0 vitória(s)' in saida)

def testar_historico(jogo):
  titulo('12. BONUS: Historico da partida')
  partida = jogo['criar_partida']()
  partida["jogadores"] = {'x': 'Miguel', 'o': 'Ana'}
  partida["historico"] = ['1. ...', '2. ...']
  jogo['registrar_jogada'](partida, 'x', 4, 2)
  conferir('formato igual ao do enunciado: "3. Miguel (X): tabuleiro 2,2 / casa 1,3"',
           partida["historico"][2] == '3. Miguel (X): tabuleiro 2,2 / casa 1,3')

  entradas_simuladas(jogo, ['Daniel', 'Larissa'] + PARTIDA_VITORIA_X)
  partida, saida = rodar_em_silencio(jogo['jogar'])
  historico = partida["historico"]
  conferir('uma linha por jogada (37 jogadas)', len(historico) == 37)
  conferir('primeira jogada: "1. Daniel (X): tabuleiro 1,1 / casa 1,1"',
           historico[0] == '1. Daniel (X): tabuleiro 1,1 / casa 1,1')
  conferir('jogada de escolha livre registra o tabuleiro escolhido (34: tabuleiro 1,3)',
           historico[33] == '34. Larissa (O): tabuleiro 1,3 / casa 2,1')
  conferir('historico e impresso ao final da partida',
           'Histórico da partida' in saida and '37. Daniel (X)' in saida)

  partida = ['1', 'Daniel', 'Larissa'] + PARTIDA_VITORIA_X
  entradas_simuladas(jogo, ['5'] + partida + partida + ['5', '3'])
  _, saida = rodar_em_silencio(jogo['main'])
  antes = saida.split('1: Iniciar jogo')[1]  #trecho entre o 1o e o 2o menu
  conferir('opcao 5 antes de jogar avisa que nao ha partida', 'Nenhuma partida' in antes)
  ultimo = saida.rsplit('Histórico da partida', 1)[1]
  conferir('opcao 5 mostra so a ultima partida (numeracao recomeca, sem jogada 38)',
           '37. Daniel (X)' in ultimo and '38.' not in ultimo)

# ---------------------------------------------------------------------------
# Modos de execucao
# ---------------------------------------------------------------------------

def rodar_testes():
  jogo = carregar_jogo()
  testar_criacao(jogo)
  testar_vencedor(jogo)
  testar_cheio_e_empate(jogo)
  testar_conquista(jogo)
  testar_entrada(jogo)
  testar_validacao(jogo)
  testar_destino(jogo)
  testar_entradas_ruins_seguidas(jogo)
  testar_partida_completa(jogo)
  testar_menu(jogo)
  testar_placar(jogo)
  testar_historico(jogo)

  titulo(f'RESULTADO: {testes_ok} de {total_testes} testes passaram')
  if testes_ok == total_testes:
    print('  Tudo certo!')
  else:
    print(f'  {total_testes - testes_ok} teste(s) falharam. Veja os [FALHOU] acima.')
  print()
  return testes_ok == total_testes

def mostrar_partida(pausar):
  #roda uma partida de verdade com entradas prontas, mostrando tudo na tela
  #comeca com algumas entradas erradas para mostrar a validacao
  jogo = carregar_jogo()
  if not pausar:
    #sem pausa, limpar a tela apagaria tudo na hora; entao so mostramos em sequencia
    jogo['limpar_tela'] = lambda: print('\n' + '-' * 60)
  titulo('PARTIDA SIMULADA: Daniel (X) x Larissa (O)')
  errosDeExemplo = ['abc', '1 2', '0 1 1 1']
  entradas_simuladas(jogo, ['Daniel', 'Larissa'] + errosDeExemplo + PARTIDA_VITORIA_X,
                     mostrar=True, pausar=pausar)
  jogo['jogar']()

def main():
  if '--partida' in sys.argv:
    mostrar_partida('--pausar' in sys.argv)
  else:
    tudoOk = rodar_testes()
    sys.exit(0 if tudoOk else 1)


main()
