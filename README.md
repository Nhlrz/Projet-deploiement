# Projet-deploiement
Vous trouverez le projet du cours de développement au déploiement d'applications web

Docker commandes :
  RUN
  FROM
  COPY

# 📌 Documentation des Endpoints API

Base URL : http://127.0.0.1:5000

---

## 👤 Utilisateurs

### 🔹 GET /users
- **Rôle** : Récupérer la liste de tous les utilisateurs
- **Méthode** : GET
- **Body** : Aucun
- **Réponse** : Liste JSON des utilisateurs

---

### 🔹 POST /users
- **Rôle** : Créer un nouvel utilisateur
- **Méthode** : POST
- **Body (JSON)** :
```json
{
  "username": "john",
  "mail": "john@mail.com",
  "langue": "fr"
}
