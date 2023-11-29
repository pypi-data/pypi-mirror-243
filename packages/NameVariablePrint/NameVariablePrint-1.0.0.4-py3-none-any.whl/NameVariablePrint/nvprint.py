import inspect


def nvprint(*args, t=False):
    """_summary_

    Args: All type of Variables to print its name and value.
        t (bool, optional): _description_. Defaults to False.
    """
    caller_globals = inspect.currentframe().f_back.f_globals
    for i, arg in enumerate(args):
        vnames = [name for name, value in caller_globals.items() if value is arg]

        if vnames:  # 리스트가 비어있지 않은 경우
            if t is True:
                var_type = str(type(arg)).split("'")[1]
                print(f"{vnames[0]}: {arg} | Type: {var_type}")  # 리스트 내부의 첫 번째 값(이름)을 출력
            else:
                print(f"{vnames[0]}: {arg}")  # 리스트 내부의 첫 번째 값(이름)을 출력

        else:
            print(f"Error, Can't print parameter number\"{i}\".")