import splitfolders

input_folder = './dataset'
output = './split_dataset'

splitfolders.ratio(input_folder, output=output, seed=1337, ratio=(.8, .2))