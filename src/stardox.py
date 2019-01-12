import requests
import structer
import data
import sys
import colors
import Logo
import time
from bs4 import BeautifulSoup

def formated(string):

    new_string=[]
    string=list(string)
    for value in string:
        if(value.isnumeric()):
            new_string.append(value)
    string=''.join(new_string)
    return string


def getting_header(soup_text):

    title=soup_text.title.get_text()
    start=title.find('/')
    stop=title.find(':')
    return title[start+1:stop]


def format_url(url):

    if url.startswith('http://'):
        url=url.replace('http','https')
    elif url.startswith('www.'):
        url=url.replace('www.','https://')
    elif url.startswith('https://') or url.startswith('https://www.'):
        pass
    else:
        colors.error("Enter the repositories url in given format [ https://github.com/username/repository_name ]")
        sys.exit(1)
    return url


def verify_url(page_data):

    data=str(page_data)
    if "Popular repositories" in data:
        return False
    elif "Page not found" in data:
        return False
    else:
        return True


if __name__ == '__main__':

    Logo.header()         # For Displaying Logo

    repository_link = str(input("\033[37mEnter the repository address :: \x1b[0m"))    # Getting repository Address
    print("\n")
    repository_link = format_url(repository_link)       # Assuring that URL starts with https://

    try:
        html = requests.get(repository_link,timeout=8).text       # Getting HTML page of repository
    except requests.exceptions.MissingSchema as e:
        colors.error("Enter the repositories url in given format [ https://github.com/username/repository_name ]")
        sys.exit(1)

    result=verify_url(html)                             # Checking if the url given is of a repository or not.
    if result is True:
        colors.success("Got the repository data ")
        time.sleep(1)
    else:
        colors.error("Please enter the correct URL ")
        sys.exit(0)

    soup1=BeautifulSoup(html,"lxml")                    # Parsing the html data using BeautifulSoup

    title=getting_header(soup1)                         # Getting the title of the page
    data.header=title                                   # Storing title of the page as Project Title
    colors.success("Repository Title : "+title)
    time.sleep(1)

    star_value=0
    watch_value = 0
    fork_value =0

    a_tags=soup1.findAll("a")                           # Finding all the 'a' tags in response html data.
    for a_tag in a_tags:                                # Finding total stargazers of the repository
        string=a_tag.get("href")
        if(string.endswith("/watchers")):
            watch_value=(a_tag.get_text()).strip()
            watch_value=formated(watch_value)
            colors.success("Total watchers : "+watch_value)
            time.sleep(1)
            watch_value=int(watch_value)
        if(string.endswith("/stargazers")):
            star_value=(a_tag.get_text()).strip()
            star_value=formated(star_value)
            colors.success("Total stargazers : "+star_value)
            time.sleep(1)
            star_value=int(star_value)
        if(string.endswith("/members")):
            fork_value=(a_tag.get_text()).strip()
            fork_value=formated(fork_value)
            colors.success("Total Forks : "+fork_value)
            time.sleep(1)
            fork_value=int(fork_value)
            break

    stargazer_link=repository_link+"/stargazers"
    stargazer_html=requests.get(stargazer_link).text
    soup2=BeautifulSoup(stargazer_html,"lxml")
    follow_names=soup2.findAll("h3",{"class":"follow-list-name"})

    for name in follow_names:
        a_tag=name.findAll("a")
        data.name_list.append(a_tag[0].get_text())
        username=a_tag[0].get("href")
        data.username_list.append(username[1:])

    count=1
    pos=0
    colors.process("Doxing started ...\n")
    time.sleep(1)
    print(colors.red+"--------------------------------------------------------------------------",colors.green,end="\n\n")

    while(count<=star_value):

        starer_url="https://github.com/"+data.username_list[pos]
        user_html=requests.get(starer_url).text
        soup3=BeautifulSoup(user_html,"lxml")
        if(user_html!=None):
            items=soup3.findAll("a",{"class":"UnderlineNav-item"})
            for item in items[1:]:
                if item.get("href").endswith("repositories")==True:
                    a_tag=item.findAll("span")
                    repo_count=a_tag[0].get_text()
                    data.repo_list.append(formated(repo_count))
                elif item.get("href").endswith("stars")==True:
                    a_tag=item.findAll("span")
                    star_count=a_tag[0].get_text()
                    data.star_list.append(formated(star_count))
                elif item.get("href").endswith("followers")==True:
                    a_tag=item.findAll("span")
                    followers_count=a_tag[0].get_text()
                    data.followers_list.append(formated(followers_count))
                elif item.get("href").endswith("following")==True:
                    a_tag=item.findAll("span")
                    following_count=a_tag[0].get_text()
                    data.following_list.append(formated(following_count))
            structer.plotdata(star_value,pos,count)

        count+=1
        pos+=1
    print(colors.green+"\n--------------------------------------------------------------------------",end="\n\n")
