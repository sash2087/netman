import git
import os

local_url = "/home/netman/netman"
url = "https://github.com/sash2087/netman.git"
branch = "new"

repo = git.Repo(local_url)
repo.git.add(A=True)
repo.index.commit("pushing from VM!")

repo.git.pull('origin', 'main')
repo.git.push('origin', 'main')

origin = repo.remote(name = "origin")
origin.push(branch)

print("Error, no updates!")


