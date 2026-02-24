import git
import os

local_url = "/home/netman/netman"
url = "https://github.com/sash2087/netman.git"
branch = "new"

repo = git.Repo(local_url)

repo.git.add('*')

repo.index.commit("pushing from VM!")

origin = repo.remote(name = "origin")
origin.push(branch)

print("Error, no updates!")

#WIP.


