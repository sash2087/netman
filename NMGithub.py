import git
import os


local_url = "/home/netman/netman"
url = "https://github.com/sash2087/netman.git"
branch = "main"

repo = git.Repo(local_url)
repo.git.add('*')
repo.index.commit("pushing from VM! Look at this!")
origin = repo.remote(name = "main")
origin.push(branch)

#WIP!!!!


