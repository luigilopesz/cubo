import pygame
import numpy as np
import pywavefront

# Função para aplicar a matriz de projeção
def projecao_perspectiva(vertices, d):
  # Matriz de projeção P
  P = np.array([
    [d, 0, 0, 0],
    [0, d, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 1/d, 0]
  ])
  
  # Multiplicar os vértices pela matriz de projeção
  projecao = np.dot(vertices, P.T)  # Transposta para multiplicar corretamente
  
  # Dividir os componentes x e y por w para projeção em perspectiva de forma vetorizada
  projecao[:, 0] /= projecao[:, 3]  # x' = x / w
  projecao[:, 1] /= projecao[:, 3]  # y' = y / w
  return projecao

# Funções de rotação 3D (matrizes de rotação adaptadas para 4D)
def rotacao_x(vertices, angulo):
  """ Rotaciona ao redor do eixo X """
  cos_ang = np.cos(angulo)
  sin_ang = np.sin(angulo)
  matriz_rotacao = np.array([
    [1, 0, 0, 0],
    [0, cos_ang, -sin_ang, 0],
    [0, sin_ang, cos_ang, 0],
    [0, 0, 0, 1]
  ])
  return np.dot(vertices, matriz_rotacao)

def rotacao_y(vertices, angulo):
  """ Rotaciona ao redor do eixo Y """
  cos_ang = np.cos(angulo)
  sin_ang = np.sin(angulo)
  matriz_rotacao = np.array([
    [cos_ang, 0, sin_ang, 0],
    [0, 1, 0, 0],
    [-sin_ang, 0, cos_ang, 0],
    [0, 0, 0, 1]
  ])
  return np.dot(vertices, matriz_rotacao)

# Inicializar o Pygame
pygame.init()

# Configurações da janela
screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Projeção em Perspectiva do Cubo")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Função para converter coordenadas para a tela
def to_screen_coordinates(x, y):
  return int(screen_width // 2 + x * 100), int(screen_height // 2 - y * 100)

# Definindo os vértices do cubo com coordenadas homogêneas (x, y, z, 1)
vertices_cubo = np.array([
  [-1, -1, -1, 1],
  [-1, -1, 1, 1],
  [-1, 1, -1, 1],
  [-1, 1, 1, 1],
  [1, -1, -1, 1],
  [1, -1, 1, 1],
  [1, 1, -1, 1],
  [1, 1, 1, 1]
])

vaca = pywavefront.Wavefront(r'C:\Users\luigi\3insper242\algelinha\cubo\cubo\vaca.obj', create_materials=True)
vaca_vertices = np.array(vaca.vertices)
uns = np.ones((vaca_vertices.shape[0], 1))  # Coluna de 1s
vaca_vertices = np.hstack((vaca_vertices, uns))


vertice_atual = vertices_cubo

# Transladar o cubo no eixo z para "afastá-lo"
translacao_z = 2  # Aumente este valor para afastar mais o cubo
angulo_x, angulo_y = 0, 0

# Parâmetro da projeção em perspectiva
d = 1.5  # Quanto maior o valor de d, mais pronunciada a perspectiva



# Loop principal do Pygame
running = True
while running:
  screen.fill(WHITE)  # Limpar a tela

  # Capturar os eventos de teclado
  keys = pygame.key.get_pressed()
  if keys[pygame.K_a]:
      angulo_y -= 0.005  # Rotacionar ao redor do eixo Y (esquerda)
  if keys[pygame.K_d]:
      angulo_y += 0.005  # Rotacionar ao redor do eixo Y (direita)
  if keys[pygame.K_w]:
      angulo_x -= 0.005  # Rotacionar ao redor do eixo X (cima)
  if keys[pygame.K_s]:
      angulo_x += 0.005  # Rotacionar ao redor do eixo X (baixo)

  # Aproximar/afastar com Q e E
  if keys[pygame.K_q]:
    translacao_z -= 0.003  # Aproximar (diminuir Z)
  if keys[pygame.K_e]:
    translacao_z += 0.003  # Afastar (aumentar Z)

  if keys[pygame.K_v]:
    vertice_atual = vaca_vertices
  if keys[pygame.K_c]:
    vertice_atual = vertices_cubo
  # Aplicar rotações
  vertices_rotacionados = rotacao_x(vertice_atual, angulo_x)
  vertices_rotacionados = rotacao_y(vertices_rotacionados, angulo_y)

  # Aplicar a translação no eixo Z para afastar o cubo
  vertices_transladados = vertices_rotacionados.copy()
  vertices_transladados[:, 2] += translacao_z

  # Aplicar a projeção em perspectiva usando a matriz
  vertices_projetados = projecao_perspectiva(vertices_transladados, d)

  # Desenhar os pontos projetados
  pontos_tela = []
  for vertice in vertices_projetados:
    x, y = to_screen_coordinates(vertice[0], vertice[1])
    pontos_tela.append((x, y))
    pygame.draw.circle(screen, RED, (x, y), 5)  # Desenha um ponto

  # Definir as arestas do cubo
  arestas = [
    [0, 1], [0, 2], [0, 4], # Conexões do vértice 0
    [1, 3], [1, 5], # Conexões do vértice 1
    [2, 3], [2, 6], # Conexões do vértice 2
    [3, 7], # Conexões do vértice 3
    [4, 5], [4, 6], # Conexões do vértice 4
    [5, 7], # Conexões do vértice 5
    [6, 7]  # Conexões do vértice 6
  ]

  # Desenhar as arestas conectando os pontos
  for aresta in arestas:
    ponto1 = pontos_tela[aresta[0]]
    ponto2 = pontos_tela[aresta[1]]
    pygame.draw.line(screen, BLACK, ponto1, ponto2, 2)  # Desenha uma aresta

  # Atualizar a tela
  pygame.display.flip()

  # Checar eventos para fechar a janela
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

# Encerrar o Pygame
pygame.quit()
