import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4


def getparams():
    result = {}
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        result["temperature"] = round(temperature,1)
        result["humidity"] = round(humidity,1)
    else:
        result["temperature"] = 0
        result["humidity"] = 0
        
    return result