import data


def plotdata(info_dict):
    print(
        '''\033[1;37m{}
\033[1;37m|-----\033[1;32m{} (@{})
\033[1;37m|  |
\033[1;37m|  |--\033[1;32mTotal Repsitories :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Stars       :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Followers   :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Following   :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mUser Email        :: \033[1;37m{}
\033[1;37m|'''.format("|", info_dict["name"], info_dict["username"],
                    info_dict["repos"].strip(),
                    info_dict["stars"].strip(),
                    info_dict["followers"].strip(),
                    info_dict["following"].strip(),
                    info_dict["email"].strip()))
