

# HycBot
---
## Fonctionnalités implémentées

- **Contrôle des mouvements via le clavier**  
  Le robot peut être dirigé à l’aide des touches directionnelles du clavier et le trackpad (avancer et reculer)

- **Caméra**  
  La caméra permet la capture d’images et la diffusion d’un flux vidéo en direct.

- **Lecture de QR Codes**  
  Le robot est capable de détecter et de décoder des QR Codes.

- **Détection de zones blanches**  
  Le robot peut repérer les zones de couleur blanche, utile pour la capture de zone.

- **Émission et réception de tirs**  
  Implémentation d’un mécanisme d’envoi et la réception de tirs.

---

## Librairies utilisées par fonctionnalité

- **Contrôle des mouvements via clavier** :
  - Aucune bibliothèque spécifique n’est requise pour la lecture des touches clavier, les entrées sont traitées directement via les fonctionnalités natives de Python.
  - La bibliothèque `socket` a été utilisée dans une tentative d’intégration avec une manette (feature abandonnée en raison de problèmes matériels).

- **Caméra et lecture de QRCode**  :
  - `picamera2` : pour gérer la capture d’images à partir de la caméra du Raspberry Pi.
  - `cv2` : pour le traitement d’image et l’interprétation des QR Codes.
  - `flask + picamera + cv2` : ont été utilisées/combinées pour permettre la diffusion en temps réel du flux vidéo.

---

## Difficultés rencontrées

L'une des principales difficultés est l’intégration d’une manette PS4 pour le contrôle des mouvements. Initialement, la manette fonctionnait correctement, meme si avec Bluetooth il y avait des soucis, celle-ci fonctionnait avec un cable. Toutefois, après l’ajout de plusieurs autres fonctionnalités au robot, elle a commencé à dysfonctionner de manière aléatoire.

Nous avons tenté de la reconnecter en USB, mais les erreurs persistaient. Ces instabilités nous ont amenés à conclure que la manette était défectueuse. Malgré plusieurs essais avec la bibliothèque `pygame` pour gérer les entrées de la manette, nous avons finalement décidé d’abandonner cette approche, et de nous concentrer uniquement sur un contrôle via clavier, plus stable et plus fiable.

