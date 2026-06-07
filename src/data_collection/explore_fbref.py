from ScraperFC.fbref import FBref

fbref = FBref()

print("Available FBref methods:\n")

for method in dir(fbref):
    if not method.startswith("_"):
        print(method)