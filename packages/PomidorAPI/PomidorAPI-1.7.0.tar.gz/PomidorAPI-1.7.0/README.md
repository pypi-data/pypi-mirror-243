## PomidorAPI 
#### This module was created by https://t.me/pythonmainer for convenient access to the API of https://pomidorproject.ru

## Features

### - fast and non registration work with neural networks
### - cool models
### - big usage potential
### - any language can be analysed
### - Many bugs

## Instalation

#### ```pip install PomidorAPI```

## Usage

```
from PomidorAPI import PomidorAPI
Pomidor = PomidorAPI('https://api.pomidorproject.ru')
print(Pomidor)
>>> '''PomidorAPI SDK
version - 1.5.0
methods - TETA, BRSC, AUM, DostGeneration'''

resp = Pomidor.BRSC("PomidorProject", 250, 42, "ru")
print(resp)
>>> {
"response": "Британские учёные выяснили, что проект Pomidor лучший в буткемпе кодИИм"
}
```