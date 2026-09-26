"""Entrypoint local da MILA."""

from pathlib import Path
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from src.llm_client import LLMClientError
from src.web import carregar_view_model, processar_mensagem, renderizar_pagina

BASE_DIR = Path(__file__).resolve().parents[1]
HOST = "127.0.0.1"
PORT = 8000


def application(environ, start_response):
    metodo = environ.get("REQUEST_METHOD", "GET").upper()
    modo = "CLASSIFICACAO"
    mensagem = ""
    resposta = ""
    erro = ""
    view_model = carregar_view_model(BASE_DIR)

    if metodo == "POST":
        tamanho = int(environ.get("CONTENT_LENGTH") or "0")
        corpo = environ["wsgi.input"].read(tamanho).decode("utf-8")
        formulario = parse_qs(corpo)
        modo = formulario.get("modo", ["CLASSIFICACAO"])[0]
        mensagem = formulario.get("mensagem", [""])[0]
        try:
            resposta = processar_mensagem(modo, mensagem, view_model)
        except (LLMClientError, ValueError) as exc:
            erro = str(exc)

    html = renderizar_pagina(
        view_model,
        resposta=resposta,
        erro=erro,
        mensagem=mensagem,
        modo=modo,
    ).encode("utf-8")
    start_response(
        "200 OK",
        [("Content-Type", "text/html; charset=utf-8")],
    )
    return [html]


def main():
    with make_server(HOST, PORT, application) as servidor:
        print(f"MILA disponível em http://{HOST}:{PORT}")
        servidor.serve_forever()


if __name__ == "__main__":
    main()
