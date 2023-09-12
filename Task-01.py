import argparse
import joblib
import numpy as np

# Load the saved model
loaded_model = joblib.load('iris_model.pkl')


def main():
    parser = argparse.ArgumentParser(description='Predict Iris Flower Species')

    # Define command-line arguments for input features
    parser.add_argument('--sepal_length', type=float,
                        required=True, help='Sepal length in cm')
    parser.add_argument('--sepal_width', type=float,
                        required=True, help='Sepal width in cm')
    parser.add_argument('--petal_length', type=float,
                        required=True, help='Petal length in cm')
    parser.add_argument('--petal_width', type=float,
                        required=True, help='Petal width in cm')

    args = parser.parse_args()

    # Collect input features
    input_features = np.array([[
        args.sepal_length,
        args.sepal_width,
        args.petal_length,
        args.petal_width
    ]])

    # Predict the class
    predicted_class = loaded_model.predict(input_features)
    class_names = ['setosa', 'versicolor', 'virginica']

    print(f"Predicted class: {class_names[predicted_class[0]]}")


if __name__ == "__main__":
    main()
