import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

def build_hpai_model():
    # Use MobileNetV2 for efficiency on Raspberry Pi
    base_model = MobileNetV2(input_shape=(224, 224, 3), 
                             include_top=False, 
                             weights='imagenet')
    base_model.trainable = False # Freeze base layers

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3), # Prevents overfitting on small datasets
        layers.Dense(1, activation='sigmoid') # 0: Healthy, 1: Symptomatic
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    return model

def train(data_directory):
    model = build_hpai_model()
    
    # Load processed datasets
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_directory,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(224, 224),
        batch_size=32
    )

    # Train for 10-20 epochs as per experimental design
    model.fit(train_ds, epochs=15)
    model.save('models/checkpoints/hpai_detector.h5')
    print("Model saved to models/checkpoints/")

if __name__ == "__main__":
    # Ensure your directory 'data/processed/train' contains 'healthy' and 'suspect' folders
    # train('data/processed/train')
    pass
