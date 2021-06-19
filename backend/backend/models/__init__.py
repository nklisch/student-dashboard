# This allows us to remove the nesting of namespaces if we would
# upper level packadges to not have to drill down anouther level
# to access these classes

from .agile import Issue, Sprint, Epic
from .repo import Repo, Pull, Commit
from .users import User, Team, Class
