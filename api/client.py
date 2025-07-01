import google.generativeai as genai

API_KEY = "AIzaSyDfQ9rIfvd1vfeGqA74sk58wIZoV_sGU9U"

genai.configure(api_key=API_KEY)

gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")

def get_car_ai_bio(model, brand, year):
  prompt = f'''
  Me mostre uma descrição de venda para o carro {model} {brand} {year} em apenas 250 caracteres. Fale coisas específicas desse modelo. Descreva especificações técnicas desse modelo de carro.
  '''
  response = gemini_model.generate_content(prompt)
  return response.text
