# Introduction
This is a demo of projectile motion. The program finds the best angle and
initial velocity using calculus. All useful information like horizontal range,
velocity etc. are shown in the top left corner. The calculations might not be
accurate. The code is quite messy because I rushed the project.

Usage:
* Left mouse click makes the bucket go to the left, thus reducing the horizontal
range. Right click does the opposite.
* Press space button to start the simulation.
* Press 'R' anytime to reset the simulation.

## Demo
[![Projectile Motion](http://img.youtube.com/vi/Djp7BpP9eXY/0.jpg)](http://www.youtube.com/watch?v=Djp7BpP9eXY)

## Getting Started

### Dependencies

* Python
* Poetry (optional)

### Executing program

* The command below uses git. You can also download zip version.
```bash
git clone https://github.com/rakin406/projectile-motion.git && cd projectile-motion
```

* If you have poetry installed, do the following:
```bash
poetry install
poetry run python projectile_motion/main.py
```

* Otherwise, do this:
```bash
pip install pyglet sympy
python3 projectile_motion/main.py
```

## Authors

Rakin Rahman

## License

This project is licensed under the MIT License - see the LICENSE file for details
