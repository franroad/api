# API PROJECT

1. Create the virtual environment, ``python3 -m venv venv1``
2. view-->command palet --> python select interpreter select the env we have installed
3. ``source venv1/bin/activate`` // deactivaste // venv1/Scripts/Activate.ps1
    - pip install fastapi[all]// pip install 'fastapi[all]'
4. Instalar FastApi
5. levantar el server ``fastapi dev main.py``

# POSTMAN
Used in test section for testing purposes but there are no schema.

Example call:
```json

{
"title":"hello from yakutia" ,
"content":"this is a test",
"published": "true",
"rating": "1"

}
```
# Pydantic
- for validating , for defining an schema that the user must accomplish. Thanks to Pydantic we make sure that the field ``rating`` for example, is an integer.


# NOTES
- Iterating to get index and content

```python
for i, p in enumerate(my_posts):
    print(f"Index: {i}, ID: {p['id']}, Title: {p['title']}, Content: {p['content']}")

```
**OUTPUT**
```python
Index: 0, ID: 1, Title: Post 1, Content: Content of post 1
Index: 1, ID: 2, Title: Post 2, Content: Content of post 2
Index: 2, ID: 3, Title: Post 3, Content: Content of post 3
```