from error import pysee_errors as pye

def take_ss(x):
    try:
        raise pye[str(x)]
    except Exception as e:
        raise e

x = int(input())
try:
    take_ss(x)
except Exception as e:
    print(e)
