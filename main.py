from data import load_info, save_info, People
from gig import Gig
from person import Person
from ticket import Ticket


# Load in all information - including schedule, people, etc.
# If a saved version exists, it will be loaded. If not, an example version will be created to get started.
schedule, people = load_info()


# Query, add or remove data here.
print(schedule)


# Save the information.
# This will be saved with a default file name that load_info uses by default.
save_info(schedule, people)

