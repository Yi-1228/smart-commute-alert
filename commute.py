import requests


LATITUDE = 24.9937
LONGITUDE = 121.3010


# ===== 天氣 API =====
def get_weather():

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "temperature_2m_max,precipitation_probability_max",
        "timezone": "Asia/Taipei"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    print("Weather HTTP Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

    max_temperature = max(
        data["daily"]["temperature_2m_max"]
    )

    max_rain_probability = max(
        data["daily"]["precipitation_probability_max"]
    )

    return max_temperature, max_rain_probability


# ===== AQI API =====
def get_aqi():

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "us_aqi",
        "timezone": "Asia/Taipei"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    print("AQI HTTP Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

    aqi_values = [
        value
        for value in data["hourly"]["us_aqi"]
        if value is not None
    ]

    max_aqi = max(aqi_values)

    return max_aqi


# ===== 測試 =====
max_temperature, max_rain_probability = get_weather()

aqi = get_aqi()

print("最高溫度:", max_temperature, "°C")
print("最高降雨機率:", max_rain_probability, "%")
print("AQI:", aqi)
# ===== 通勤建議 =====

recommendations = []


if max_rain_probability >= 60:
    recommendations.append("☔ 降雨機率達 60%，請攜帶雨傘。")


if max_temperature >= 33:
    recommendations.append("☀️ 最高溫達 33°C，請做好防曬並補充水分。")


if aqi >= 100:
    recommendations.append("😷 AQI 達 100，建議配戴口罩。")


if not recommendations:
    recommendations.append("✅ 天氣與空氣品質狀況正常，適合外出通勤。")


print()
print("===== 通勤建議 =====")

for recommendation in recommendations:
    print(recommendation)
