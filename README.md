# Camera-reconnaissante

Projet de sensibilisation à la vidéosurveillance algorithmique (VSA) dans le cadre de l'action Technopolice Paris-Banlieue

Intention du projet :

Ce projet artistique vise à concevoir une caméra de vidéosurveillance algorithmique capable de produire en temps réel des commentaires perturbants à propos des passant·es qu'elle observe. Motorisée et autonome, cette caméra vise à être déployée lors d'interventions publiques par le collectif Technopolice Paris-Banlieue.

En détournant les technologies de vidéosurveillance en une expérience tangible de gêne et d'inconfort, ce dispositif cherche à faciliter la tenue d'un débat et à susciter chez les passant·es une véritable prise de conscience sur les dérives de la VSA dans l’espace public.

# Installation et utilisation

## Git clone et creation d'un environnement virtuel python

```bash
git clone https://github.com/loubetcorentin/Camera-reconnaissante.git
cd Camera-reconnaissante
mkdir img
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Telechargement du modèle yolov11n-face

```bash
mkdir yolo-Weights
cd yolo-Weights
wget https://github.com/akanametov/yolo-face/releases/download/v0.0.0/yolov11n-face.pt
```

## Installer ollama et llava

Installer Ollama sur votre machine voir `https://ollama.com/`

Une fois ollama installé, télécharger llava :

```bash
ollama pull llava
```

