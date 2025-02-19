from flask import Flask, url_for


def generate_routes(app: Flask, blueprint_name: str) -> object:
    """
    Генерирует динамические маршруты для шаблонов на основе зарегистрированных маршрутов Flask-приложения.

    Этот метод перебирает все маршруты, зарегистрированные в приложении Flask, и возвращает
    словарь, где ключами являются имена конечных точек (endpoints) маршрутов, а значениями -
    соответствующие URL-адреса. Только маршруты, которые принадлежат указанному blueprint'у
    и не являются статическими, включаются в результат.

    :param app: Экземпляр Flask-приложения, для которого генерируются маршруты.
    :param blueprint_name: Имя blueprint'а, маршруты которого должны быть сгенерированы.
    :return: Словарь с конечными точками и соответствующими URL-адресами для заданного blueprint'а.
    """
    routes = {}
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith(blueprint_name + ".") and "static" not in rule.endpoint:
                endpoint_name = rule.endpoint.split(".")[-1]
                routes[endpoint_name] = url_for(rule.endpoint)
    return routes


def utility_routes(app: Flask, blueprint_name: str) -> dict[str, object]:
    """
    Генерирует и возвращает маршруты для указанного blueprint'а в виде словаря.

    Использует функцию generate_routes для получения всех маршрутов blueprint'а
    и возвращает их в структуре, где ключ - 'routes', а значение - словарь с маршрутами.

    :param app: Экземпляр Flask-приложения.
    :param blueprint_name: Имя blueprint'а.
    :return: Словарь с ключом 'routes' и значением, являющимся словарем маршрутов.
    """
    return {"routes": generate_routes(app, blueprint_name)}
