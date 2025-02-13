from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
import numpy as np
import base64
from io import BytesIO
import tensorflow as tf
from .models import DigitImage
from .tasks import train_and_save_model, initialize_and_save_model
from .db import connect


class RecognizeNumber(APIView):

    def post(self, request):
        data = request.data.get('image')
        if data:
            try:
                model = tf.keras.models.load_model('ocr_model_old.h5')

                # Décoder et prétraiter l'image
                image_data = base64.b64decode(data.split(',')[1])
                image = Image.open(BytesIO(image_data)).convert('L')
                image = image.resize((28, 28))
                image_array = np.array(image).reshape((28, 28)) * 255.0  # Normalisation

                # Prédire le chiffre
                prediction = model.predict(image_array.reshape(1, 28, 28, 1))
                predicted_number = np.argmax(prediction)
                accuracy = prediction[0][predicted_number] * 100

                # Sauvegarder l'image et le label prédit
                image_file = BytesIO()
                image.save(image_file, format='PNG')
                image_file.seek(0)
                digit_image = DigitImage(
                    image=image_file,
                    predicted_label=predicted_number,
                    accuracy=accuracy
                )
                digit_image.save()

                return Response({'id': str(digit_image.id), 'number': predicted_number, 'accuracy': accuracy}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid image data'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPrediction(APIView):

    def post(self, request):
        data = request.data
        try:
            image_id = data.get('image_id')
            correct_label = data.get('correct_label')

            digit_image = DigitImage.objects.get(id=image_id)
            digit_image.label = correct_label
            digit_image.verified = True
            digit_image.save()

            train_and_save_model.delay()

            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except DigitImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
