# Matcha — Cahier des charges

## 1. Presentation du projet

**Type** : Application web de rencontre
**Objectif** : Faciliter les connexions entre partenaires potentiels, de l'inscription a la rencontre.

---

## 2. Contraintes techniques

| Contrainte | Detail |
|---|---|
| Backend | Micro-framework uniquement (routeur + templating, pas d'ORM ni de gestionnaire de comptes) |
| Frontend | Libre (React, Vue, Angular, Svelte, etc.) |
| Base de donnees | Relationnelle ou graphe, gratuite (PostgreSQL, MySQL, Neo4j, etc.) — requetes manuelles |
| Serveur web | Libre (Apache, Nginx, ou serveur integre) |
| Compatibilite | Firefox + Chrome (dernieres versions) |
| Responsive | Obligatoire (mobile-friendly) |
| Securite | Zero tolerance : pas de mdp en clair, pas de XSS, pas d'injection SQL, pas d'upload non autorise |
| Seed data | 500 profils minimum en base pour l'evaluation |
| Secrets | Fichier `.env` exclu de Git |

---

## 3. Fonctionnalites obligatoires

### 3.1 Inscription et connexion

| Fonctionnalite | Detail |
|---|---|
| Inscription | email, username, nom, prenom, mot de passe securise |
| Validation MDP | Rejet des mots anglais courants |
| Verification email | Lien unique envoye par mail |
| Connexion | username + mot de passe |
| Mot de passe oublie | Email de reinitialisation |
| Deconnexion | Possible depuis n'importe quelle page (1 clic) |

### 3.2 Profil utilisateur

| Champ | Detail |
|---|---|
| Genre | Homme / Femme / Autre |
| Preferences sexuelles | Orientation (defaut : bisexuel si non renseigne) |
| Biographie | Texte libre |
| Tags d'interets | Liste de tags reutilisables (#vegan, #geek, #piercing, etc.) |
| Photos | Jusqu'a 5, dont 1 photo de profil |
| Localisation | GPS (avec consentement) ou saisie manuelle (ville/quartier) — modifiable |
| Note de popularite | Score public (criteres a definir) |

**Actions sur le profil :**
- Modifier toutes les infos (nom, prenom, email, genre, bio, tags, photos, localisation)
- Voir qui a consulte son profil
- Voir qui l'a "like"

### 3.3 Navigation (suggestions)

**Algorithme de suggestion** : proposer des profils "interessants" en respectant les preferences sexuelles.

**Criteres de matching (ponderes) :**
1. Proximite geographique (priorite)
2. Nombre de tags communs
3. Note de popularite

**Tri et filtres disponibles :**
- Age
- Localisation
- Note de popularite
- Tags communs

### 3.4 Recherche avancee

**Criteres de recherche :**
- Tranche d'age
- Plage de note de popularite
- Localisation
- Un ou plusieurs tags d'interet

Les resultats sont triables et filtrables (memes criteres que la navigation).

### 3.5 Consultation de profil

**Affichage** : toutes les infos sauf email et mot de passe.

**Lors de la visite** : enregistrement dans l'historique de visites du profil consulte.

**Actions disponibles :**
| Action | Detail |
|---|---|
| Like | Liker la photo de profil (impossible si on n'a pas de photo soi-meme) |
| Unlike | Retirer un like — desactive les notifications et le chat |
| Connexion | Automatique quand deux utilisateurs se likent mutuellement |
| Deconnexion | Se "deconnecter" d'un profil (annuler le match) |
| Statut en ligne | Voir si l'utilisateur est connecte, sinon date/heure de derniere connexion |
| Popularite | Consulter la note de popularite |
| Signaler | Signaler comme "faux compte" |
| Bloquer | L'utilisateur bloque disparait des recherches, notifications et chat |

**Indicateurs visuels** : l'utilisateur voit clairement s'il a deja like le profil ou s'il est connecte avec.

### 3.6 Chat

| Contrainte | Detail |
|---|---|
| Condition | Les deux utilisateurs doivent etre "connectes" (like mutuel) |
| Temps reel | Delai max 10 secondes |
| Notification | Visible depuis n'importe quelle page lors de la reception d'un message |

### 3.7 Notifications (temps reel, delai max 10s)

| Evenement | Notification |
|---|---|
| Like recu | "X vous a like" |
| Visite de profil | "X a consulte votre profil" |
| Message recu | "X vous a envoye un message" |
| Like reciproque | "X vous a like en retour — vous etes connectes !" |
| Unlike d'un connecte | "X s'est deconnecte de vous" |

Indicateur de notifications non lues visible depuis toutes les pages.

---

## 4. Fonctionnalites bonus

| Bonus | Detail |
|---|---|
| OmniAuth | Strategies d'authentification tierces (Google, 42, etc.) |
| Galerie photo | Upload drag-and-drop + edition (recadrage, rotation, filtres) |
| Carte interactive | Carte des utilisateurs avec localisation GPS precise (JavaScript) |
| Chat video/audio | Pour les utilisateurs connectes |
| Evenements / rendez-vous | Planification de rencontres reelles pour les utilisateurs matches |

> Les bonus ne sont evalues que si la partie obligatoire est **parfaite** (100% fonctionnelle, zero dysfonctionnement).

---

## 5. Securite — Checklist obligatoire

- [ ] Mots de passe hashes (bcrypt / argon2)
- [ ] Protection injection SQL (requetes parametrees)
- [ ] Protection XSS (sanitization des inputs, echappement des outputs)
- [ ] Validation de tous les formulaires (front + back)
- [ ] Validation des uploads (type MIME, taille, extension)
- [ ] Tokens CSRF sur les formulaires
- [ ] Variables sensibles dans `.env` (exclu de Git)
- [ ] Sessions securisees (httpOnly, secure, SameSite)
- [ ] Rate limiting sur login / reset password

---

## 6. Structures de donnees

### 6.1 Table `users`

```sql
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    username        VARCHAR(50)  UNIQUE NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    first_name      VARCHAR(100) NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    is_verified     BOOLEAN DEFAULT FALSE,
    verify_token    VARCHAR(255),
    reset_token     VARCHAR(255),
    reset_token_exp TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### 6.2 Table `profiles`

```sql
CREATE TABLE profiles (
    id                  SERIAL PRIMARY KEY,
    user_id             INT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    gender              VARCHAR(20),        -- 'male', 'female', 'other'
    sexual_preference   VARCHAR(20) DEFAULT 'bisexual', -- 'male', 'female', 'bisexual'
    biography           TEXT,
    birth_date          DATE,
    fame_rating         INT DEFAULT 0,      -- note de popularite
    latitude            DECIMAL(10, 8),
    longitude           DECIMAL(11, 8),
    city                VARCHAR(100),
    gps_consent         BOOLEAN DEFAULT FALSE,
    last_online         TIMESTAMP,
    is_online           BOOLEAN DEFAULT FALSE,
    profile_complete    BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);
```

### 6.3 Table `tags`

```sql
CREATE TABLE tags (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL  -- ex: '#vegan', '#geek'
);
```

### 6.4 Table `user_tags` (N:N)

```sql
CREATE TABLE user_tags (
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tag_id  INT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, tag_id)
);
```

### 6.5 Table `photos`

```sql
CREATE TABLE photos (
    id         SERIAL PRIMARY KEY,
    user_id    INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_path  VARCHAR(500) NOT NULL,
    is_profile BOOLEAN DEFAULT FALSE,
    sort_order SMALLINT DEFAULT 0,     -- 0 a 4
    created_at TIMESTAMP DEFAULT NOW()
);

-- Contrainte : max 5 photos par user
-- Contrainte : 1 seule is_profile = true par user
```

### 6.6 Table `likes`

```sql
CREATE TABLE likes (
    id         SERIAL PRIMARY KEY,
    liker_id   INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    liked_id   INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (liker_id, liked_id)
);

-- Un "match" (connexion) existe quand :
-- EXISTS (liker_id=A, liked_id=B) AND EXISTS (liker_id=B, liked_id=A)
```

### 6.7 Table `profile_views`

```sql
CREATE TABLE profile_views (
    id         SERIAL PRIMARY KEY,
    viewer_id  INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    viewed_id  INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    viewed_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_profile_views_viewed ON profile_views(viewed_id);
```

### 6.8 Table `blocks`

```sql
CREATE TABLE blocks (
    id         SERIAL PRIMARY KEY,
    blocker_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    blocked_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (blocker_id, blocked_id)
);
```

### 6.9 Table `reports`

```sql
CREATE TABLE reports (
    id          SERIAL PRIMARY KEY,
    reporter_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reported_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reason      TEXT,
    created_at  TIMESTAMP DEFAULT NOW(),
    UNIQUE (reporter_id, reported_id)
);
```

### 6.10 Table `messages`

```sql
CREATE TABLE messages (
    id          SERIAL PRIMARY KEY,
    sender_id   INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    receiver_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content     TEXT NOT NULL,
    is_read     BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON messages(sender_id, receiver_id);
CREATE INDEX idx_messages_receiver ON messages(receiver_id, is_read);
```

### 6.11 Table `notifications`

```sql
CREATE TABLE notifications (
    id         SERIAL PRIMARY KEY,
    user_id    INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type       VARCHAR(30) NOT NULL,  -- 'like', 'visit', 'message', 'match', 'unlike'
    from_id    INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_read    BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id, is_read);
```

---

## 7. Schema relationnel

```
users 1──1 profiles
users 1──N photos        (max 5)
users N──N tags           (via user_tags)
users N──N users          (via likes)
users N──N users          (via blocks)
users N──N users          (via reports)
users 1──N messages       (sender)
users 1──N messages       (receiver)
users 1──N notifications  (destinataire)
users 1──N profile_views  (viewer / viewed)
```

---

## 8. Note de popularite — Proposition de calcul

| Evenement | Points |
|---|---|
| Like recu | +3 |
| Unlike recu | -3 |
| Visite de profil recue | +1 |
| Match (connexion) | +5 |
| Perte de match | -5 |
| Signalement recu | -10 |
| Profil complet | +10 (one-time) |

Score min : 0 — Score max : libre (ou cap a 100 pour affichage normalise).
