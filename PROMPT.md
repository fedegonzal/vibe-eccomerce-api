Create a FastAPI app to manage an ecommerce REST API platform, including:
- products: title, descripcion, price, category, pictures, tags
- categories: title, description, picture
- tags: title

This app is designed to support my students learning Frontend, to practice with a REST API.

Te app hasn't to be complex, just a simple CRUD API. Do not include authentication or advanced features.

Since different students will use this API, add a token to isolate their data. The token should be passed as a bearer token in the Authorization header, so (for example) one product can be created by one student and not visible to another, same for categories and tags.

Tha database must be SQLite, and the app should be able to run with Uvicorn.

Pictures should be stored in a local folder, and the path to the picture should be stored in the database. Every picture will be publicly accessible.

Create a `README.md` file with instructions to run the app, including how to install dependencies, how to run the server, and how to use the API with tools like HTTPie. Write the README in Markdown format, in spanish from Argentina.

Into the README, include a description about the app, its purpose, a link to https://www.untdf.edu.ar/ and how it can be used by students to practice with a REST API, also about the porpose, use this base: "Esta aplicación es un ejemplo de una API REST simple para gestionar un ecommerce, diseñada para que los estudiantes de la Tecnicatura Universitaria en Desarrollo de Aplicaciones de la Universidad Nacional de Tierra del Fuego puedan practicar con el desarrollo de Frontend y el consumo de APIs REST. Esta API fue desarrollada por el profesor Federico Gonzalez Brizzio, utilizando tecnicas de Vibe Coding, con la ayuda de Copilot y agent Claude Sonnet 4, ambas herramientas gratuitas de inteligencia artificial."

I will deploy the app in render.com, so it should be compatible with that platform, free of charge.
