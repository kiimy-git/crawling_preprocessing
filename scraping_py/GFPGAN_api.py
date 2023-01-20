import replicate
import os

import certifi

## Error - urllib 사용시??
os.environ["REPLICATE_API_TOKEN"] = "60853831b0c9b0b323da08020ae06cf14d60fe65"

## SSL/TLS 서버의 인증서 신뢰 설정


model = replicate.models.get("tencentarc/gfpgan")
print(model.versions.get("9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3"))
# version = model.versions.get("9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3")

# output = version.predict(img=".\\scraping_image(130X130)\\test1.jpg")


