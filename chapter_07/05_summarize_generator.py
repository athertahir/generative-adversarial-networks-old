# %%
'''
## How to Define and Use the Generator Model
The generator model is responsible for creating new, fake but plausible images of handwritten
digits. It does this by taking a point from the latent space as input and outputting a square7.4. How to Define and Use the Generator Model 106
grayscale image. The latent space is an arbitrarily defined vector space of Gaussian-distributed
values, e.g. 100 dimensions. It has no meaning, but by drawing points from this space randomly
and providing them to the generator model during training, the generator model will assign
meaning to the latent points. At the end of training, the latent vector space represents a
compressed representation of the output space, MNIST images, that only the generator knows
how to turn into plausible MNIST images.

❼ Inputs: Point in latent space, e.g. a 100 element vector of Gaussian random numbers.
❼ Outputs: Two-dimensional square grayscale image of 28 × 28 pixels with pixel values in
[0,1].

We don’t have to use a 100 element vector as input; it is a round number and widely used,
but I would expect that 10, 50, or 500 would work just as well. Developing a generator model
requires that we transform a vector from the latent space with, 100 dimensions to a 2D array
with 28×28 or 784 values. There are a number of ways to achieve this but there is one approach
that has proven effective at deep convolutional generative adversarial networks. It involves two
main elements. The first is a Dense layer as the first hidden layer that has enough nodes to
represent a low-resolution version of the output image. Specifically, an image half the size (one
quarter the area) of the output image would be 14 × 14 or 196 nodes, and an image one quarter
the size (one eighth the area) would be 7 × 7 or 49 nodes.

We don’t just want one low-resolution version of the image; we want many parallel versions
or interpretations of the input. This is a pattern in convolutional neural networks where we
have many parallel filters resulting in multiple parallel activation maps, called feature maps,
with different interpretations of the input. We want the same thing in reverse: many parallel
versions of our output with different learned features that can be collapsed in the output layer
into a final image. The model needs space to invent, create, or generate. Therefore, the first
hidden layer, the Dense layer needs enough nodes for multiple low-resolution versions of our
output image, such as 128.
'''

# %%
# example of defining the generator model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Reshape
from keras.layers import Conv2D
from keras.layers import Conv2DTranspose
from keras.layers import LeakyReLU
from keras.utils.vis_utils import plot_model

# define the standalone generator model
def define_generator(latent_dim):
	model = Sequential()
	# foundation for 7x7 image
	n_nodes = 128 * 7 * 7
	model.add(Dense(n_nodes, input_dim=latent_dim))
	model.add(LeakyReLU(alpha=0.2))
	model.add(Reshape((7, 7, 128)))
	# upsample to 14x14
	model.add(Conv2DTranspose(128, (4,4), strides=(2,2), padding='same'))
	model.add(LeakyReLU(alpha=0.2))
	# upsample to 28x28
	model.add(Conv2DTranspose(128, (4,4), strides=(2,2), padding='same'))
	model.add(LeakyReLU(alpha=0.2))
	model.add(Conv2D(1, (7,7), activation='sigmoid', padding='same'))
	return model

# define the size of the latent space
latent_dim = 100
# define the generator model
model = define_generator(latent_dim)
# summarize the model
model.summary()
# plot the model
plot_model(model, to_file='generator_plot.png', show_shapes=True, show_layer_names=True)

