
class DBM:
    def __init__(self, db_file_name):
        try:
            # reading DataBase file.
            db_file = open(db_file_name, "r")
        except Exception as e:
            print("Error: DataBase file not found.")
            print("Error log - " + str(e))
            exit(1)
        else:
            db_file = db_file.readlines()

            # create program database dictionary.
            self.db = {}

            # add albums to db.
            for item in db_file:
                if item.startswith('#'):
                    self.db[item[1:item.find("::")]] = dict()
                    self.db[item[1:item.find("::")]].update({"songs": dict()})
                    self.db[item[1:item.find("::")]].update({"year": item[item.find("::") + 2:item.find('\n')]})

            # add to albums it's songs.
            current_album_flag = db_file[0]
            for item in db_file:
                if item.startswith('*'):
                    self.db[current_album_flag[1:current_album_flag.find("::")]]["songs"].update(
                        {item[1:item.find("::")]: dict()})
                    self.db[current_album_flag[1:current_album_flag.find("::")]]["songs"][item[1:item.find("::")]]. \
                        update({"length": item.split("::")[2]})
                    self.db[current_album_flag[1:current_album_flag.find("::")]]["songs"][item[1:item.find("::")]]. \
                        update({"lyrics": list()})
                elif item.startswith('#'):
                    current_album_flag = item

            # add songs lyrics to each song in db.
            current_album_flag = db_file[0]
            current_song_flag = db_file[1]
            for item in db_file:
                if item.startswith('#'):
                    current_album_flag = item
                elif item.startswith('*'):
                    current_song_flag = item
                else:
                    self.db[current_album_flag[1:current_album_flag.find("::")]]["songs"][
                        current_song_flag[1:current_song_flag.find("::")]]["lyrics"].append(item.split('\n')[0])

    @staticmethod
    def print_menu():
        print("\nMenu: (enter the desired command number)\n"
              "1 - Albums List\n"
              "2 - Album Songs List\n"
              "3 - Song Length\n"
              "4 - Song Lyrics\n"
              "5 - Song Album Name\n"
              "6 - Find Song With Specified Word In Title\n"
              "7 - Find Song With Specified Word In Lyrics\n"
              "8 - Exit\n")

    @staticmethod
    def get_albums_list(database):
        for item in database.keys():
            print(item)

    @staticmethod
    def get_songs_list(database):
        album_name = input("Enter album name: ")
        if album_name in database:
            songs = database[album_name]["songs"].keys()
            print('\n')
            for song in songs:
                print(song)
        else:
            print("Error: Album name not found.")

    @staticmethod
    def get_song_length(database):
        song_name = input("Enter song name: ")
        for album_name in database.keys():
            for song in database[album_name]["songs"].keys():
                if song == song_name:
                    print("Song Length:", database[album_name]["songs"][song]["length"])
                    return

        print("Error: Song name not found.")

    @staticmethod
    def get_song_lyrics(database):
        song_name = input("Enter song name: ")
        for album_name in database.keys():
            for song in database[album_name]["songs"].keys():
                if song == song_name:
                    print("Song lyrics:\n")
                    for line in database[album_name]["songs"][song]["lyrics"]:
                        print(line)
                    return

        print("Error: Song name not found.")

    @staticmethod
    def get_song_album(database):
        song_name = input("Enter song name: ")
        for album_name in database.keys():
            for song in database[album_name]["songs"].keys():
                if song == song_name:
                    print("Album name:", album_name)
                    return

        print("Error: Song name not found.")

    @staticmethod
    def find_song_by_title(database):
        song_list_counter = 0
        search_term = input("Enter search term: ")
        print("\nSongs list:")
        for album_name in database.keys():
            for song in database[album_name]["songs"].keys():
                if search_term.lower() in song.lower():
                    print(song)
                    song_list_counter += 1

        if song_list_counter == 0:
            print("There is no songs with this search term in theirs title.")

    @staticmethod
    def find_song_by_lyrics(database):
        song_list_counter = 0
        search_term = input("Enter search term: ")
        print("\nSongs list:")

        songs = set()
        for album_name in database.keys():
            for song in database[album_name]["songs"].keys():
                for song_line in database[album_name]["songs"][song]["lyrics"]:
                    if search_term.lower() in song_line.lower():
                        songs.add(song)
                        song_list_counter += 1

        if song_list_counter == 0:
            print("There is no songs with this search term in theirs lyrics.")
        else:
            for item in songs:
                print(item)

    def play(self):
        # show menu to user.
        self.print_menu()

        # user menu commands input choosing.
        command = input("Enter Command: ")
        while command != "exit":
            match command:
                case '1':
                    # albums list
                    self.get_albums_list(self.db)
                case '2':
                    # songs list in album
                    self.get_songs_list(self.db)
                case '3':
                    # song length
                    self.get_song_length(self.db)
                case '4':
                    # song lyrics
                    self.get_song_lyrics(self.db)
                case '5':
                    # which album song in
                    self.get_song_album(self.db)
                case '6':
                    # find song by title word
                    self.find_song_by_title(self.db)
                case '7':
                    # find song by lyrics word
                    self.find_song_by_lyrics(self.db)
                case '8':
                    # exit
                    print("\nExiting Program...")
                    exit(0)
                case default:
                    # unknown command try again.
                    print("\nError: Command", default, " not found (use numbers only and according to menu).")

            # show menu to user.
            self.print_menu()

            # user menu commands input choosing.
            command = input("Enter Command: ")
