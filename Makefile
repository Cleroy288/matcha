COMPOSE := docker compose

all:
	@$(COMPOSE) up --build -d
	@echo "Matcha : http://localhost:80/login"

clean:
	@$(COMPOSE) down --remove-orphans

fclean:
	@$(COMPOSE) down --rmi all --volumes --remove-orphans

re: fclean all

.PHONY: all clean fclean re
