from django.shortcuts import render
import requests

def get_weather_icon_class(weather_id):
    if weather_id // 100 == 2:
        return "wi wi-thunderstorm"
    elif weather_id // 100 == 3:
        return "wi wi-sprinkle"
    elif weather_id // 100 == 5:
        return "wi wi-rain"
    elif weather_id // 100 == 6:
        return "wi wi-snow"
    elif weather_id // 100 == 7:
        return "wi wi-fog"
    elif weather_id == 800:
        return "wi wi-day-sunny"
    elif weather_id == 801:
        return "wi wi-day-cloudy"
    elif weather_id // 100 == 8:
        return "wi wi-cloudy"
    else:
        return "wi wi-na"

def fetch_weather_data(city):
    api_key = 'b745d7af4d0cc18e3e121e9e897c1c5e'
    source = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}"
    response = requests.get(source)
    list_of_data = response.json()
    weather_id = list_of_data['weather'][0]['id']
    
    if response.status_code == 200:
        if 'coord' in list_of_data:
            data = {
                "country_code": str(list_of_data.get('sys', {}).get('country', 'DefaultCountryCode')),
                "coordinate": f"{list_of_data['coord']['lon']} {list_of_data['coord']['lat']}",
                "temp": round((list_of_data['main']['temp'] - 32) * 5.0 / 9.0, 2),
                "humidity": str(list_of_data['main']['humidity']),
                "city": str(list_of_data.get('name', 'DefaultCityName')),
                "wind_speed": str(list_of_data.get('wind', {}).get('speed', 'DefaultWindSpeed')),
                "weather_icon_class": get_weather_icon_class(weather_id)
            }
        else:
            data = {
                'error': 'City not found or API response does not contain coordinates.'
            }
    else:
        data = {
            'error': f"Error fetching data from API: {list_of_data.get('message', 'Unknown error')}"
        }
    
    return data

def weather(request):
    default_city = 'Delhi'
    if request.method == 'POST':
        city = request.POST.get('city')
        if not city:
            data = {
                'error': 'Please enter a city name.'
            }
        else:
            data = fetch_weather_data(city)
    else:
        data = fetch_weather_data(default_city)
    
    return render(request, "weather.html", data)
