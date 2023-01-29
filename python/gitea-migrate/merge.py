import git
import tempfile
import re

name_re = re.compile(r"^http://[\w\.]{6,}/[\w\.]{3,}/([^/]+)\.git$")

original_repo = git.Repo("bsuir-works")
merge_repo = "http://git.dream.vm/Illusion_of_control/bsuir-prog-langs-labs.git"

temp_dir = tempfile.TemporaryDirectory()
repo = git.Repo.clone_from(merge_repo, temp_dir.name)
    
name = name_re.match(merge_repo).groups()[0]
remote = original_repo.create_remote(name, merge_repo)
remote.fetch()

original_repo.git.checkout(b=f"{name}/master")
original_repo.git.merge("--allow-unrelated-histories", f"{name}/master")

# Remove the remote repository
original_repo.delete_remote(name)


