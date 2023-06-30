# Crie um ambiente Virtual se nao tiver
criar ambiente virtual  -> ```python -m venv venv```

ativar ambiente ->  ```.\venv\Scripts\activate```  
desativar ambiente -> ```deactivate```

# Para instalar as dependencias
```pip install -r requirements.txt```
# Para Criar as dependeicas caso seja necessario
```pip freeze > requirements.txt```


# Dowload dos dados Do Plan UDM 
```python discover.py -m snapshot -ct plan -svn 10 -cf yes -cd "^" -ch yes ```

# Fazer o Parse dos dados dos Planos Aprovados
```python .\Info_PLAN\PLAN_atributos.py ```



