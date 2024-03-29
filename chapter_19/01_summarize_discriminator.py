# %%
'''
## AC-GAN Discriminator Model
Let’s start with the discriminator model. The discriminator model must take as input an
image and predict both the probability of the realness of the image and the probability of the
image belonging to each of the given classes. The input images will have the shape 28 × 28 × 1
and there are 10 classes for the items of clothing in the Fashion-MNIST dataset. The model
can be defined as per the DCGAN architecture. That is, using Gaussian weight initialization,
BatchNormalization, LeakyReLU, Dropout, and a 2 × 2 stride for downsampling instead of
pooling layers. For example, below is the bulk of the discriminator model defined using the
Keras functional API.
'''

# %%
'''
The model must be trained with two loss functions, binary cross-entropy for the first output
layer, and categorical cross-entropy loss for the second output layer. Rather than comparing a
one hot encoding of the class labels to the second output layer, as we might do normally, we can
compare the integer class labels directly. We can achieve this automatically using the sparse
categorical cross-entropy loss function. This will have the identical effect of the categorical
cross-entropy but avoids the step of having to manually one hot encode the target labels. When
compiling the model, we can inform Keras to use the two different loss functions for the two
output layers by specifying a list of function names as strings
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
from keras.layers import BatchNormalization
from keras.initializers import RandomNormal
from keras.optimizers import Adam
from keras.utils.vis_utils import plot_model

# define the standalone discriminator model
def define_discriminator(in_shape=(28,28,1), n_classes=10):
	# weight initialization
	init = RandomNormal(stddev=0.02)
	# image input
	in_image = Input(shape=in_shape)
	# downsample to 14x14
	fe = Conv2D(32, (3,3), strides=(2,2), padding='same', kernel_initializer=init)(in_image)
	fe = LeakyReLU(alpha=0.2)(fe)
	fe = Dropout(0.5)(fe)
	# normal
	fe = Conv2D(64, (3,3), padding='same', kernel_initializer=init)(fe)
	fe = BatchNormalization()(fe)
	fe = LeakyReLU(alpha=0.2)(fe)
	fe = Dropout(0.5)(fe)
	# downsample to 7x7
	fe = Conv2D(128, (3,3), strides=(2,2), padding='same', kernel_initializer=init)(fe)
	fe = BatchNormalization()(fe)
	fe = LeakyReLU(alpha=0.2)(fe)
	fe = Dropout(0.5)(fe)
	# normal
	fe = Conv2D(256, (3,3), padding='same', kernel_initializer=init)(fe)
	fe = BatchNormalization()(fe)
	fe = LeakyReLU(alpha=0.2)(fe)
	fe = Dropout(0.5)(fe)
	# flatten feature maps
	fe = Flatten()(fe)
	# real/fake output
	out1 = Dense(1, activation='sigmoid')(fe)
	# class label output
	out2 = Dense(n_classes, activation='softmax')(fe)
	# define model
	model = Model(in_image, [out1, out2])
	# compile model
	opt = Adam(lr=0.0002, beta_1=0.5)
	model.compile(loss=['binary_crossentropy', 'sparse_categorical_crossentropy'], optimizer=opt)
	return model

# define the discriminator model
model = define_discriminator()
# summarize the model
model.summary()
# plot the model
plot_model(model, to_file='discriminator_plot.png', show_shapes=True, show_layer_names=True)