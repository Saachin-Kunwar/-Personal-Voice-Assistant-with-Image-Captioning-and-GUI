# -Personal-Voice-Assistant-with-Image-Captioning-and-GUI
An AI-powered desktop voice assistant built with Python that understands voice commands, performs tasks, and even describes images using deep learning. Featuring a simple and responsive Tkinter GUI, this assistant makes interaction seamless and smart.
         ---

## Features
- 🗣️ **Voice Recognition** – Listens and understands your voice commands
- 🔊 **Text-to-Speech** – Speaks responses using `pyttsx3`
- 🕒 **Tells Time & Date** – Provides current time and date
- 🌐 **Web Navigation** – Opens Google and YouTube on command
- 📚 **Wikipedia Search** – Retrieves brief summaries using the Wikipedia API
- 🌦️ **Weather Report** – Speaks the current weather using OpenWeatherMap API
- 🖼️ **Image Captioning** – Describes selected images using the BLIP vision-language model
- 💬 **Small Talk Support** – Responds to basic conversational inputs
- 🪟 **GUI Interface** – Built with `tkinter` for easy interaction
- ⚙️ **Multithreading** – Keeps the GUI responsive during operations
  
 ---
 ## 📸 Image Captioning Demo

Select any `.jpg`, `.png`, `.bmp`, or `.jpeg` image file, and the assistant will use [Salesforce's BLIP model](https://huggingface.co/Salesforce/blip-image-captioning-base) to generate a natural-language caption for the image.

---

## 🧰 Tech Stack

- Python 3.x
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [wikipedia](https://pypi.org/project/wikipedia/)
- [requests](https://pypi.org/project/requests/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)
- [transformers](https://pypi.org/project/transformers/) by Hugging Face
- [Pillow](https://pypi.org/project/Pillow/) (PIL)

---











