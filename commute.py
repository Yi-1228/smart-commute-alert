import os
import requests


LATITUDE = 24.9937
LONGITUDE = 121.3010

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


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


# ===== 通勤建議 =====
def create_recommendations(
    max_temperature,
    max_rain_probability,
    aqi
):

    recommendations = []

    if max_rain_probability >= 60:
        recommendations.append(
            "☔ 降雨機率達 60%，請攜帶雨傘。"
        )

    if max_temperature >= 33:
        recommendations.append(
            "☀️ 最高溫達 33°C，請做好防曬並補充水分。"
        )

    if aqi >= 100:
        recommendations.append(
            "😷 AQI 達 100，建議配戴口罩。"
        )

    if not recommendations:
        recommendations.append(
            "✅ 天氣與空氣品質狀況正常，適合外出通勤。"
        )

    return recommendations


# ===== Telegram =====
def send_telegram(message):

    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(
        url,
        json=payload,
        timeout=10
    )

    print("Telegram HTTP Status:", response.status_code)

    response.raise_for_status()


# ===== 主程式 =====
def main():

    max_temperature, max_rain_probability = get_weather()

    aqi = get_aqi()

    recommendations = create_recommendations(
        max_temperature,
        max_rain_probability,
        aqi
    )

    message = f"""
🚨 智慧通勤風險通知

📍 地點：桃園

🌡️ 最高溫：{max_temperature:.1f}°C
🌧️ 最高降雨機率：{max_rain_probability:.0f}%
🌫️ AQI：{aqi}

📋 通勤建議：
"""

    message += "\n".join(recommendations)

    print(message)

    send_telegram(message)


if __name__ == "__main__":
    main()
