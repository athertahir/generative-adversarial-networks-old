# %%
'''
## Traditional Discriminator Model
Consider a discriminator model for the standard GAN model. It must take an image as input
and predict whether it is real or fake. More specifically, it predicts the likelihood of the input
image being real. The output layer uses a sigmoid activation function to predict a probability
value in [0,1] and the model is typically optimized using a binary cross-entropy loss function.
For example, we can define a simple discriminator model that takes grayscale images as input
with the size of 28 × 28 pixels and predicts a probability of the image being real. We can use
best practices and downsample the image using convolutional layers with a 2 × 2 stride and
a leaky ReLU activation function. The define discriminator() function below implements
this and defines our standard discriminator model.
'''

# %%
# example of defining the discriminator model
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import LeakyReLU
from keras.layers import Dropout
from keras.layers import Flatten
from keras.optimizers import Adam
from keras.utils.vis_utils import plot_model

# define the standalone discriminator model
def define_discriminator(in_shape=(28,28,1)):
	# image input
	in_image = Input(shape=in_shape)
	# downsample
	fe = Conv2D(128, (3,3), strides=(2,2), padding='same')(in_image)
	fe = LeakyReLU(alpha=0.2)(fe)
	# downsample
	fe = Conv2D(128, (3,3), strides=(2,2), padding='same')(fe)
	fe = LeakyReLU(alpha=0.2)(fe)
	# downsample
	fe = Conv2D(128, (3,3), strides=(2,2), padding='same')(fe)
	fe = LeakyReLU(alpha=0.2)(fe)
	# flatten feature maps
	fe = Flatten()(fe)
	# dropout
	fe = Dropout(0.4)(fe)
	# output layer
	d_out_layer = Dense(1, activation='sigmoid')(fe)
	# define and compile discriminator model
	d_model = Model(in_image, d_out_layer)
	d_model.compile(loss='binary_crossentropy', optimizer=Adam(lr=0.0002, beta_1=0.5))
	return d_model

# create model
model = define_discriminator()
# plot the model
plot_model(model, to_file='discriminator_plot.png', show_shapes=True, show_layer_names=True)