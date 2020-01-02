import data


def plotdata(stars):
    print(
        '''\033[1;37m{}
\033[1;37m|-----\033[1;32m{} (@{})
\033[1;37m|  |
\033[1;37m|  |--\033[1;32mTotal Repsitories :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Stars       :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Followers   :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Following   :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mUser Email        :: \033[1;37m{}
\033[1;37m|'''.format("|", data.info_dict["name"], data.info_dict["username"],
                    data.info_dict["repos"].strip(),
                    data.info_dict["stars"].strip(),
                    data.info_dict["followers"].strip(),
                    data.info_dict["following"].strip(),
                    data.info_dict["email"].strip()))
