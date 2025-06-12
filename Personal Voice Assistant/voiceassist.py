import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import requests
import tkinter as tk
import threading
import tkinter.filedialog as filedialog
from PIL import Image

# Import transformers for image captioning
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load BLIP model for image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Install TTS engine 
engine = pyttsx3.init()

# Updated speak function with threading to avoid blocking GUI
def speak(text):
    def run_speech():
        print(f"Assistant: {text}")
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run_speech).start()
    try:
        app.update_text(f"Assistant: {text}\n")
    except:
        pass

# Listen function
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        app.update_text("Listening....\n")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
        try:
            app.update_text("Recognizing...\n")
            command = recognizer.recognize_google(audio, language='en-in')
            app.update_text(f"You said: {command}\n")
        except Exception:
            speak("Sorry, I did not catch that.")
            return ""
        return command.lower()

# commands dictionary (added image captioning command)
commands = {
    "time": ["what's the time", "tell me the time", "current time", "time now"],
    "date": ["what's the date", "today's date", "current date", "date today"],
    "google": ["open google", "search google", "start google"],
    "youtube": ["open youtube", "search youtube", "start youtube"],
    "wikipedia": ["search wikipedia", "wikipedia", "find on wikipedia"],
    "weather": ["weather", "what's the weather", "current weather"],
    "caption": ["caption an image", "image caption", "describe image", "generate caption"],
    "exit": ["exit", "quit", "close assistant", "stop", "shutdown"]
}

# Basic AI Chat Response (rule-based small talk)
small_talk = {
    "how r u": "I'm doing great, thank you!",
    "who are you": "I am your personal assistant.",
    "what is your name": "You can call me your personal assistant.",
    "hello": "Hello! How can I help you?",
    "hi": "Hi there! How can I assist you?",
    "thank you": "You're welcome!"
}

# Detect command
def detect_command(user_input):
    for key, phrases in commands.items():
        for phrase in phrases:
            if phrase in user_input:
                return key
    return "unknown"

# Weather function
def get_weather(): #add your api key and city name to work this function
    API_KEY = "my_openweathermap_api_key_here"  # Insert your API key
    city = "insert your location"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        speak("Sorry, I could not get the weather.")
        return

    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    weather_report = f"The temperature in {city} is {temp}°C with {description}."
    speak(weather_report)

# Image Captioning function
def generate_caption(image_path):
    try:
        image = Image.open(image_path).convert('RGB')
        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return "Failed to generate caption."

# Execute command 
def execute_command(action, user_input):
    if action == "time":
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif action == "date":
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")

    elif action == "google":
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif action == "youtube":
        speak("Opening Youtube")
        webbrowser.open("https://www.youtube.com")

    elif action == "wikipedia":
        speak("Searching Wikipedia...")
        query = user_input.replace("wikipedia", "").strip()
        if query == "":
            speak("Please say something to search on Wikipedia.")
        else:
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                speak(result)
            except Exception as e:
                speak("Sorry, I could not find anything.")

    elif action == "weather":
        get_weather()

    elif action == "caption":
        app.open_and_caption_image()

    elif action == "exit":
        speak("Goodbye! Have a nice day.")
        app.stop_assistant()

    else:
        found = False
        for question, answer in small_talk.items():
            if question in user_input:
                speak(answer)
                found = True
                break
        if not found:
            speak("Sorry, I did not understand that yet.")

# GUI class
class AssistantGUI:
    def __init__(self, master):
        self.master = master
        master.title("Voice Assistant")

        self.label = tk.Label(master, text="Personal Voice Assistant", font=("Arial", 16))
        self.label.pack(pady=10)

        self.text_area = tk.Text(master, height=20, width=60, state=tk.DISABLED)
        self.text_area.pack(pady=10)

        self.start_button = tk.Button(master, text="Start Listening", command=self.start_listening_thread)
        self.start_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_assistant)
        self.stop_button.pack(side=tk.RIGHT, padx=20, pady=10)

        self.caption_button = tk.Button(master, text="Caption Image", command=self.open_and_caption_image)
        self.caption_button.pack(pady=10)

        self.running = False

    def update_text(self, text):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def start_listening_thread(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.run_assistant).start()

    def run_assistant(self):
        speak("Hello, I am your personal assistant. How can I help you?")
        while self.running:
            user_input = take_command()
            if user_input == "":
                continue
            action = detect_command(user_input)
            execute_command(action, user_input)

    def stop_assistant(self):
        self.running = False
        speak("Assistant stopped.")
        self.update_text("Assistant stopped.\n")

    def open_and_caption_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.update_text(f"Generating caption for {file_path}\n")
            caption = generate_caption(file_path)
            speak(caption)

# Run the GUI
root = tk.Tk()
app = AssistantGUI(root)
root.mainloop()
