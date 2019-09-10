__author__ = 'Carl Huang, yuhui97@live.unc.edu, Onyen = yuhui97'

# Loads data for both books and movies, returning a dictionary with two keys, 'books' and 'movies', one for
# each subset of the collection.
# Loads data for both books and movies, returning a dictionary with two keys, 'books' and 'movies', one for
# each subset of the collection.
def load_collections():

    # Load the two collections.
    book_collection, max_book_id = load_collection("books.csv")
    movie_collection, max_movie_id = load_collection("movies.csv")

    # Check for error.
    if (book_collection is None) or (movie_collection is None):
        return None, None

    # Return the composite dictionary.
    return {"books": book_collection, "movies": movie_collection}, max(max_book_id, max_movie_id)


# Loads a single collection and returns the data as a list.  Upon error, None is returned.
def load_collection(file_name):
    max_id = -1
    try:
        # Create an empty collection.
        collection = []

        # Open the file and read the field names
        collection_file = open(file_name, "r")
        field_names = collection_file.readline().rstrip().split(",")

        # Read the remaining lines, splitting on commas, and creating dictionaries (one for each item)
        for item in collection_file:
            field_values = item.rstrip().split(",")
            collection_item = {}
            for index in range(len(field_values)):
                if (field_names[index] == "Available") or (field_names[index] == "Copies") or (field_names[index] == "ID"):
                    collection_item[field_names[index]] = int(field_values[index])
                else:
                    collection_item[field_names[index]] = field_values[index]
            # Add the full item to the collection.
            collection.append(collection_item)
            # Update the max ID value
            max_id = max(max_id, collection_item["ID"])

        # Close the file now that we are done reading all of the lines.
        collection_file.close()

    # Catch IO Errors, with the File Not Found error the primary possible problem to detect.
    except FileNotFoundError:
        print("File not found when attempting to read", file_name)
        return None
    except IOError:
        print("Error in data file when reading", file_name)
        collection_file.close()
        return None

    # Return the collection.
    return collection, max_id

# This method checks in books.
def check_in(library_collections):
    print("Welcome to book check in system. I hope you did not miss the due date. :)")
    print()

    able_to_find = False
    library_collections_values_books = library_collections["books"]
    library_collections_values_movies = library_collections["movies"]

    item_id = input("Please enter the ID number of the item you want to check in: ")

    # First, access each item in the list.
    for val in range(0, len(library_collections_values_books)):
        each_item_dictionary = library_collections_values_books[val]
        # Next, in each item of the list, access each key and its corresponding value.
        for key in each_item_dictionary:
            # When reaching the key ID, and if the item's id matches what we are looking for,
            if key == "ID":
                if str(each_item_dictionary[key]) == item_id:
                    able_to_find = True
                    for available_key in each_item_dictionary:
                        # then we go find the key available and check if the amount of available items is less then its original copy.
                        if available_key == "Available":
                            for copies_key in each_item_dictionary:
                                if copies_key == "Copies":
                                    # If so, we will allow check in of the item and update its available amount.
                                    if int(each_item_dictionary[available_key]) < int(each_item_dictionary[copies_key]):
                                        available_num = int(each_item_dictionary[available_key])
                                        each_item_dictionary[available_key] = available_num + 1
                                        str(each_item_dictionary[available_key])
                                        print()
                                        print("You have successfully checked in this book")
                                        for key in each_item_dictionary:
                                            print(key, each_item_dictionary[key], sep=": ")
                                    # If not, then tell the user check in failed.
                                    else:
                                        print()
                                        print("This book is not missing any copy. Check in failed.")

    # The following is almost identical to the check in of a book except that it checks in a movie.
    for val in range(0, len(library_collections_values_movies)):
        each_item_dictionary = library_collections_values_movies[val]
        for key in each_item_dictionary:
            if key == "ID":
                if str(each_item_dictionary[key]) == item_id:
                    able_to_find = True
                    for available_key in each_item_dictionary:
                        if available_key == "Available":
                            for copies_key in each_item_dictionary:
                                if copies_key == "Copies":
                                    if int(each_item_dictionary[available_key]) < int(each_item_dictionary[copies_key]):
                                        available_num = int(each_item_dictionary[available_key])
                                        each_item_dictionary[available_key] = available_num + 1
                                        str(each_item_dictionary[available_key])
                                        print()
                                        print("You have successfully checked in this movie")
                                        for key in each_item_dictionary:
                                            print(key, each_item_dictionary[key], sep=": ")
                                    else:
                                        print()
                                        print("This movie is not missing any copy. Check in failed.")

    if able_to_find == False:
        print()
        print("There is no such item to be checked in. But we encourage you to donate that item to us! :))")

# This method checks out an item. It has the same logic as checking in an item.
def check_out(library_collections):
    print("Welcome to the item check out system. Let's get you equipped with knowledge.")
    print()
    able_to_find = False
    library_collections_values_books = library_collections["books"]
    library_collections_values_movies = library_collections["movies"]

    item_id = input("Please enter the ID number of the item you want to check out: ")

    for val in range(0, len(library_collections_values_books)):
        each_item_dictionary = library_collections_values_books[val]
        for key in each_item_dictionary:
            if key == "ID":
                if str(each_item_dictionary[key]) == item_id:
                    able_to_find = True
                    for another_key in each_item_dictionary:
                        if another_key == "Available":
                            if int(each_item_dictionary[another_key]) > 0:
                                available_num = int(each_item_dictionary[another_key])
                                each_item_dictionary[another_key] = available_num - 1
                                str(each_item_dictionary[another_key])
                                print()
                                print("You have successfully checked out this book")
                                for key in each_item_dictionary:
                                    print(key, each_item_dictionary[key], sep=": ")
                            else:
                                print()
                                print("This book is no longer available.")

    for val in range(0, len(library_collections_values_movies)):
        each_item_dictionary = library_collections_values_movies[val]
        for key in each_item_dictionary:
            if key == "ID":
                if str(each_item_dictionary[key]) == item_id:
                    able_to_find = True
                    for another_key in each_item_dictionary:
                        if another_key == "Available":
                            if int(each_item_dictionary[another_key]) > 0:
                                available_num = int(each_item_dictionary[another_key])
                                each_item_dictionary[another_key] = available_num - 1
                                str(each_item_dictionary[another_key])
                                print()
                                print("You have successfully checked out this movie")
                                for key in each_item_dictionary:
                                    print(key, each_item_dictionary[key], sep=": ")
                            else:
                                print()
                                print("This movie is no longer available.")

    if able_to_find == False:
        print()
        print("There is no such item to be checked out. If your heart will break without this item, "
              "you can submit a request to add this item. :)")

# This method adds a book to the library collection.
def add_book(library_collections_values, max_existing_id):
    print("Welcome to the book adding system. Hmmm, one more book to read, not bad.")
    print()
    int_max_existing_id = int(max_existing_id)
    print("Please enter the following attributes for the new book.")
    print()
    # Accepts user input
    title = input("Title: ")
    author = input("Author: ")
    publisher = input("Publisher: ")
    pages = input("Pages: ")
    year = input("Year: ")
    copies = input("Copies: ")
    # Validates user input
    while title.rstrip() == "" or author.rstrip() == "" or publisher.rstrip == "" \
            or pages.rstrip == "" or year.rstrip == "" or copies.rstrip() == "" or copies.isdigit() == False\
            or pages.isdigit() == False or year.isdigit() == False:
        print("Illegal parameter entered! Please re-enter all the parameter.")
        print("Please re-enter the following attributes for the new book.")
        print()
        title = input("Title: ")
        author = input("Author: ")
        publisher = input("Publisher: ")
        pages = input("Pages: ")
        year = input("Year: ")
        copies = input("Copies: ")
    available = copies
    print()
    # Confirm with user about his/her input and asks if he/she would like to continue the process of adding this item.
    print("You have entered the following data: ")
    print("Title: ", title)
    print("Author: ", author)
    print("Publisher: ", publisher)
    print("Pages: ", pages)
    print("Year: ", year)
    print("Copies: ", copies)
    print("Available: ", available)
    print()
    confirm_to_continue = input("Press press enter to add this item to the collection.  Enter 'x' to cancel.")
    # If so, we add the book with its attribute combined as a dictionary and then adds this dictionary to the list.
    # Please notice here that I did not perform duplicate item check because I believe I do not want to make this program
    # too complicated to read.
    if confirm_to_continue != "x":
        dict_for_new_book = {}
        dict_for_new_book["Title"] = title
        dict_for_new_book["Author"] = author
        dict_for_new_book["Publisher"] = publisher
        dict_for_new_book["Pages"] = pages
        dict_for_new_book["Year"] = year
        dict_for_new_book["Copies"] = copies
        dict_for_new_book["Available"] = available
        dict_for_new_book["ID"] = int_max_existing_id + 1
        int_max_existing_id += 1
        library_collections_values.append(dict_for_new_book)
        print("You have successfully added a book to the library.")
    return str(int_max_existing_id)

# This method adds a movie to the library collection. The logic is the same as adding a book.
def add_movie(library_collections_values, max_existing_id):
    print("Welcome to the movie adding system. One more movie to watch, fantastic.")
    print()
    int_max_existing_id = int(max_existing_id)
    print("Please enter the following attributes for the new movie.")
    print()
    title = input("Title: ")
    director = input("Director: ")
    length = input("Length: ")
    genre = input("Genre: ")
    year = input("Year: ")
    copies = input("Copies: ")
    while title.rstrip() == "" or director.rstrip() == "" or length.rstrip == "" \
            or genre.rstrip == "" or year.rstrip == "" or copies.rstrip() == "" or copies.isdigit() == False\
            or year.isdigit() == False or length.isdigit() == False:
        print("Illegal parameter entered! Please re-enter all the parameter.")
        print("Please re-enter the following attributes for the new movie.")
        print()
        title = input("Title: ")
        director = input("Director: ")
        length = input("Length: ")
        genre = input("Genre: ")
        year = input("Year: ")
        copies = input("Copies: ")
    available = copies
    print()
    print("You have entered the following data: ")
    print("Title: ", title)
    print("Author: ", director)
    print("Publisher: ", length)
    print("Pages: ", genre)
    print("Year: ", year)
    print("Copies: ", copies)
    print("Available: ", available)
    print()
    confirm_to_continue = input("Press press enter to add this item to the collection.  Enter 'x' to cancel.")
    if confirm_to_continue != "x":
        dict_for_new_book = {}
        dict_for_new_book["Title"] = title
        dict_for_new_book["Director"] = director
        dict_for_new_book["Length"] = length
        dict_for_new_book["Genre"] = genre
        dict_for_new_book["Year"] = year
        dict_for_new_book["Copies"] = copies
        dict_for_new_book["Available"] = available
        dict_for_new_book["ID"] = int_max_existing_id + 1
        int_max_existing_id += 1
        library_collections_values.append(dict_for_new_book)
        print("You have successfully added a movie to the library.")
    return str(int_max_existing_id)

# This method displays the collection of the library's book copies. It uses the same logic as checking in items
# when it comes to extracting information from the list and dictionary.
def display_collection(library_collections_values):
    print("Welcome to the item display system. Wanna peak inside the library? Find anything attractive?")
    print()
    count = 0
    for val in range(0, len(library_collections_values)):
        if count < 10:
            each_item_dictionary = library_collections_values[val]
            for key in each_item_dictionary:
                print(key, each_item_dictionary[key], sep = ": ")
        else:
            count = 0
            indicator = input("Press enter to show more items, or type m to return to the menu.")
            print()
            if indicator != "m":
                each_item_dictionary = library_collections_values[val]
                for key in each_item_dictionary:
                    print(key, each_item_dictionary[key], sep = ": ")
            else:
                break
        count += 1
        print()

# This method takes in a query from user and perform a case-insensitive search in the entire library collection.
# It also uses the same logic as checking in an item when it comes to extracting information from the list and dictionary.
def query_collection(library_collections_values):
    print("Welcome to the query system. Anything I can get for you?")
    print()
    item_to_search = input("Enter a query string to use for the search: ")
    while item_to_search.rstrip() == "":
        print("You did not enter a valid string. ")
        item_to_search = input("Re-enter a query string to use for the search: ")
    able_to_find = False
    for val in range(0, len(library_collections_values)):
        each_item_dictionary = library_collections_values[val]
        result = search(each_item_dictionary, item_to_search)
        if result == None:
            pass
        else:
            able_to_find = True
            print()
            for key in each_item_dictionary:
                print(key, each_item_dictionary[key], sep=": ")
    if able_to_find == False:
        print()
        print("I did not find any record matching the query.")

# Helper method which encapsulates the algorithim to search (case insensitive) an item in a dictionary.
def search(dict, searchFor):
    for key in dict:
        if searchFor.lower() in str(dict[key]).lower():
            return key
    return None

# Display the menu of commands and get user's selection.  Returns a string with the user's requested command.
# No validation is performed.
def prompt_user_with_menu():
    print("\n\n********** Welcome to the Collection Manager. **********")
    print("COMMAND    FUNCTION")
    print("  ci         Check in an item")
    print("  co         Check out an item")
    print("  ab         Add a new book")
    print("  am         Add a new movie")
    print("  db         Display books")
    print("  dm         Display movies")
    print("  qb         Query for books")
    print("  qm         Query for movies")
    print("  x          Exit")
    user_input = input("Please enter a command to proceed: ")
    print()
    print("---------------------------------------------------------------")
    print()
    return user_input


# This is the main program function.  This function should (1) Load the data and (2) Manage the main program loop that
# lets the user perform the various operations (ci, co, qb, etc.)
def main():
    # Load the collections, and check for an error.
    library_collections, max_existing_id = load_collections()
    if library_collections is None:
        print("The collections could not be loaded. Exiting.")
        return
    print("The collections have loaded successfully.")

    # Display the menu and get the operation code entered by the user.  We perform this continuously until the
    # user enters "x" to exit the program.  Calls the appropriate function that corresponds to the requested operation.
    operation = prompt_user_with_menu()
    while operation != "x":
        ###############################################################################################################
        ###############################################################################################################
        # HINTS HINTS HINTS!!! READ THE FOLLOWING SECTION OF COMMENTS!
        ###############################################################################################################
        ###############################################################################################################
        #
        # The commented-out code below gives you a some good hints about how to structure your code.
        #
        # FOR BASIC REQUIREMENTS:
        #
        # Notice that each operation is supported by a function.  That is good design, and you should use this approach.
        # Moreover, you will want to define even MORE functions to help break down these top-level user operations into
        # even smaller chunks that are easier to code.
        #
        # FOR ADVANCED REQUIREMENTS:
        #
        # Notice the "max_existing_id" variable?  When adding a new book or movie to the collection, you'll need to
        # assign the new item a unique ID number.  This variable is included to make that easier for you to achieve.
        # Remember, if you assign a new ID to a new item, be sure to keep "max_existing_id" up to date!
        #
        # Have questions? Ask on Piazza!
        #
        ###############################################################################################################
        ###############################################################################################################
        #
        #
        if (operation == "ci"):
            check_in(library_collections)
            print()
            input("Press enter to go back to the main menu.")
        elif (operation == "co"):
            check_out(library_collections)
            print()
            input("Press enter to go back to the main menu.")
        elif (operation == "ab"):
            max_existing_id = add_book(library_collections["books"], max_existing_id)
            print()
            input("Press enter to go back to the main menu.")
        elif (operation == "am"):
            max_existing_id = add_movie(library_collections["movies"], max_existing_id)
            print()
            input("Press enter to go back to the main menu.")
        elif (operation == "db"):
            display_collection(library_collections["books"])
        elif (operation == "dm"):
            display_collection(library_collections["movies"])
        elif (operation == "qb"):
            query_collection(library_collections["books"])
            print()
            input("Press enter to go back to the main menu.")
        elif (operation == "qm"):
            query_collection(library_collections["movies"])
            print()
            input("Press enter to go back to the main menu.")
        else:
            print("Unknown command.  Please try again.")

        operation = prompt_user_with_menu()

    if operation == "x":
        print("See you and have a nice day. :)")


# Start the program!
main()