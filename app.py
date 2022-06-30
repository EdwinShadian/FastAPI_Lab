#!/usr/bin/python3.10

from fastapi import FastAPI, HTTPException, Response
import uvicorn
import json

app = FastAPI()

with open('library.json') as library:
    tree = json.load(library)

@app.get("/library")
def library():
    return Response(json.dumps(tree), media_type='json')


@app.get("/library/{author}")
def author_name(author):
    match author:
        case "Pushkin":
            return Response(json.dumps(tree['items']['Pushkin']), media_type='json')
        case "Yesenin":
            return Response(json.dumps(tree['items']['Yesenin']), media_type='json')
        case "Mayakovskiy":
            return Response(json.dumps(tree['items']['Mayakovskiy']), media_type='json')
        case _:
            raise HTTPException(status_code = 404, detail = "Страница не найдена")


@app.get("/library/Pushkin/{poem}")
def poems(poem):
    match poem:
        case "kern.txt":
            return Response(json.dumps(tree['items']['Pushkin']['items']['kern.txt']), media_type='json')
        case "love.txt":
            return Response(json.dumps(tree['items']['Pushkin']['items']['love.txt']), media_type='json')
        case "sibiria.txt":
            return Response(json.dumps(tree['items']['Pushkin']['items']['sibiria.txt']), media_type='json')
        case _:
            raise HTTPException(status_code=404, detail="Страница не найдена")


@app.get("/library/Yesenin/{poem}")
def poems(poem):
    match poem:
        case "porosha.txt":
            return Response(json.dumps(tree['items']['Yesenin']['items']['porosha.txt']), media_type='json')
        case "bereza.txt":
            return Response(json.dumps(tree['items']['Yesenin']['items']['bereza.txt']), media_type='json')
        case "morning.txt":
            return Response(json.dumps(tree['items']['Yesenin']['items']['morning.txt']), media_type='json')
        case _:
            raise HTTPException(status_code=404, detail="Страница не найдена")


@app.get("/library/Mayakovskiy/{poem}")
def poems(poem):
    match poem:
        case "nate.txt":
            return Response(json.dumps(tree['items']['Mayakovskiy']['items']['nate.txt']), media_type='json')
        case "soviet.txt":
            return Response(json.dumps(tree['items']['Mayakovskiy']['items']['soviet.txt']), media_type='json')
        case "listen.txt":
            return Response(json.dumps(tree['items']['Mayakovskiy']['items']['listen.txt']), media_type='json')
        case _:
            raise HTTPException(status_code=404, detail="Страница не найдена")


if __name__ == "__main__":
    uvicorn.run(app)
