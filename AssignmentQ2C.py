from AssignmentQ2B import Person
def create_people():
    people = [
        Person("u001", "Mamamia", "Female", "Travel lover", "public"),
        Person("u002", "Bobby", "Male", "Coffee enthusiast", "private"),
        Person("u003", "Charlie", "Other", "Tech geek", "public"),
        Person("u004", "Diana", "Female", "Fitness fan", "public"),
        Person("u005", "Ethan", "Male", "Gamer and streamer", "private"),
        Person("u006","Jospeh","Male","Fulltime Gambler","public"),
    ]
    return people

if __name__ == "__main__":
    profiles = create_people()
    for p in profiles:
        print(p)
