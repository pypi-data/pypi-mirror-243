def nvprint(*args, t=False):
    for i, arg in enumerate(args):
        vnames = [name for name in globals() if globals()[name] is arg]

        if vnames:  # 리스트가 비어있지 않은 경우
            if t is True:
                var_type = str(type(arg)).split("'")[1]
                print(f"{vnames[0]}: {arg} | Type: {var_type}")  # 리스트 내부의 첫 번째 값(이름)을 출력
            else:
                print(f"{vnames[0]}: {arg}")  # 리스트 내부의 첫 번째 값(이름)을 출력

        else:
            print(f"Error, Can't print parameter number\"{i}\".")
