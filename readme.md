# Object detection API + Front-end and OpenCv Live webcam
Detecção de objetos com Inteligência artificial, front-end para upload de arquivos, webservice para consumo via API. Desenvolvido em python 3 com Flask. Para detecção de objetos o modelo adotado foi YoloV3 com Tensorflow 1.14.
A segunda página tem um exemplo em python do consumo da câmera local para aplicar filtros com opencv.

## Instalação

Recomendo a utilização de um gerenciador de pacotes e ambiente virtual como o [pip](https://pip.pypa.io/en/stable/), para instalar os pacotes necessários execute:

```bash
pip install -r requirements.txt
```

Baixe os pesos pré-treinados no dataset COCO, que detecta mais de 80 classes. Importante: Extraia dentro da pasta yolov3Tf/data/darknet_weight
[Download YoloV3 weights](https://emannuell.com.br/downloads/darknet_weights.zip)

## Forma de uso
Para executar a aplicação:
```bash
python app.py
```
