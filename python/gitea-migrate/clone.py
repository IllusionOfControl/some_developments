import git
import tempfile
import re

repos = [
    "http://git.dream.vm/Illusion_of_control/bsuir_ootpisp.git",
    "http://git.dream.vm/Illusion_of_control/bsuir_siaod.git",
    "http://git.dream.vm/Illusion_of_control/bsuir_kpo.git",
    "http://git.dream.vm/Illusion_of_control/bsuir_sp.git",
    "http://git.dream.vm/Illusion_of_control/bsuir_spp.git"
]

name_re = re.compile(r"^http://[\w\.]{6,}/[\w\.]{3,}/([^/]+)\.git$")

for repo in repos:
    name = name_re.match(repo).groups()[0]
    git.Repo.clone_from(repo, name)
