from graphviz import Digraph

# Crear el objeto de diagrama
dot = Digraph(comment='TreeMan UML', format='png')
dot.attr(rankdir='TB')

# Clase Game
dot.node('Game', '''Game
- tree: Tree
- achas: list<Acha>
- points: list<Point>
- score: int
+ run()
+ check_collisions()
+ update_screen()
+ handle_input()
+ end_game()''')

# Clase Tree
dot.node('Tree', '''Tree
- x: int
- y: int
- speed: int
- lives: int
- image
+ move(dx, dy)
+ draw()
+ collide(obj)''')

# Clase Acha
dot.node('Acha', '''Acha
- x: int
- y: int
- speed: int
- image
+ move(target_x, target_y)
+ draw()''')

# Clase Point
dot.node('Point', '''Point
- x: int
- y: int
- type: str
- image
+ draw()''')

# Clase ScoreManager
dot.node('ScoreManager', '''ScoreManager
+ save_score(score, action)''')

# Clase UIManager
dot.node('UIManager', '''UIManager
+ draw_ui(tree, score)
+ draw_start_menu()
+ draw_game_over(score)''')

# Relaciones (uso)
dot.edge('Game', 'Tree', label='uses')
dot.edge('Game', 'Acha', label='uses')
dot.edge('Game', 'Point', label='uses')
dot.edge('Game', 'ScoreManager', label='uses')
dot.edge('Game', 'UIManager', label='uses')

# Exportar el archivo
dot.render('uml_treeman', view=True)  # Abre la imagen automáticamente
