COMPOSE := docker compose

all:
	@$(COMPOSE) up --build -d
	@echo "Matcha : http://localhost:5173/login"

generate:
	@$(COMPOSE) exec backend python3 generator_profile.py

test:
	@$(COMPOSE) exec backend sh -c "python3 -m pytest && ruff check ."
	@$(COMPOSE) exec frontend sh -c "npm test && npm run lint"

clean:
	@$(COMPOSE) down --remove-orphans

fclean:
	@$(COMPOSE) down --rmi all --volumes --remove-orphans

re: fclean all

.PHONY: all generate test clean fclean re
