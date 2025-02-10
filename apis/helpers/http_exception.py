from fastapi import status, HTTPException


class HttpException:
    @staticmethod
    def error_handling(func):
        def wrapper(*args, **kwargs):
            func_name = str(func.__name__).strip()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=e)

        return wrapper

    @staticmethod
    def connect_database_handling(func):
        def wrapper(*args, **kwargs):
            func_name = str(func.__name__).strip()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                                    detail=f"The GrafanaUISAPI can not call GrafanaUISDatabase. --> Detail :  {e} {args} {kwargs}")

        return wrapper

    @staticmethod
    def insert_data_handling(func):
        def wrapper(*args, **kwargs):
            func_name = str(func.__name__).strip()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"{e} {args} {kwargs}")

        return wrapper
