# TODO — Navigation + Recherche + Chat + Responsive (parties Charles)

## Backend
- [x] Table `messages` dans schema.sql + application auto du schema au boot (idempotent)
- [x] Statut en ligne : socket connect/disconnect → `is_online` / `last_online` en DB
- [x] Algo suggestions `GET /browse` : compat orientation (bisexuel par défaut), exclusion blocks/likes,
      score = tags communs + proximité géo + fame, tri (âge, distance, fame, tags), filtres (âge, distance, fame, tags communs)
- [x] Recherche avancée `GET /search` : tranche âge, plage fame, ville, tags — triable/filtrable pareil
- [x] Consultation profil `GET /profile/<id>` enrichi : toutes infos publiques + distance + is_online/last_online
      + liked_by_me / likes_me / connected / i_blocked
- [x] Like impossible sans photo de profil (exigence sujet IV.5)
- [x] Chat : model + service + controller + routes
      (`GET /chat/conversations`, `GET /chat/messages/<id>`, `POST /chat/messages/<id>`, `GET /chat/unread`)
      envoi → insert + notif "message" + emit socket `new_message`

## Frontend
- [x] Services : browse.ts, chat.ts, social.ts étendu (block, report, profil public)
- [x] Home/Feed : brancher sur /browse + panneau tri/filtres
- [x] Page Recherche `/search` : formulaire critères + mêmes cards stack
- [x] Page profil public `/user/:id` : toutes infos, boutons like/unlike/block/report,
      badges "vous a liké"/"connectés", statut en ligne/dernière connexion, enregistre la visite
- [x] Page Chat `/chat` : liste conversations (matchs) + fil de messages temps réel
- [x] Badge messages non lus toutes pages (Topbar) + notif socket message
- [x] Routes App.tsx + liens Topbar (Recherche, Chat)
- [x] Responsive final (topbar, feed, chat, profil, recherche)
- [x] Tests front (vitest sur helpers/services)

## Vérification
- [x] Backend : compile + tests pytest existants passent (22/22)
- [x] Frontend : tsc + vite build OK + tests vitest OK (7/7) + eslint 0 erreur / 0 warning

## Review

### Vérification E2E effectuée (backend local port 5001 + DB docker)
- /browse : compat orientation mutuelle OK (alice pref male invisible pour carol),
  bisexuel par défaut OK (carol sans préférence voit les deux genres), common_tags,
  distance haversine, tri age/score, filtres age/fame/distance/city/min_common_tags,
  filtre invalide → 400, tri non whitelisté → 400.
- /search : tags exacts (`?tags=%23geek,%23vegan`), city ILIKE, min_common_tags.
- /profile/<id> : champs publics complets sans email, relation (liked_by_me/likes_me/connected),
  distance, 404 si bloqué ; visite enregistrée via POST /visit.
- Like : refusé sans photo de profil ; like mutuel → match:true + notif.
- Chat : envoi refusé hors match et si bloqué ; message vide refusé ; unread 1 → lecture → 0 ;
  réception temps réel via WS (`new_message` + `new_notification`) vérifiée avec un client socketio.
- Statut en ligne : is_online=TRUE à la connexion WS, FALSE + last_online à la déconnexion.
- Block : disparaît du browse, chat coupé dans les deux sens, profil 404, conversation masquée.

### Corrections apportées en cours de route
- `backend/models/report_model.py` : SQL invalide (`INTO INSERT`, `ON CONFLIC`) → report ne pouvait
  jamais fonctionner. Corrigé + testé (idempotent).
- Lint front : 4 erreurs + 2 warnings → 0/0 (StatusMessage deps via ref, TagsSection setState
  hors effect, AuthContext param inutilisé, ThemeContext eslint-disable comme AuthContext,
  Notifications dep manquante).
- `matcha-frontend/package.json` : script `test` (vitest run) ajouté.
- venv backend recassé en Python 3.11 (même version que le Dockerfile) : eventlet incompatible 3.14.

### Notes hors scope (à voir avec Pierre)
- `generator_profile.py` (seed) : utilise `werkzeug.generate_password_hash` alors que l'app
  vérifie avec bcrypt → les comptes seedés ne peuvent pas se logger ; `sexual_preference="both"`
  au lieu de "bisexual". Tâche seed marquée "commencé" côté Pierre.
- `src/hooks/useTheme.ts` : fichier mort (entièrement commenté), doublon du hook dans ThemeContext.
- `test_auth.py::test_register_login` échoue en local si `DISABLE_EMAIL_VERIFICATION=TRUE` (.env) :
  le test attend le 400 "email non vérifié". Passe avec la config CI.





1. Autoriser la localisation manuelle par ville sans GPS.
2. Bloquer le matching si le profil ou la localisation est incomplet.
3. Permettre de choisir la photo de profil principale.
4. Corriger le générateur des 500 profils : bcrypt, préférence `bisexual`, tags et photos.
5. Mettre `DISABLE_EMAIL_VERIFICATION=FALSE` et valider l’envoi SMTP.
6. Sécuriser les extensions des images uploadées.
7. Ajouter le footer obligatoire et vérifier toutes les pages sur mobile.
8. Lancer un test E2E complet avec Docker et plusieurs comptes.
9. Corriger le lint backend global.
10. Ajouter, commit et push tous les fichiers modifiés/non suivis.
