import torch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .apps import NlpConfig


class NLPInferenceView(APIView):
    """
    API view to handle NLP inference requests.
    """

    def post(self, request, *args, **kwargs):
        input_text = request.data.get("text", "")
        output_text = self.perform_inference(input_text)
        return Response({"result": output_text}, status=status.HTTP_200_OK)

    @staticmethod
    def perform_inference(input_text):
        model = NlpConfig.model
        tokenizer = NlpConfig.tokenizer
        model.eval()
        input_tensor = tokenizer.encode(input_text, return_tensors="pt").to("cpu")
        with torch.no_grad():
            output = model.generate(input_tensor, max_length=1024)
        decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
        return decoded_output.strip()
