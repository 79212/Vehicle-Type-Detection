import tensorflow
from tensorflow.keras.applications.mobilenet import MobileNet
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from helpers import separate_test_train_dirs, generate_augment
from sklearn.externals import joblib

input_generator_shape = (224, 224)
input_shape = (224, 224, 3) # including color channels
batch_size = 32

# All paths needs a "/" at the end for this to work
all_path = "./all_images/" # CHANGE THIS. directory path to where all images are
train_path = "./train_only/" # directory path to store train images
test_path = "./test_only/" # directory path to store test images

# Separate images into train and test
# separate_test_train_dirs(all_path, train_path, test_path)

num_classes = 17 # number of classes in the data
epochs = 12

base_model = MobileNet( input_shape = input_shape, alpha=1.0, include_top = False)
w = base_model.output
w = Flatten()(w)
W = Dense(128, activation = "relu")(w)
output = Dense(17, activation = "sigmoid")(w)
model = Model(inputs = [base_model.input], outputs = [output])

model.compile(loss=tensorflow.keras.losses.categorical_crossentropy,
              optimizer=tensorflow.keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.summary()

# Get generators for training and validation
train_generator, validation_generator = generate_augment(train_path, 
										test_path,
										input_generator_shape,
										batch_size)

model.fit_generator(train_generator,
				    steps_per_epoch = train_generator.samples // batch_size,
				    validation_data = validation_generator, 
				    validation_steps = validation_generator.samples // batch_size,
					epochs=epochs)

model_name = 'inception_model.h5'
model.save(model_name)