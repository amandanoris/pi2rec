# Copyright (c) 2023-2025
# This file is part of pi2rec.
#
# pi2rec is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pi2rec is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pi2rec. If not, see <http://www.gnu.org/licenses/>.
#
from common import pic_height
from common import pic_width
from PIL import Image
import argparse
import keras
import matplotlib.pyplot as plt
import numpy

def loss_ssim (y_true, y_pred):
  return 1 - tf.image.ssim (y_true, y_pred, max_val = 1.0)

def parse_args ():

  parser = argparse.ArgumentParser (description = 'pi2rec')

  parser.add_argument ('--InputImage',
      default = 'input.jpg',
      help = 'input image to process',
      metavar = 'input',
      required = False,
      type = str)
  parser.add_argument ('--OutputImage',
      default = 'output.jpg',
      help = 'where to output the result image',
      metavar = 'output',
      required = False,
      type = str)

  args = parser.parse_args ()

  return (args.InputImage, args.OutputImage)

custom_objects = { 'loss_ssim' : loss_ssim }
input_file, output_file = parse_args ()
model = keras.models.load_model ('pi2rec.keras', custom_objects = custom_objects)
image = keras.preprocessing.image.load_img (input_file)
image_width = image.width
image_height = image.height
image = image.resize ((pic_width, pic_height))
image = keras.preprocessing.image.img_to_array (image)
image = image / 255.0
batch = numpy.expand_dims (image, axis = 0)
result = model.predict (batch)
result = result [0] * 255.0
result = result.astype (numpy.uint8)
result = Image.fromarray (result)
result = result.resize ((image_width, image_height))
result.save (output_file)