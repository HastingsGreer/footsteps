import footsteps
footsteps.initialize(output_root="../results/")

with open(footsteps.output_dir + "card.txt", "w") as f:
  f.write("happy birthday!")
