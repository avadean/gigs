import data

from gig import Gig
from person import Person
from ticket import Ticket

# Load in a schedule.
# If a saved version exists, it will be loaded. If not, an example version will be created to get started.
schedule = data.load_schedule()


# Query or add data here.
print(schedule)


# Save the schedule.
# This will be saved with a default file name that load_schedule uses by default.
data.save_schedule(schedule)

