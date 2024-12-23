# Bomberman 

Bomberman clone written in Python using Pygame. The game allows playing against two types of AI (Dijkstra Algorithm and Depth-first search).

## Controls 
### For Player 1  
- Moving: Arrows 
- Planting Bomb: LCTRL

### For Player 2 :
- Moving: WASD 
- Planting Bomb: RCTRL

## Requirements
To run this game, you need to install Pygame and Pygame-menu packages.

You can install them using pip:
```bash
pip install pygame pygame-menu


Run using menu file:

`` 
python3 launch.py
`` 


Python might not be able to locate main game files due to module import issues. 
In order to test this game, you need to use this command: 

``
 python -m pytest tests/$filename.py

``
