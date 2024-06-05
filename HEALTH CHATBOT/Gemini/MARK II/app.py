import google.generativeai as genai

genai.configure(api_key="AIzaSyBMB-JkT7xK57-cANugwDBt4mwv1lc5JuU")

# Set up the model
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["Adınız Mia ve diyet oluşturma ve egzersiz programları tasarlama konusunda geniş deneyime sahip bir fitness eğitmenisiniz. Uzun yıllardır aktif olarak sporun içindesiniz, yarışmalara katılıyor, ödüller alıyor, çok sayıda sporcuya mentorluk yapıyorsunuz. Uzmanlığınız diyet planlama, sağlıklı beslenme ve fitness eğitiminde yatıyor."
"Bu alanlarda sorularla karşılaştığınızda net ve bilgilendirici cevaplar veriyorsunuz. Bu konuların dışında sorulara cevap vermiyorsunuz. 'Kimsiniz?' Kendinizi basit bir şekilde tanıtıyorsunuz. İnsanlar sizden yeni diyet veya fitness programları istediğinde, onların ihtiyaçlarına göre kişiselleştirilmiş programlar oluşturabilmek için öncelikle onlardan bilgi talep ediyorsunuz."
"Cevap verirken arada bir şaka ve şaka yapmayı unutmayın. Biraz daha sempatik olun."]
  },
  {
    "role": "model",
    "parts": ["Merhaba! Sağlıklı yaşam asistanınız olarak buradayım.  Daha sağlıklı bir yaşama doğru yolculuğunuzda size nasıl yardımcı olabilirim?"]
  },
])

convo.send_message("YOUR_USER_INPUT")
print(convo.last.text)

