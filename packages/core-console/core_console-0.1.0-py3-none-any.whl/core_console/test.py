from rich import print,inspect #type: ignore

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
a = "a"
inspect(a,methods=True)