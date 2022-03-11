# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WDBltEfTzOApPvCBe22bF0phwDL_I_GH

<h1>El modelo secuencial</h1>
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

"""<h3>Cuándo usar un modelo secuencial</h3>

A Sequential modelo es apropiado para una <b>pila llanura de capas</b>, donde cada capa tiene exactamente un tensor de entrada y un tensor de salida.

Esquemáticamente, la siguiente Sequential modelo:
"""

# Define Sequential model with 3 layers
model = keras.Sequential(
    [
        layers.Dense(2, activation="relu", name="layer1"),
        layers.Dense(3, activation="relu", name="layer2"),
        layers.Dense(4, name="layer3"),
    ]
)
# Call model on a test input
x = tf.ones((3, 3))
y = model(x)

"""es equivalente a :"""

# Create 3 layers
layer1 = layers.Dense(2, activation="relu", name="layer1")
layer2 = layers.Dense(3, activation="relu", name="layer2")
layer3 = layers.Dense(4, name="layer3")

# Call layers on a test input
x = tf.ones((3, 3))
y = layer3(layer2(layer1(x)))

"""El modelo A secuencial <b>no</b> es apropiado cuando:

<ul>
<li>Su modelo tiene múltiples entradas o múltiples salidas</li>
<li>Cualquiera de sus capas tiene múltiples entradas o múltiples salidas</li>
<li>Necesitas compartir capas</li>
<li>Quiere una topología no lineal (por ejemplo, una conexión residual, un modelo de varias ramas)</li>

<h2>Creación de un modelo secuencial</h2>
Puede crear un modelo secuencial pasando una lista de capas al constructor secuencial:
"""

model = keras.Sequential(
    [
        layers.Dense(2, activation="relu"),
        layers.Dense(3, activation="relu"),
        layers.Dense(4),
    ]
)

model.layers

"""También puede crear un modelo secuencial de forma incremental a través de la add() método:

"""

model = keras.Sequential()
model.add(layers.Dense(2, activation="relu"))
model.add(layers.Dense(3, activation="relu"))
model.add(layers.Dense(4))

"""Tenga en cuenta que también hay una correspondiente pop() método para eliminar las capas: un modelo secuencial se comporta muy parecido a una lista de capas."""

model.pop()
print(len(model.layers))  # 2

"""También tenga en cuenta que el constructor secuencial acepta un name argumento, al igual que cualquier capa o modelo en el Keras. Esto es útil para anotar gráficos de TensorBoard con nombres semánticamente significativos."""

model = keras.Sequential(name="my_sequential")
model.add(layers.Dense(2, activation="relu", name="layer1"))
model.add(layers.Dense(3, activation="relu", name="layer2"))
model.add(layers.Dense(4, name="layer3"))

"""### Especificar la forma de entrada por adelantado


Generalmente, todas las capas en Keras necesitan conocer la forma de sus entradas para poder crear sus pesos. Entonces, cuando crea una capa como esta, inicialmente, no tiene pesos:


"""

layer = layers.Dense(3)
layer.weights  # Empty

"""Crea sus pesos la primera vez que se llama a una entrada, ya que la forma de los pesos depende de la forma de las entradas:"""

# Call layer on a test input
x = tf.ones((1, 4))
y = layer(x)
layer.weights  # Now it has weights, of shape (4, 3) and (3,)

"""Naturalmente, esto también se aplica a los modelos secuenciales. Cuando se instancia un modelo secuencial sin una forma de entrada, no se "construye": no tiene pesos (y llamando model.weights resultados en un error que indica simplemente esto). Los pesos se crean cuando el modelo ve por primera vez algunos datos de entrada:"""

model = keras.Sequential(
    [
        layers.Dense(2, activation="relu"),
        layers.Dense(3, activation="relu"),
        layers.Dense(4),
    ]
)  # No weights at this stage!

# At this point, you can't do this:
# model.weights

# You also can't do this:
# model.summary()

# Call the model on a test input
x = tf.ones((1, 4))
y = model(x)
print("Number of weights after calling the model:", len(model.weights))  # 6

"""Una vez que un modelo se "construye", puede llamar a su summary() método para mostrar su contenido:"""

model.summary()

"""Sin embargo, puede ser muy útil al construir un modelo secuencial de forma incremental para poder mostrar el resumen del modelo hasta el momento, incluida la forma de salida actual. En este caso, usted debe comenzar su modelo mediante el paso de una Input objeto a su modelo, para que conozca su forma de entrada desde el principio:"""

model = keras.Sequential()
model.add(keras.Input(shape=(4,)))
model.add(layers.Dense(2, activation="relu"))

model.summary()

"""Tenga en cuenta que la Input de objetos no se muestra como parte de model.layers , ya que no es una capa:"""

model.layers

"""Una alternativa más sencilla es simplemente pasar un input_shape argumento para su primera capa:"""

model = keras.Sequential()
model.add(layers.Dense(2, activation="relu", input_shape=(4,)))

model.summary()

"""Los modelos creados con una forma de entrada predefinida como esta siempre tienen pesos (incluso antes de ver los datos) y siempre tienen una forma de salida definida.

En general, es una mejor práctica recomendada especificar siempre la forma de entrada de un modelo secuencial por adelantado si sabe cuál es.

## Un flujo de trabajo de depuración comunes: add() + summary()
Cuando la construcción de una nueva arquitectura secuencial, es útil para apilar capas de forma incremental con add() y con frecuencia imprimir resúmenes modelo. Por ejemplo, esto le permite controlar cómo una pila de Conv2D y MaxPooling2D capas se Downsampling mapas de características de imagen:
"""

model = keras.Sequential()
model.add(keras.Input(shape=(250, 250, 3)))  # 250x250 RGB images
model.add(layers.Conv2D(32, 5, strides=2, activation="relu"))
model.add(layers.Conv2D(32, 3, activation="relu"))
model.add(layers.MaxPooling2D(3))

# Can you guess what the current output shape is at this point? Probably not.
# Let's just print it:
model.summary()

# The answer was: (40, 40, 32), so we can keep downsampling...

model.add(layers.Conv2D(32, 3, activation="relu"))
model.add(layers.Conv2D(32, 3, activation="relu"))
model.add(layers.MaxPooling2D(3))
model.add(layers.Conv2D(32, 3, activation="relu"))
model.add(layers.Conv2D(32, 3, activation="relu"))
model.add(layers.MaxPooling2D(2))

# And now?
model.summary()

# Now that we have 4x4 feature maps, time to apply global max pooling.
model.add(layers.GlobalMaxPooling2D())

# Finally, we add a classification layer.
model.add(layers.Dense(10))

"""Muy práctico, ¿verdad?

## Qué hacer una vez que tienes un modelo

Una vez que la arquitectura de su modelo esté lista, querrá:

* Entrene su modelo, evalúelo y ejecute inferencias. Vea nuestra guía para la formación y evaluación con la incorporada en bucles
* Guarde su modelo en el disco y restáurelo. Vea nuestra guía para la serialización y ahorro .
* Acelere el entrenamiento de modelos aprovechando varias GPU. Vea nuestra guía para multi-GPU y la formación distribuida .
## Extracción de características con un modelo secuencial
Una vez que un modelo secuencial se ha construido, se comporta como un modelo funcional de la API . Esto significa que cada capa tiene una input y output de atributos. Estos atributos se pueden usar para hacer cosas interesantes, como crear rápidamente un modelo que extraiga los resultados de todas las capas intermedias en un modelo secuencial:
"""

initial_model = keras.Sequential(
    [
        keras.Input(shape=(250, 250, 3)),
        layers.Conv2D(32, 5, strides=2, activation="relu"),
        layers.Conv2D(32, 3, activation="relu"),
        layers.Conv2D(32, 3, activation="relu"),
    ]
)
feature_extractor = keras.Model(
    inputs=initial_model.inputs,
    outputs=[layer.output for layer in initial_model.layers],
)

# Call feature extractor on test input.
x = tf.ones((1, 250, 250, 3))
features = feature_extractor(x)

"""Aquí hay un ejemplo similar que solo extrae características de una capa:


"""

initial_model = keras.Sequential(
    [
        keras.Input(shape=(250, 250, 3)),
        layers.Conv2D(32, 5, strides=2, activation="relu"),
        layers.Conv2D(32, 3, activation="relu", name="my_intermediate_layer"),
        layers.Conv2D(32, 3, activation="relu"),
    ]
)
feature_extractor = keras.Model(
    inputs=initial_model.inputs,
    outputs=initial_model.get_layer(name="my_intermediate_layer").output,
)
# Call feature extractor on test input.
x = tf.ones((1, 250, 250, 3))
features = feature_extractor(x)

"""## Transferir el aprendizaje con un modelo Secuencial

El aprendizaje por transferencia consiste en congelar las capas inferiores en un modelo y solo entrenar las capas superiores. Si no está familiarizado con él, asegúrese de leer nuestra guía para el aprendizaje de transferencia .

Aquí hay dos planos comunes de aprendizaje por transferencia que involucran modelos secuenciales.

Primero, supongamos que tiene un modelo secuencial y desea congelar todas las capas excepto la última. En este caso, sólo tendría que iterar sobre model.layers y conjunto layer.trainable = False en cada capa, excepto la última. Como esto:
"""

model = keras.Sequential([
    keras.Input(shape=(784)),
    layers.Dense(32, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(10),
])

# Presumably you would want to first load pre-trained weights.
model.load_weights(...)

# Freeze all layers except the last one.
for layer in model.layers[:-1]:
  layer.trainable = False

# Recompile and train (this will only update the weights of the last layer).
model.compile(...)
model.fit(...)

"""Otro plan común es usar un modelo secuencial para apilar un modelo previamente entrenado y algunas capas de clasificación recién inicializadas. Como esto:"""

# Load a convolutional base with pre-trained weights
base_model = keras.applications.Xception(
    weights='imagenet',
    include_top=False,
    pooling='avg')

# Freeze the base model
base_model.trainable = False

# Use a Sequential model to add a trainable classifier on top
model = keras.Sequential([
    base_model,
    layers.Dense(1000),
])

# Compile & train
model.compile(...)
model.fit(...)

"""Si transfiere el aprendizaje, probablemente se encontrará utilizando con frecuencia estos dos patrones.

¡Eso es todo lo que necesita saber sobre los modelos secuenciales!

Para obtener más información sobre la creación de modelos en Keras, consulte:
"""