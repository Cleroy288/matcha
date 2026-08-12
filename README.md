# Matcha

Matcha is a dating web application built for the 42 school project. Users can create and verify an account, complete a profile with photos and interests, and discover compatible people based on location, shared tags, and popularity.

Main features include advanced profile search, likes, mutual matches, real-time chat, notifications, profile visits, blocking, and reporting.

Built with React, Flask, PostgreSQL, Socket.IO, Nginx, and Docker.

## Run the project

Docker and Docker Compose are required. Configure the `.env` file, then run:

```bash
make
```

Open [http://localhost:5173/login](http://localhost:5173/login). Run all tests and linters with `make test`.

## Stack

- Frontend: React, TypeScript, Vite
- Backend: Flask, Python, Socket.IO
- Data and infrastructure: PostgreSQL, Nginx, Docker Compose

## Architecture

The React frontend communicates with a layered Flask API organized into routes, controllers, services, and models. PostgreSQL stores application data, Socket.IO provides real-time features, and Docker Compose runs every service.

## Developers

- Charles Leroy ([Cleroy288](https://github.com/Cleroy288))
- Pierre ([His000ka](https://github.com/His000ka))
