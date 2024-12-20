from app import create_app

app = create_app()


@app.get('/')
async def root():
    return {'message': 'CHUPALO PEPE'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=5050, reload=True)
