# Importing modules
import sys
import os
import colors
import Logo
import argparse


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


def email(repository_link,ver,save):
    try:
        import data
    except ImportError:
        colors.error('Error importing data module')
        sys.exit(1)

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
    title = getting_header(soup1)  # Getting the title of the page
    data.header = title  # Storing title of the page as Project Title
    colors.success("Repository Title : " + title, verbose)
    colors.process("Doxing started ...\n", verbose)
    stargazer_link = repository_link + "/stargazers"
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
            username = a_tag[0].get("href")
            data.username_list.append(username[1:])
    count = 1
    pos = 0
    while(count <= len(data.username_list)):
        repo_data = requests.get(
            "https://github.com/{}?tab=repositories&type=source"
            .format(data.username_list[pos])).text
        repo_soup = BeautifulSoup(repo_data, "lxml")
        a_tags = repo_soup.findAll("a")
        repositories_list = []
        for a_tag in a_tags:
            if a_tag.get("itemprop") == "name codeRepository":
                repositories_list.append(a_tag.get_text().strip())
        if len(repositories_list) > 0:
            email = get_latest_commit(
                    repositories_list[0],
                    data.username_list[pos])  # Getting stargazer's email
            data.email_list.append(str(email))
        else:
            data.email_list.append("Not enough information.")
        count += 1
        pos += 1

    # Printing or saving the emails
    print(colors.red + "{0}".format("-") * 75, colors.green, end="\n\n")
    save_data = False
    for arg in sys.argv[1:]:
        if arg == '-s' or arg == '--save':
            save_data = True
            save_info(dat='emails')
    if save_data is False:
        for e in range(len(data.email_list)):
            print(colors.white)
            print(data.username_list[e], (30-len(data.username_list[e]))*' ',
                  colors.green, '::',
                  colors.white, data.email_list[e])
    print("\n", colors.green + "{0}".format("-") * 75,
          colors.green, end="\n\n")


def save_info(dat='stardox'):
    try:
        import data
        import csv
    except ImportError:
        colors.error('Error importing data module')
        sys.exit(1)

    if dat == 'stardox':
        fields = ['Username', 'Repositories', 'Stars', 'Followers',
                  'Following', 'Email']
        rows = [[0 for x in range(6)] for y in range(len(data.username_list))]
        for row in range(len(data.username_list)):
            rows[row][0] = '@' + data.username_list[row]
            rows[row][1] = data.repo_list[row].strip()
            rows[row][2] = data.star_list[row].strip()
            rows[row][3] = data.followers_list[row].strip()
            rows[row][4] = data.following_list[row].strip()
            rows[row][5] = data.email_list[row]
    elif dat == 'emails':
        fields = ['Username', 'Email']
        rows = [[0 for x in range(2)] for y in range(len(data.username_list))]
        for row in range(len(data.username_list)):
            rows[row][0] = '@' + data.username_list[row]
            rows[row][1] = data.email_list[row]

    file_path = args.save
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


class username_details(argparse.Action):
    """Action class for username feature"""
    def __call__(self, parser, namespace, values, option_string=None):
        self.user = values
        self.url = requests.get("https://github.com/" + self.user)
        if self.url.status_code != requests.codes.ok:
            print(colors.red, "Unable to find username. Please enter"
                              " valid username and try again.")
            sys.exit()

        self.location = "No information provided."
        self.full_name = self.username = self.bio = self.location
        self.soup = BeautifulSoup(self.url.text, features="lxml")
        try:
            self.full_name = self.soup.select('.vcard-fullname')[0].get_text()
            self.username = self.soup.select('.vcard-username')[0].get_text()
            self.bio = self.soup.select('.user-profile-bio')[0].get_text()
            self.location = self.soup.select('.p-label')[0].get_text()
        except IndexError:
            pass
        self.repo_list = []
        rep = self.soup.select('a[class="text-bold flex-auto min-width-0"]')
        for i in rep:
            self.repo_list.append(i.get('href').lstrip('/'))
        self.email = self.get_email()
        self.counters = self.soup.select('.Counter')
        self.repositories = self.counters[0].get_text().strip()
        self.stars = self.counters[2].get_text().strip()
        self.followers = self.counters[3].get_text().strip()
        self.following = self.counters[4].get_text().strip()

        self.display()
        sys.exit()

    def get_email(self):
        try:
            repo = self.soup.select('span[class="repo"]')[0].get_text()
            email = get_latest_commit(repo, self.username)
        except IndexError:
            email = "Not enough information."
        return email

    def display(self):
        print(colors.green, "-" * 80)
        print(colors.blue, self.full_name, " ({})".format(self.username))
        if len(self.bio) < 80:
            print(colors.white, self.bio, '\n')
        else:
            print(colors.white, self.bio[:80], '\n', self.bio[80:])
        print(colors.yellow, "Location :: ", self.location)
        print(" Email :: ", self.email, '\n')
        print(colors.cyan, "Repositories : {} \t Stars : {} \t Followers : {} "
                           "\t Following : {} \n".format(self.repositories,
                                                         self.stars,
                                                         self.followers,
                                                         self.following))
        print(colors.orange, "Pinned/Popular Repositories")
        for rep in self.repo_list:
            print(colors.green, rep)
        print(colors.green, "-" * 80)


def stardox(repo_link, ver, save):
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
        count = 1
        pos = 0
        colors.process("Doxing started ...\n", verbose)
        print(colors.red + "{0}".format("-") * 75, colors.green, end="\n\n")
        # Fetching details of stargazers one by one.
        while(count <= len(data.username_list)):
            starer_url = "https://github.com/" + data.username_list[pos]
            user_html = requests.get(starer_url).text
            soup3 = BeautifulSoup(user_html, "lxml")
            repo_data = requests.get(
                    "https://github.com/{}?tab=repositories&type=source"
                    .format(data.username_list[pos])).text
            repo_soup = BeautifulSoup(repo_data, "lxml")
            a_tags = repo_soup.findAll("a")
            repositories_list = []
            for a_tag in a_tags:
                if a_tag.get("itemprop") == "name codeRepository":
                    repositories_list.append(a_tag.get_text().strip())
            if len(repositories_list) > 0:
                email = get_latest_commit(
                        repositories_list[0],
                        data.username_list[pos])  # Getting stargazer's email
                data.email_list.append(str(email))
            else:
                data.email_list.append("Not enough information.")
            if(user_html is not None):
                items = soup3.findAll("a", {"class": "UnderlineNav-item"})
                for item in items[1:]:
                    # Getting total repositories of the stargazer
                    if item.get("href").endswith("repositories") is True:
                        a_tag = item.findAll("span")
                        repo_count = a_tag[0].get_text()
                        data.repo_list.append(repo_count)
                    # Getting total stars by the stargazer
                    elif item.get("href").endswith("stars") is True:
                        a_tag = item.findAll("span")
                        star_count = a_tag[0].get_text()
                        data.star_list.append(star_count)
                    # Getting total followers of the stargazers
                    elif item.get("href").endswith("followers") is True:
                        a_tag = item.findAll("span")
                        followers_count = a_tag[0].get_text()
                        data.followers_list.append(followers_count)
                    # Getting following list of the stargazers
                    elif item.get("href").endswith("following") is True:
                        a_tag = item.findAll("span")
                        following_count = a_tag[0].get_text()
                        data.following_list.append(following_count)
                if print_data is True:
                    try:
                        import structer
                        # Plotting the tree structer of the fetched details
                        structer.plotdata(len(data.username_list), pos, count)
                    except ImportError:
                        colors.error("Error importing structer module.")
                        sys.exit(1)
                count += 1
                pos += 1

        if save_data is True:
            save_info()

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
                            required=False, default="../Desktop")
        parser.add_argument('-e', '--email', action='store_true',
                            help="Fetch only emails of stargazers.",
                            required=False, default=False)
        parser.add_argument('-u', '--username', type=str,
                            help="Fetch a user's profile information.",
                            action=username_details, required=False)

        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            colors.error('Error importing requests module.')

        args = parser.parse_args()
        repository_link = args.rURL
        verbose = args.verbose
        issave = args.save
        isemail = args.email


        if args.rURL == False:
            repository_link = input(
                        "\033[37mEnter the repository address :: \x1b[0m")
            print(repository_link)

        repository_link = format_url(repository_link)
        if isemail:
            email(repository_link,verbose,issave)
        else:
            stardox(repository_link,verbose,issave)

    except KeyboardInterrupt:
        print("\n\nYou're Great..!\nThanks for using :)")
        sys.exit(0)
