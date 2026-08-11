COMPOSE := docker compose

all:
	@$(COMPOSE) up --build -d
	@echo "Matcha : http://localhost:5173/login"

generate:
	@$(COMPOSE) exec backend python3 generator_profile.py

clean:
	@$(COMPOSE) down --remove-orphans

fclean:
	@$(COMPOSE) down --rmi all --volumes --remove-orphans

re: fclean all

.PHONY: all clean fclean re
