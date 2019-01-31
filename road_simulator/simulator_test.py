from roadsimulator.colors import Yellow, White, DarkShadow
from roadsimulator.layers.layers import Background, Crop, Perspective, DrawLines, Symmetric
from roadsimulator.layers.noise import Shadows, Filter, NoiseLines, Enhance
from roadsimulator.simulator import Simulator

simulator = Simulator()

white = White()

white_range = White()
yellow_range = Yellow()
shadow_colors = DarkShadow()
color_range = white_range + yellow_range

simulator.add(Background(n_backgrounds=3, path="./road_simulator/ground_pics", input_size=(250, 200)))
simulator.add(DrawLines(input_size=(250,200), color_range=white))
simulator.add(Perspective(output_dim=(200, 66)))
simulator.add(Symmetric(proba=0.5))
simulator.add(Shadows(color=shadow_colors))
simulator.add(NoiseLines(color_range))
simulator.add(Filter())
simulator.add(Enhance())
simulator.add(Crop(output_dim=(200, 66)))

simulator.generate(n_examples=2000, path="dataset")