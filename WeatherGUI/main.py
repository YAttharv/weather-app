import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:", self)
        self.city_inp = QLineEdit(self)
        self.getWeather_button = QPushButton("Get Weather", self)
        self.temp_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.desc_label = QLabel(self)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("D:\\My\\Coding\\Code\\Python Projects\\WeatherGUI\\weather_icon.jpg"))

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_inp)
        vbox.addWidget(self.getWeather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.desc_label)
        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_inp.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_inp.setObjectName("city_inp")
        self.getWeather_button.setObjectName("getWeather_button")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.desc_label.setObjectName("desc_label")

        self.setStyleSheet("""QLabel, QPushButton{
                           font-family: calibri;}

                           QLabel#city_label, QLineEdit#city_inp{
                           font-size: 40px;
                           font-family: Aerial}
                           
                           QPushButton#getWeather_button{
                           font-size: 30px;
                           font-weight: bold;}
                           
                           QLabel#temp_label{
                           font-size: 75px;}
                           
                           QLabel#emoji_label{
                           font-size: 100px;
                           font-family: Segoe UI emoji;}
                           
                           QLabel#desc_label{
                           font-size: 50px;
                           font-weight: bold;}""")
        self.getWeather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "1cf82396dd6abd0c69c270713a47daf0"
        city = self.city_inp.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAccess denied")
                case 404:
                    self.display_error("Not found\nCity not found")
                case 500:
                    self.display_error("Internal server error\nPlease try again later")
                case 502:
                    self.display_error("Bad gateway\nInvalid response from the server")
                case 503:
                    self.display_error("Service unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway timeout\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message:str):
        self.emoji_label.setText("")
        self.desc_label.setText("")
        self.temp_label.setStyleSheet("font-size: 30px")
        self.temp_label.setText(message)

    def display_weather(self, data):
        self.temp_label.setStyleSheet("font-size: 75px")
        temp = data["main"]["temp"] - 273.15
        temp = round(temp, 2)
        temp = str(temp) + "°C"
        self.temp_label.setText(temp)

        weather_id = data['weather'][0]['id']
        self.emoji_label.setText(self.getEmoji(weather_id))

        desc = data['weather'][0]['description']
        self.desc_label.setText(desc)

    def getEmoji(self, id):
        if 200 <= id <= 232:
            emoji = '⛈️'
        elif 300 <= id <= 321:
            emoji = '🌦️'
        elif 500 <= id <= 531:
            emoji = '🌧️'
        elif 600 <= id <= 622:
            emoji = '🌨️'
        elif 701 <= id <= 741:
            emoji = '༄'
        elif id == 762:
            emoji = '🌋'
        elif id == 771:
            emoji = '💨'
        elif id == 781:
            emoji = '🌪️'
        elif id == 800:
            emoji = '☀️'
        elif id == 801:
            emoji = '🌤️'
        elif id == 802:
            emoji = '⛅'
        elif id == 803:
            emoji = '🌥️'
        elif id == 804:
            emoji = '☁️'
        else:
            emoji = ""
        return emoji

def main():
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
