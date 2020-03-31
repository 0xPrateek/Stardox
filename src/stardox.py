# Importing modules
import sys
import os
import colors
import Logo
import argparse
import threading
import csv
import queue
import copy

# Getting the name of the repository.


def getting_header(soup_text):
    title = soup_text.title.get_text()
    start = title.find('/')
    stop = title.find(':')
    return title[start + 1: stop]


# Function to make sure all the Url passed is made in particualr format.
def format_url(url):
    if url.startswith('http://'):
        url = url.replace('http', 'https')
    elif url.startswith('www.'):
        url = url.replace('www.', 'https://')
    elif url.startswith('https://') or url.startswith('https://www.'):
        pass
    else:
        colors.error("Enter the repositories url in given format"
                     "[ https://github.com/username/repository_name ]")
        sys.exit(1)
    return url


# Function to verify that the page URL given
# is pointing to some repository or not.
def verify_url(page_data):
    data = str(page_data)
    if "Popular repositories" in data:
        return False
    elif "Page not found" in data:
        return False
    else:
        return True


# Function returning email of the stargazer
def get_latest_commit(repo_name, username):
    email = ""
    commit_data = requests.get(
        "https://github.com"
        "/{}/{}/commits?author={}".format(
            username,
            repo_name,
            username)).text
    soup = BeautifulSoup(commit_data, "lxml")
    a_tags = soup.findAll("a")
    for a_tag in a_tags:
        URL = a_tag.get("href")
        if URL.startswith("/{}/{}/commit/".format(username, repo_name)):
            label = str(a_tag.get("aria-label"))
            if "Merge" not in label and label != "None":
                patch_data = requests.get("https://github.com{}{}".format(
                    URL, ".patch")).text
                try:
                    start = patch_data.index("<")
                    stop = patch_data.index(">")
                    email = patch_data[start + 1: stop]
                except ValueError:
                    return "Not enough information."
                break
    if email != "":
        return email
    else:
        return "Not enough information."

# Fetching details of stargazers


def fetch_details(print_data, username, name):
    try:
        # No import locking required, append is a thread-safe operation
        import data
    except ImportError:
        colors.error('Error importing data module')
        sys.exit(1)

    # For storing the individual user data
    info_dict = {
        "stars": None,
        "repos": None,
        "followers": None,
        "email": None,
        "following": None,
        "name": None,
        "username": None
    }

    starer_url = "https://github.com/" + username
    user_html = requests.get(starer_url).text
    soup3 = BeautifulSoup(user_html, "lxml")
    repo_data = requests.get(
        "https://github.com/{}?tab=repositories&type=source"
        .format(username)).text
    repo_soup = BeautifulSoup(repo_data, "lxml")
    a_tags = repo_soup.findAll("a")
    repositories_list = []
    for a_tag in a_tags:
        if a_tag.get("itemprop") == "name codeRepository":
            repositories_list.append(a_tag.get_text().strip())
    if len(repositories_list) > 0:
        email = get_latest_commit(
            repositories_list[0],
            username)  # Getting stargazer's email
        info_dict["email"] = str(email)
    else:
        info_dict["email"] = "Not enough information."
    info_dict["name"] = name
    info_dict["username"] = username
    if(user_html is not None):
        items = soup3.findAll("a", {"class": "UnderlineNav-item"})
        for item in items[1:]:
            # Getting total repositories of the stargazer
            if item.get("href").endswith("repositories") is True:
                a_tag = item.findAll("span")
                repo_count = a_tag[0].get_text()
                info_dict["repos"] = repo_count
            # Getting total stars by the stargazer
            elif item.get("href").endswith("stars") is True:
                a_tag = item.findAll("span")
                star_count = a_tag[0].get_text()
                info_dict["stars"] = star_count
            # Getting total followers of the stargazers
            elif item.get("href").endswith("followers") is True:
                a_tag = item.findAll("span")
                followers_count = a_tag[0].get_text()
                info_dict["followers"] = followers_count
            # Getting following list of the stargazers
            elif item.get("href").endswith("following") is True:
                a_tag = item.findAll("span")
                following_count = a_tag[0].get_text()
                info_dict["following"] = following_count
        if print_data is True:
            try:
                import structer
                # Plotting the tree structer of the fetched details
                structer.plotdata(info_dict)
            except ImportError:
                colors.error("Error importing structer module.")
                sys.exit(1)
    data.info_dicts.append(info_dict)


def save():
    try:
        import data
    except ImportError:
        colors.error('Error importing data module')
        sys.exit(1)

    fields = ['Username', 'Repositories', 'Stars', 'Followers', 'Following',
              'Email']
    rows = [[0 for x in range(len(fields))]
            for user_i in range(len(data.username_list))]
    for row in range(len(data.username_list)):
        username = data.username_list[row]
        info_dicts = data.info_dicts
        for info_dict in info_dicts:
            if info_dict["username"] == username:
                user_data = info_dict
                break
            else:
                continue
        try:
            rows[row][0] = '@' + data.username_list[row]
            rows[row][1] = user_data["repos"].strip()
            rows[row][2] = user_data["stars"].strip()
            rows[row][3] = user_data["followers"].strip()
            rows[row][4] = user_data["following"].strip()
            rows[row][5] = user_data["email"].strip()
        except(NameError):
            colors.error("Invalid Username")
            sys.exit()

    file_path = args.path
    if file_path is not None and file_path.endswith('.csv'):
        pass
    else:
        csv_file = data.header + '.csv'  # Name of csv file
        file_path = os.path.join(os.environ["HOME"], "Desktop", csv_file)
    try:
        with open(file_path, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)
            colors.success("Saved the data into " + file_path, True)
    except FileNotFoundError:
        colors.error("Please enter valid path.")
        sys.exit()


def stardox(repo_link, ver, max_threads):
    try:
        print_data = True
        save_data = False
        for arg in sys.argv[1:]:
            if arg == '-s' or arg == '--save':
                save_data = True
                print_data = False

        repository_link = repo_link
        verbose = ver
        try:
            # Getting HTML page of repository
            html = requests.get(repository_link, timeout=8).text
        except (requests.exceptions.RequestException,
                requests.exceptions.HTTPError):
            colors.error(
                "Enter the repositories url in given format "
                "[ https://github.com/username/repository_name ]")
            sys.exit(1)
        # Checking if the url given is of a repository or not.
        result = verify_url(html)
        if result:
            colors.success("Got the repository data ", verbose)
        else:
            colors.error("Please enter the correct URL ")
            sys.exit(0)
        # Parsing the html data using BeautifulSoup
        soup1 = BeautifulSoup(html, "lxml")
        try:
            import data
        except ImportError:
            colors.error('Error importing data module')
            sys.exit(1)
        title = getting_header(soup1)  # Getting the title of the page
        data.header = title  # Storing title of the page as Project Title
        colors.success("Repository Title : " + title, verbose)
        star_value = watch_value = fork_value = 0

        # Finding all the 'a' tags in response html data.
        a_tags = soup1.findAll("a")
        for a_tag in a_tags:  # Finding total stargazers of the repository
            string = a_tag.get("href")
            if(string.endswith("/watchers")):  # Finding total watchers
                watch_value = (a_tag.get_text()).strip()
                colors.success("Total watchers : " + watch_value, verbose)
            if(string.endswith("/stargazers")):  # Finding total stargazers
                star_value = (a_tag.get_text()).strip()
                colors.success("Total stargazers : " + star_value, verbose)
            if(string.endswith("/members")):  # Finding total members
                fork_value = (a_tag.get_text()).strip()
                colors.success("Total Forks : " + fork_value, verbose)
                break
        stargazer_link = repository_link + "/stargazers"
        colors.process("Fetching stargazers list", verbose)

        # Getting list of all the stargazers
        while (stargazer_link is not None):
            stargazer_html = requests.get(stargazer_link).text
            soup2 = BeautifulSoup(stargazer_html, "lxml")
            a_next = soup2.findAll("a")
            for a in a_next:
                if a.get_text() == "Next":
                    stargazer_link = a.get('href')
                    break
                else:
                    stargazer_link = None
            follow_names = soup2.findAll("h3", {"class": "follow-list-name"})
            for name in follow_names:
                a_tag = name.findAll("a")
                data.name_list.append(a_tag[0].get_text())
                username = a_tag[0].get("href")
                data.username_list.append(username[1:])

        colors.process("Doxing started ...\n", verbose)
        print(colors.red + "{0}".format("-") * 75, colors.green, end="\n\n")

        def wrapper_fetch(f, print_data, q1, q2):
            while True:
                try:
                    username = q1.get(timeout=3)
                    name = q2.get(timeout=3)
                except queue.Empty:
                    return
                f(print_data, username, name)
                q1.task_done()
                q2.task_done()

        q1 = queue.Queue()
        q2 = queue.Queue()
        for (username, name) in zip(data.username_list, data.name_list):
            q1.put_nowait(username)
            q2.put_nowait(name)
        for _ in range(max_threads):
            threading.Thread(target=wrapper_fetch,
                             args=(fetch_details, print_data, q1, q2)).start()
        q1.join()
        q2.join()

        if save_data is True:
            save()

        print("\n", colors.green + "{0}".format("-") * 75,
              colors.green, end="\n\n")
    except KeyboardInterrupt:
        print("\n\nYou're Great..!\nThanks for using :)")
        sys.exit(0)


if __name__ == '__main__':
    try:
        Logo.header()  # For Displaying Logo

        parser = argparse.ArgumentParser()
        parser.add_argument('-r', '--rURL', help=" Path to repository.",
                            required=False, default=False)
        parser.add_argument('-v', '--verbose', help="Verbose",
                            required=False, default=True,
                            action='store_false')
        parser.add_argument('-s', '--save',
                            help="Save the doxed data in a csv file."
                                 " By default, saved at Desktop.",
                            required=False, default=os.path.expanduser('~') +'/Desktop',
                            metavar='path', dest='path', nargs='?')

        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            colors.error('Error importing requests module.')

        args = parser.parse_args()
        verbose = args.verbose
        repository_link = args.rURL

        if not args.rURL:
            repository_link = input(
                "\033[37mEnter the repository address :: \x1b[0m")
            print(repository_link)

        repository_link = format_url(repository_link)

        stardox(repository_link, verbose, max_threads=16)

    except KeyboardInterrupt:
        print("\n\nYou're Great..!\nThanks for using :)")
        sys.exit(0)
